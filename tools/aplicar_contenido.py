#!/usr/bin/env python3
"""Aplica a src/home.html el contenido REAL de Arimune (21/11/2026): textos de arimune.es, fotos reales,
16 habitaciones, Bakio en vez de Urdaibai, sin precios inventados. Idempotente sobre el original (git)."""
import re, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "src", "home.html")
h = open(P, encoding="utf-8").read()
new = open(os.path.join(ROOT, "tools", "contenido_bakio.html"), encoding="utf-8").read()

def rep(old, new_, count=1, must=True):
    global h
    if old not in h:
        if must: raise SystemExit("no encuentro: " + old[:80])
        return
    h = h.replace(old, new_, count)

# 1) Cabecera, SEO e intro
h = re.sub(r"<title>.*?</title>", "<title>Hotel Arimune · Hotel boutique a pie de playa en Bakio</title>", h, 1, re.S)
h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Hotel Arimune, hotel boutique familiar desde 1929 a escasos metros de la playa de Bakio (Bizkaia) y a 2 km a pie de San Juan de Gaztelugatxe. 16 habitaciones, muchas con vistas al mar.">', h, 1)
rep('data-i18n="i_t1">un refugio de paz,</span>', '>dormir con el mar,</span>')
rep('data-i18n="i_t2">cerca de todo.</span>', '>en Bakio desde 1929.</span>')
h = h.replace('alt="Arimune Alojamiento Rural"', 'alt="Hotel Arimune"')

# 2) Cuerpo: de HERO a FOOTER
a = h.index("<!-- HERO -->"); b = h.index("<!-- FOOTER -->")
extra_css = """<style>
.room-filter{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}
.room-filter button{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:8px 15px;font:600 .8rem var(--sans);cursor:pointer}
.room-filter button.on{background:var(--pine);color:#fff;border-color:var(--pine)}
.room .ph{position:relative;cursor:zoom-in}
.room .ph .nph{position:absolute;right:10px;bottom:10px;background:rgba(0,0,0,.6);color:#fff;font:600 .72rem var(--sans);padding:5px 9px;border-radius:999px}
.ent-fiestas{display:grid;gap:6px;margin:28px 0 0;padding:18px 22px;border-left:3px solid var(--oak);background:var(--paper-2,#f3f1ea);border-radius:0 10px 10px 0}
.ent-fiestas p{margin:0;font-size:.95rem}
.lbx{position:fixed;inset:0;z-index:10000;background:rgba(10,12,10,.92);display:none;align-items:center;justify-content:center;flex-direction:column;gap:12px;padding:20px}
.lbx.open{display:flex}.lbx img{max-width:min(1100px,94vw);max-height:78vh;border-radius:10px;object-fit:contain}
.lbx .lb-t{color:#fff;font-family:var(--serif);font-size:1.4rem}.lbx .lb-n{color:#bbb;font-size:.8rem}
.lbx button{position:absolute;background:rgba(255,255,255,.12);color:#fff;border:0;border-radius:999px;width:46px;height:46px;font-size:1.4rem;cursor:pointer}
@media(max-width:700px){.places li{flex-direction:column;gap:3px}.places .pl-name{min-width:0}}
html,body{overflow-x:clip}
.lbx .lb-x{top:16px;right:16px}.lbx .lb-p{left:12px;top:50%}.lbx .lb-nx{right:12px;top:50%}
</style>
"""
h = h[:a] + extra_css + new + h[b:]

# 3) Pie
rep('mailto:info@arimune.es">info@arimune.es</a>', 'mailto:hotel@arimune.es">hotel@arimune.es</a>', count=5, must=False)
h = h.replace('info@arimune.es', 'hotel@arimune.es')
rep('<a href="https://wa.me/34946194022" target="_blank" rel="noopener">WhatsApp</a>', '<a href="https://arimune.es/blog/" target="_blank" rel="noopener">Blog del hotel</a>', must=False)
h = re.sub(r'<p class="foot-tag"[^>]*>.*?</p>', '<p class="foot-tag">Hotel boutique familiar desde 1929, a escasos metros de la playa de Bakio (Bizkaia) y a 2 km a pie de San Juan de Gaztelugatxe.</p>', h, 1, re.S)
h = h.replace("© 2026 Arimune · Hotel boutique junto al mar — maqueta de propuesta de rediseño", "© 2026 Hotel Arimune · Bentako plaza 1, 48130 Bakio · 946 19 40 22")
h = h.replace('<p>Bentako Plaza 1<br>Bakio (Bizkaia) 48130</p>', '<p>Bentako plaza 1<br>48130 Bakio (Bizkaia)</p>')
# Botón WhatsApp de la cabecera/barras → teléfono (el 946 19 40 22 es fijo)
h = h.replace('href="https://wa.me/34946194022"', 'href="tel:+34946194022"')

