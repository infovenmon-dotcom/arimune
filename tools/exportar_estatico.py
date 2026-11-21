#!/usr/bin/env python3
"""Exporta la web y el panel de Arimune como páginas estáticas de DEMOSTRACIÓN (para enseñarlas sin servidor).
- Lee el HTML que genera el servidor Astro (npm run build:node + node dist/server/entry.mjs en 127.0.0.1:4399).
- La web y el panel comparten estado en el navegador (localStorage): una reserva hecha en la web aparece en el panel,
  y bloquear una habitación en el panel la quita de la web.
- El panel se abre con PIN 1234 (demo).
Uso: python3 tools/exportar_estatico.py <carpeta_destino> [password_panel]"""
import hashlib, hmac, os, re, shutil, sys, urllib.request
DST = sys.argv[1]; PW = sys.argv[2] if len(sys.argv) > 2 else "demo1234"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "http://127.0.0.1:4399"
tok = hmac.new(("env:" + PW).encode(), b"arimune-panel-v1", hashlib.sha256).hexdigest()
def get(path, cookie=None):
    rq = urllib.request.Request(BASE + path, headers={"Cookie": "arimune_panel=" + tok} if cookie else {})
    return urllib.request.urlopen(rq).read().decode("utf-8")

SHARED = r"""<script>
/* DEMO estática: web y panel comparten estado en este navegador */
window.ARI_DEMO={
 get:function(k,d){try{return JSON.parse(localStorage.getItem('arimune_demo_'+k))||d;}catch(e){return d;}},
 set:function(k,v){try{localStorage.setItem('arimune_demo_'+k,JSON.stringify(v));}catch(e){}}
};
</script>
"""
# ---------- WEB ----------
h = get("/")
h = h.replace('src="/fotos/', 'src="fotos/').replace("'/fotos/", "'fotos/").replace('"/fotos/', '"fotos/')
h = h.replace('src="/logo', 'src="logo').replace('href="/favicon.jpg"', 'href="favicon.jpg"')
home_shim = SHARED + r"""<script>
(function(){
 var AV=window.ARIMUNE_AVAIL=window.ARIMUNE_AVAIL||{};var st=ARI_DEMO.get('states',{});
 if(AV.activeNames){var all=(window.ARIMUNE_RM||[]).map(function(r){return r.id;});
   AV.activeNames=(all.length?all:AV.activeNames).filter(function(n){return st[n]!==undefined?st[n]:AV.activeNames.indexOf(n)>=0;});}
 AV.booked=AV.booked||{};ARI_DEMO.get('bookings',[]).forEach(function(b){(AV.booked[b.room]=AV.booked[b.room]||[]).push([b.in,b.out]);});
 var of=window.fetch;window.fetch=function(u,o){
   if(String(u).indexOf('/api/checkout')===0){var d={};try{d=JSON.parse(o.body);}catch(e){}
     var L=ARI_DEMO.get('bookings',[]);L.push({room:d.room,name:d.name,email:d.email,phone:d.phone,nif:d.nif||'',lang:d.lang||'es',consent:!!d.consent,in:d.in,out:d.out,guests:+d.pax||2,ch:'Directa',web:1});ARI_DEMO.set('bookings',L);
     return Promise.resolve(new Response(JSON.stringify({url:'#reserva-ok'}),{headers:{'content-type':'application/json'}}));}
   return of.apply(this,arguments);};
 function ok(){if(location.hash!=='#reserva-ok')return;var ov=document.getElementById('kbOv');if(ov)ov.classList.remove('open');
   var t=document.createElement('div');t.style.cssText='position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:10001;background:#2B3A2E;color:#fff;padding:16px 20px;border-radius:12px;max-width:92vw;font:500 15px system-ui;box-shadow:0 10px 30px rgba(0,0,0,.3)';
   t.innerHTML='Reserva de demostración recibida ✓ Ya aparece en el <a href="panel/" style="color:#E7C9A0">panel del hotel</a> (PIN 1234).';document.body.appendChild(t);setTimeout(function(){t.remove();},9000);history.replaceState(null,'',location.pathname);}
 window.addEventListener('hashchange',ok);
})();
</script>
"""
h = h.replace("<!--ARIMUNE_AVAIL-->", "")
h = re.sub(r"(<script>window\.ARIMUNE_AVAIL=.*?</script>)", lambda m: m.group(1) + home_shim, h, 1, re.S)
assert "ARI_DEMO" in h
# Acceso al panel desde el pie
h = h.replace('<a href="#" aria-label="Instagram de Arimune">Instagram</a>', '<a href="panel/">Acceso hotel · panel de gestión</a>')
os.makedirs(DST, exist_ok=True)
open(os.path.join(DST, "index.html"), "w", encoding="utf-8").write(h)

