# Arimune

Web de producción + panel de gestión para **Arimune**, **hotel boutique junto
al mar** en primera línea de playa en **Bakio** (Bizkaia), a un paso de San Juan
de Gaztelugatxe. Casona de 1929 restaurada, con restaurante, terrazas y vistas
al mar. Marca: madera, luz natural, calma, encanto. Idea: *el mar, la calma y la
buena mesa.*

> Proyecto adaptado del codebase de producción de **Kirana**
> (`alojamientohotel-rural`): misma arquitectura Astro + panel, con el contenido,
> la marca y los datos portados a Arimune. Documento de traspaso en
> `referencia/arimune-traspaso-claude-code.md`.

## Stack

Astro (SSR, `output: 'server'`) + Tailwind CSS v4 · multi-idioma con routing por
locale (hreflang pendiente, Fase 7) · PostgreSQL (Fase 3+, hoy persistencia de
fichero) · Stripe (Fase 4) · channel manager vía iCal (Fase 5) · deploy
Cloudflare Workers / Vercel / Netlify / Node.

> SSR: la web pública y el panel leen `rooms.json` en cada petición, de modo
> que bloquear/activar una habitación en el panel se refleja **en vivo** en la
> web (regla #2). La persistencia es de fichero como stand-in; se sustituye por
> la BD cambiando solo `src/lib/roomsStore.ts`.

## Estado

- [x] Scaffold Astro + Tailwind + tokens de marca
- [x] `src/data/rooms.json` — fuente única de las 10 habitaciones (nombres,
      categorías, precios orientativos → **confirmar con el hotel**)
- [x] **Web pública** (`src/home.html`, SSR): Hero · La casa · La idea ·
      Habitaciones (solo activas, con specs/servicios, inyectadas desde
      `rooms.json`) · Servicios · Entorno · Actividades · Opiniones · Ofertas ·
      Reserva. Posicionamiento reescrito a hotel boutique junto al mar.
- [x] Contacto real portado: Bentako Plaza 1, Bakio (Bizkaia) 48130 ·
      +34 946 194 022 · info@arimune.es · arimune.es
- [x] **Panel de gestión** (`/panel`): login por contraseña + middleware ·
      **Habitaciones** bloquear/activar que persiste y se refleja en la web en
      vivo (regla #2) · Reservas · Ingresos · Facturas · Contabilidad
- [ ] **Fotos reales de Arimune** — PENDIENTE. No se pudieron descargar de
      arimune.es (bloqueado por la política de red del entorno). La maqueta
      muestra las fotos heredadas de Kirana como *placeholder*; sustituir por
      las de Arimune (ver traspaso, §Fotos).
- [ ] i18n: el diccionario embebido y algunas cadenas nuevas de Arimune caen a
      ES en los otros idiomas; revisar/traducir (EU por traductor nativo).
- [ ] Contenido de **Entorno/Actividades** aún describe Urdaibai/Kirana; revisar
      para Bakio (Gaztelugatxe, txakoli, cabo Matxitxako, surf…).
- [ ] Reservas reales + Stripe (Fase 4) · Channel manager iCal (Fase 5) ·
      Facturación (Fase 6) · SEO/hreflang/RGPD/deploy (Fase 7)

## Reglas clave

1. `src/data/rooms.json` es la **fuente única** de las 10 habitaciones.
2. La web pública **solo muestra habitaciones activas** (`activa: true`).
3. **No reimplementar a mano** la facturación ni la sincronización con OTAs
   (usar software homologado / channel manager).
4. Tono de marca: **hotel boutique junto al mar** — calma, encanto, buena mesa.
5. Claves en `.env` (ver `.env.example`), **nunca** en el código.

## Desarrollo local

```bash
npm install
cp .env.example .env           # define PANEL_PASSWORD
npm run dev                    # http://localhost:4321

# Producción (SSR Node, ejecutar desde la raíz del proyecto):
npm run build:node             # genera dist/ (servidor Node)
PANEL_PASSWORD=… node ./dist/server/entry.mjs
```

El panel de gestión está en **`/panel`** (protegido por `PANEL_PASSWORD`).

## Estructura

```
referencia/                # briefing maestro (SOLO LECTURA)
src/
├── home.html              # web pública (maqueta autocontenida, SSR)
├── data/
│   ├── rooms.json         # fuente única de las 10 habitaciones
│   └── panel-sample.json  # datos de ejemplo del panel (reservas/facturas/gastos)
├── i18n/                  # diccionario (clave = texto ES → 8 idiomas)
├── lib/
│   ├── rooms.ts           # tipos + helpers
│   ├── roomsStore.ts      # lectura/escritura de rooms.json (→ BD en prod)
│   ├── panel-app.js       # lógica del panel (cliente)
│   └── auth.ts            # login del panel por contraseña (stand-in)
├── middleware.ts          # protege /panel y /api
├── styles/global.css      # tokens de marca (Tailwind v4 @theme)
└── pages/
    ├── index.astro · [lang]/index.astro     # web pública (SSR)
    ├── api/…                                # rooms, checkout, ical, panel…
    └── panel/                               # reservas, ingresos, habitaciones,
                                             # facturas, contabilidad, login
```

## Datos pendientes de confirmar con el hotel

Fotos reales · nombres/categorías y precios definitivos de las habitaciones ·
nº de Registro de Turismo de Euskadi · WhatsApp de reservas · email profesional
(hoy `info@arimune.es`) · régimen y precio del desayuno/media pensión ·
channel manager · dominio y traducciones (EU por traductor nativo).