# 4) Tarjetas de habitación: sin precios, con filtro y galería de fotos
s = h.index("const RM=["); e = h.index("];", s) + 2
rooms = json.load(open(os.path.join(ROOT, "src", "data", "rooms.json")))["rooms"]
RM = [{"id": r["nombre"], "concept": r["concepto"], "cap": r["capacidad"], "m2": r["m2"], "bed": r["cama"], "kind": r["tipo"],
       "active": r["activa"], "story": r["storytelling"], "img": (r["fotos"] or [""])[0], "fotos": r["fotos"],
       "mar": r.get("vistas_mar", False), "terraza": "terraza" in r["tipo"], "adultos": r.get("solo_adultos", False)} for r in rooms]
h = h[:s] + "const RM=" + json.dumps(RM, ensure_ascii=False) + ";" + h[e:]
h = re.sub(r"  const IMG=\{[^\n]*\n", "", h, 1)
old_card = h[h.index("  function bathWord(r){"):h.index("  function renderRooms(lc){")]
new_card = r'''  function amenList(r){var a=['Baño con ducha','Calefacción por el suelo','Wi-Fi'];if(r.mar)a.unshift('Vistas al mar');if(r.terraza)a.unshift('Terraza privada');if(r.adultos)a.push('Solo adultos');return a;}
  function card(r,lc){
    var src=r.img||'';var nf=(r.fotos||[]).length;
    var amen=amenList(r).map(function(a){return '<li>'+t(a,lc)+'</li>';}).join('');
    return '<article class="room" data-mar="'+(r.mar?1:0)+'" data-terraza="'+(r.terraza?1:0)+'" data-adultos="'+(r.adultos?1:0)+'">'
      +'<div class="ph" data-gal="'+r.id+'"><img loading="lazy" src="'+src+'" alt="Habitación '+r.id+'">'+(nf>1?'<span class="nph">'+nf+' fotos</span>':'')+'</div>'
      +'<div class="room-body">'
      +'<p class="room-concept">'+t(r.concept,lc)+'</p>'
      +'<h3 class="name">'+r.id+'</h3>'
      +'<p>'+t(r.story,lc)+'</p>'
      +'<div class="rspecs"><span>'+(r.cap===1?'1 persona':(r.cap===3?'2 o 3 personas':'2 personas'))+' · '+r.m2+' m² · cama '+t(r.bed,lc)+'</span></div>'
      +'<ul class="amen">'+amen+'</ul>'
      +'<div class="meta"><span>'+t('Precio según fechas',lc)+'</span><a href="#reserva" class="kb-book" data-room="'+r.id+'">'+t('Reservar →',lc)+'</a></div>'
      +'</div></article>';
  }
'''
h = h.replace(old_card, new_card)
old_render = h[h.index("  function renderRooms(lc){"):h.index("  function init(){")]
new_render = r'''  var FILT='all';
  function renderRooms(lc){var g=document.getElementById('roomsGrid');if(!g)return;
    var AV=window.ARIMUNE_AVAIL||{};
    var byId={};RM.forEach(function(r){byId[r.id]=r;});
    var list=(AV.activeNames&&AV.activeNames.length)?AV.activeNames.map(function(n){return byId[n];}).filter(Boolean):RM.filter(function(r){return r.active;});
    if(FILT!=='all')list=list.filter(function(r){return r[FILT];});
    g.innerHTML=list.map(function(r){return card(r,lc);}).join('');
    Array.prototype.forEach.call(g.querySelectorAll('[data-gal]'),function(el){el.onclick=function(){openGal(byId[el.getAttribute('data-gal')]);};});}
  var LB,LBi=0,LBr=null;
  function openGal(r){if(!r||!(r.fotos||[]).length)return;LBr=r;LBi=0;
    if(!LB){LB=document.createElement('div');LB.className='lbx';LB.innerHTML='<button class="lb-x" aria-label="Cerrar">×</button><button class="lb-p" aria-label="Anterior">‹</button><img alt=""><div class="lb-t"></div><div class="lb-n"></div><button class="lb-nx" aria-label="Siguiente">›</button>';document.body.appendChild(LB);
      LB.querySelector('.lb-x').onclick=function(){LB.classList.remove('open');};LB.onclick=function(e){if(e.target===LB)LB.classList.remove('open');};
      LB.querySelector('.lb-p').onclick=function(){LBi=(LBi-1+LBr.fotos.length)%LBr.fotos.length;drawGal();};
      LB.querySelector('.lb-nx').onclick=function(){LBi=(LBi+1)%LBr.fotos.length;drawGal();};
      document.addEventListener('keydown',function(e){if(!LB.classList.contains('open'))return;if(e.key==='Escape')LB.classList.remove('open');if(e.key==='ArrowRight')LB.querySelector('.lb-nx').click();if(e.key==='ArrowLeft')LB.querySelector('.lb-p').click();});}
    drawGal();LB.classList.add('open');}
  function drawGal(){LB.querySelector('img').src=LBr.fotos[LBi];LB.querySelector('.lb-t').textContent=LBr.id+' · '+LBr.concept;LB.querySelector('.lb-n').textContent=(LBi+1)+' / '+LBr.fotos.length;}
  document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('#roomFilter button');if(!b)return;
    FILT=b.getAttribute('data-f');Array.prototype.forEach.call(document.querySelectorAll('#roomFilter button'),function(x){x.classList.toggle('on',x===b);});
    renderRooms((document.documentElement.lang||'es').slice(0,2));});
'''
h = h.replace(old_render, new_render)