# ---------- PANEL ----------
p = get("/panel", cookie=True)
p = p.replace('src="/logo', 'src="../logo').replace('href="/logo.png"', 'href="../favicon.jpg"')
p = p.replace("'/fotos/", "'../fotos/").replace('"/fotos/', '"../fotos/').replace('\\/fotos\\/', '..\\/fotos\\/')
p = p.replace('href="/panel/logout"', 'href="../"')
panel_shim = SHARED + r"""<style>#pinGate{position:fixed;inset:0;z-index:99999;background:#2B3A2E;display:flex;align-items:center;justify-content:center;font-family:system-ui}
#pinGate form{background:#F4F5F0;border-radius:16px;padding:30px 28px;width:min(360px,92vw);text-align:center}
#pinGate img{height:80px;margin-bottom:8px}#pinGate input{width:100%;font-size:22px;letter-spacing:.4em;text-align:center;padding:12px;border:1px solid #ccd;border-radius:10px;margin:14px 0 10px;box-sizing:border-box}
#pinGate button{width:100%;padding:12px;border:0;border-radius:10px;background:#2B3A2E;color:#fff;font-weight:600;font-size:15px;cursor:pointer}#pinGate p{margin:6px 0;color:#555;font-size:14px}</style>
<div id="pinGate"><form onsubmit="if(this.pin.value==='1234'){try{sessionStorage.setItem('ari_pin','1')}catch(e){};document.getElementById('pinGate').remove();}else{this.querySelector('.e').textContent='PIN incorrecto';}return false;">
<img src="../logo.png" alt="Arimune"><p><b>Panel de gestión · Hotel Arimune</b></p><p>Demostración · PIN 1234</p>
<input name="pin" type="password" inputmode="numeric" maxlength="4" autofocus placeholder="····"><button>Entrar</button><p class="e" style="color:#A6543E"></p><p><a href="../" style="color:#5F6E52">← Volver a la web</a></p></form></div>
<script>try{if(sessionStorage.getItem('ari_pin'))document.getElementById('pinGate').remove();}catch(e){}
(function(){var of=window.fetch;window.fetch=function(u,o){u=String(u);
 if(u.indexOf('/api/')===0){var d={};try{d=JSON.parse(o&&o.body||'{}');}catch(e){}
  if(u==='/api/panel/rooms'&&window.PANEL_REF){var st=ARI_DEMO.get('states',{});PANEL_REF.rooms.forEach(function(r){if(d.states&&r.rid in d.states)st[r.id]=!!d.states[r.rid];});ARI_DEMO.set('states',st);}
  if(u==='/api/panel/booking'){var L=ARI_DEMO.get('bookings',[]);L.push({room:d.room,name:d.name||'Reserva',in:d.in,out:d.out,guests:+d.guests||2,ch:d.ch||'Directa'});ARI_DEMO.set('bookings',L);}
  return Promise.resolve(new Response(JSON.stringify({ok:true,demo:true,synced:0,events:0}),{headers:{'content-type':'application/json'}}));}
 return of.apply(this,arguments);};})();
</script>
"""
merge = r"""
window.PANEL_REF=PANEL;(function(){try{var st=ARI_DEMO.get('states',{});PANEL.rooms.forEach(function(r){if(r.id in st)r.active=st[r.id];});
 var rate={};PANEL.rooms.forEach(function(r){rate[r.id]=Math.round((r.rate||0)*0.9);});
 ARI_DEMO.get('bookings',[]).forEach(function(b){PANEL.bookings.push({room:b.room,name:b.name,email:b.email||'',phone:b.phone||'',nif:b.nif||'',lang:b.lang||'es',consent:!!b.consent,in:b.in,out:b.out,guests:b.guests||2,ch:b.ch||'Directa',mp:false,rate:rate[b.room]||0});});}catch(e){}})();
"""
p = re.sub(r"(const PANEL=\{.*?\});\n", lambda m: m.group(1) + ";" + merge, p, 1, re.S)
assert "PANEL_REF" in p
p = p.replace("<body>", "<body>" + panel_shim, 1)
os.makedirs(os.path.join(DST, "panel"), exist_ok=True)
open(os.path.join(DST, "panel", "index.html"), "w", encoding="utf-8").write(p)

# ---------- Ficheros ----------
pub = os.path.join(ROOT, "public")
for f in ["logo.png", "logo-blanco.png", "favicon.jpg", "robots.txt"]:
    shutil.copy(os.path.join(pub, f), os.path.join(DST, f))
shutil.rmtree(os.path.join(DST, "fotos"), ignore_errors=True)
shutil.copytree(os.path.join(pub, "fotos"), os.path.join(DST, "fotos"))
open(os.path.join(DST, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
print("ok", DST)