# 5) Reserva (calendario): sin precios ni WhatsApp
names = [r["nombre"] for r in rooms]
h = re.sub(r"  var FB=\{activeNames:.*?\};\n  var AV=", "  var FB={activeNames:" + json.dumps(names, ensure_ascii=False) + ",booked:{}};\n  var AV=", h, 1, re.S)
h = re.sub(r"  var PRICE=\{[^\n]*\n", "  var PRICE={};\n", h, 1)
h = re.sub(r"  var ORDER=\[[^\n]*\n", "  var ORDER=" + json.dumps(names, ensure_ascii=False) + ";\n", h, 1)
h = h.replace("var RMETA={}; (AV.rooms||[]).forEach(function(r){RMETA[r.id]=r;});",
              "var RMETA={}; (AV.rooms||[]).forEach(function(r){RMETA[r.id]=r;}); (window.ARIMUNE_RM||[]).forEach(function(r){if(!RMETA[r.id])RMETA[r.id]=r;});")
h = h.replace("+' &middot; desde <b>'+tot+'&euro;</b></p>'+((rm.ota&&rm.ota>pr)?'<p style=\"margin:-6px 0 12px;font-size:.78rem;color:#5F6E52\">Precio web '+pr+'&euro;/noche &middot; un 10% menos que en plataformas.</p>':'');",
              "+'</p><p style=\"margin:-6px 0 12px;font-size:.8rem;color:#5F6E52\">El hotel te confirma el precio de esas fechas.</p>';")
h = h.replace("<span class=\"pr\">'+((m.ota&&m.ota>m.price)?'<s style=\"opacity:.5\">'+m.ota+'&euro;</s> ':'')+(m.price||PRICE[r]||'')+'&euro;/noche'+((m.ota&&m.ota>m.price)?' &middot; -10% web':'')+'</span>",
              "<span class=\"pr\">'+(m.concept||'')+'</span>")
h = h.replace("var specs=(m.cap?m.cap+' pers':'')+(m.m2?' · ≈'+m.m2+' m²':'')+' · '+bathWord(m);", "var specs=(m.cap?m.cap+' pers':'')+(m.m2?' · '+m.m2+' m²':'');")
h = h.replace("'<p style=\"margin:10px 0 0;text-align:center;font-size:.8rem\"><a href=\"'+waLink(ROOM,pax())+'\" target=\"_blank\" rel=\"noopener\" style=\"color:#5F6E52\">&iquest;Dudas? Escr&iacute;benos por WhatsApp</a></p>'",
              "'<p style=\"margin:10px 0 0;text-align:center;font-size:.8rem\"><a href=\"tel:+34946194022\" style=\"color:#5F6E52\">&iquest;Dudas? Llama al 946 19 40 22</a></p>'")
h = h.replace("<label class=\"kb-consent\"><input type=\"checkbox\" id=\"kbConsent\"> Quiero recibir ofertas y novedades de Arimune por email.</label>",
              "<label class=\"kb-consent\"><input type=\"checkbox\" id=\"kbConsent\"> Quiero recibir novedades del Hotel Arimune por email.</label>")
# El RM de la tarjeta también alimenta el calendario
h = h.replace("const RM=", "const RM=window.ARIMUNE_RM=", 1)

# 6) Idiomas: lo que no tenga traducción fija se traduce automáticamente
tr = r'''<script>
(function(){var base=window.applyLang,ORIG=new Map(),CACHE={};
function nodes(){var out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null,false),n;
 while(n=w.nextNode()){var p=n.parentElement;if(!p||p.closest('script,style,.kb-ov,.lang-menu,.langsel'))continue;var v=n.nodeValue;if(!/[A-Za-zÁÉÍÓÚáéíóúñÑ]{2}/.test(v))continue;if(!ORIG.has(n))ORIG.set(n,v);out.push(n);}return out;}
function gtx(list,l){var c=CACHE[l]=CACHE[l]||{};var need=list.filter(function(s){return !(s in c);});
 var chunks=[],cur=[],len=0;need.forEach(function(s){var e=encodeURIComponent(s).length+3;if(len+e>5000&&cur.length){chunks.push(cur);cur=[];len=0;}cur.push(s);len+=e;});if(cur.length)chunks.push(cur);
 return Promise.all(chunks.map(function(ch){return fetch('https://translate.googleapis.com/translate_a/t?client=gtx&sl=es&tl='+l+'&'+ch.map(function(s){return 'q='+encodeURIComponent(s);}).join('&')).then(function(r){return r.json();}).then(function(j){ch.forEach(function(s,i){var t=j[i];if(Array.isArray(t))t=t[0];if(typeof t==='string')c[s]=t;});}).catch(function(){});}));}
window.applyLang=function(code){if(base)base(code);var l=String(code).toLowerCase();if(l==='be')l='nl';if(l==='no')l='no';
 var ns=nodes();if(l==='es'){ns.forEach(function(n){n.nodeValue=ORIG.get(n);});return;}
 var keys=ns.map(function(n){return ORIG.get(n).trim();});
 gtx(keys,l).then(function(){var c=CACHE[l]||{};ns.forEach(function(n){var o=ORIG.get(n),k=o.trim();if(c[k])n.nodeValue=o.replace(k,c[k]);});});};
})();
</script>
'''
h = h.replace("</body>", tr + "</body>", 1)

# 7) Logo real de Arimune (arimune.es), barra superior, pie
h = re.sub(r'(<img class="intro-logo" src=")data:image/png;base64,[A-Za-z0-9+/=]+', r'\1/logo-blanco.png', h, 1)
h = re.sub(r'(<img class="logo-img" src=")data:image/png;base64,[A-Za-z0-9+/=]+', r'\1/logo.png', h, 1)
h = re.sub(r'(<img class="foot-logo" src=")data:image/png;base64,[A-Za-z0-9+/=]+', r'\1/logo-blanco.png', h, 1)
h = h.replace('<link rel="icon" type="image/png" href="/logo.png">', '<link rel="icon" type="image/jpeg" href="/favicon.jpg">')
h = h.replace('<span data-i18n="u_bar"><b>Mejor precio garantizado</b> reservando en esta web</span>', '<span><b>A pie de playa</b> en Bakio · desde 1929</span>')
h = h.replace('<a href="tel:+34946194022" target="_blank" rel="noopener">WhatsApp</a>', '<a href="https://arimune.es/blog/" target="_blank" rel="noopener">Blog del hotel</a>')
# 8) Sin «X personas mirando»: es un dato inventado
h = h.replace("<p class=\"kb-watch\" id=\"kbWatch\">", "<p class=\"kb-watch\" id=\"kbWatch\" style=\"display:none\">")

open(P, "w", encoding="utf-8").write(h)
print("ok", len(h))
