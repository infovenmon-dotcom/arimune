# Arimune — Traspaso a Claude Code
### Resumen del proyecto + estado de la adaptación desde Kirana

> **Qué es esto.** El documento maestro del proyecto Arimune. La web y el panel
> se han construido **adaptando el codebase de producción de Kirana**
> (`alojamientohotel-rural`): misma arquitectura (Astro SSR + panel de gestión),
> con la marca, el contacto, las habitaciones y el posicionamiento portados a
> Arimune. Idioma de trabajo: español.

---

## 1. El proyecto en una frase

**Arimune** es un **hotel boutique junto al mar** en **Bakio** (Bizkaia), en
primera línea de la playa, a un paso de **San Juan de Gaztelugatxe**. Es una
**casona de 1929 restaurada** (arquitectura vasco-francesa), con **restaurante**,
cafetería/lounge, **dos terrazas** (una con vistas al mar, otra bajo árboles
centenarios) y jardín. Hotel con encanto, sostenible, con **desayuno casero**
muy valorado. Marca: madera, luz natural, calma y buena mesa.

---

## 2. Datos verificados (fuentes públicas, jul. 2026)

- **Dirección:** Bentako Plaza 1, 48130 **Bakio** (Bizkaia).
- **Teléfono:** +34 946 194 022.
- **Web:** https://arimune.es (ES + EN).
- **Categoría:** hotel boutique 3★. ~10–16 habitaciones (aquí se modela un
  conjunto de 10, como Kirana).
- **Tipos de habitación reales:** Doble Deluxe · Doble Deluxe Superior · Doble
  Deluxe Vistas Mar (algunas 2–3 pax). Zona reservada solo para adultos.
- **Servicios:** restaurante, cafetería/lounge bar, dos terrazas, jardín,
  desayuno, WiFi, TV, calefacción, minibar, caja fuerte, baño privado con
  secador, vistas al mar o a la montaña. Hotel sostenible.
- **Entorno:** playa de Bakio (surf, txakoli — Doniene Gorrondona), San Juan de
  Gaztelugatxe, iglesia gótica de Santa María, cabo Matxitxako, Bermeo, Bilbao.

> ⚠️ **A confirmar con el hotel:** nombres/categorías y precios definitivos por
> habitación, nº de habitaciones exacto, WhatsApp de reservas, email profesional
> (se ha usado `info@arimune.es` como marcador), nº de Registro de Turismo de
> Euskadi, régimen y precio de desayuno/media pensión.

> El email `nuss@uxper.co` que aparece en algunos agregadores es un **placeholder
> de la plantilla WordPress** (Uxper), no un contacto real.

---

## 3. Modelo de datos — las habitaciones (`src/data/rooms.json`)

Fuente ÚNICA. La web pública solo muestra las `activa:true`; el panel activa/
bloquea y se refleja en vivo. Se ha dado **nombre propio en euskera** a cada
habitación (temática mar/Bakio) manteniendo el patrón narrativo de Kirana, y se
han asignado las **categorías reales** de Arimune. **6 activas + 4 bloqueadas.**

| Nombre | Significado | Concepto | Tipo | Precio* | Estado |
|---|---|---|---|---|---|
| Itsaso | el mar | Frente al mar | Doble Deluxe Vistas Mar | 115 € | Activa |
| Hondartza | la playa | Sobre la arena | Doble Deluxe Vistas Mar | 110 € | Activa |
| Eguzki | el sol | Bajo el sol | Doble Deluxe | 98 € | Activa |
| Uhin | la ola | Con las olas | Doble Deluxe | 95 € | Activa |
| Haize | la brisa | Con la brisa marina | Doble Deluxe Superior | 105 € | Activa |
| Izar | la estrella | Bajo las estrellas | Doble Deluxe Superior | 105 € | Activa |
| Ilargi | la luna | A la luz de la luna | Doble Deluxe Vistas Mar | 118 € | Bloqueada |
| Mahasti | el viñedo | Entre viñas de txakoli | Doble Deluxe | 98 € | Bloqueada |
| Itsaslabar | el acantilado | Sobre el acantilado | Doble Deluxe Superior Vistas Mar | 135 € | Bloqueada |
| Gaztelu | el castillo | Camino a Gaztelugatxe | Suite | 155 € | Bloqueada |

*Precios, m² y camas **orientativos** → confirmar con el hotel.

---

## 4. Qué se ha portado desde Kirana

- **Arquitectura completa**: Astro SSR (`output: 'server'`), web pública en
  `src/home.html` (maqueta autocontenida, i18n en cliente), panel en `/panel`
  (`panel-markup.html` + `panel-app.js` + `panel.css`), APIs (`/api/*`),
  persistencia de `rooms.json` (`roomsStore.ts`, stand-in de fichero → BD).
- **Marca y contacto** sustituidos globalmente: nombre, dominio, teléfono,
  dirección, email, worker de Cloudflare (`name = "arimune"`).
- **`rooms.json`** reescrito con las habitaciones de Arimune (§3).
- **Posicionamiento** reescrito de "alojamiento rural solo adultos / Urdaibai" a
  "hotel boutique junto al mar / Bakio" en el hero, la idea, habitaciones, footer
  y metadatos (`src/home.html`).

---

## 5. Pendiente (lo que NO se ha podido completar aquí)

1. **Fotos reales de Arimune.** No se pudieron descargar de arimune.es: la
   política de red del entorno bloquea el dominio (HTTP 403 en el proxy).
   `src/home.html` lleva **las fotos de Kirana embebidas en base64** por toda la
   página (hero, galería, "la casa"…) y `rooms.json` tiene `fotos:[]`, por lo que
   las tarjetas usan también un placeholder heredado. **Acción:** descargar las
   imágenes de arimune.es (o pedírselas al hotel), colocarlas en
   `public/fotos/…` y en los bloques base64 de `home.html`, y referenciarlas en
   `rooms.json → fotos[]`.
2. **Contenido de Entorno/Actividades.** Sigue describiendo Urdaibai/Bermeo de
   Kirana (geográficamente contiguo, Bakio está en la puerta oeste de la Reserva
   de Urdaibai). Revisar para Bakio: Gaztelugatxe, txakoli, cabo Matxitxako,
   surf, Bermeo, Mundaka.
3. **i18n.** El diccionario `I18N` embebido (8 idiomas) mantiene el copy antiguo;
   las cadenas nuevas de Arimune caen a ES en los demás idiomas (fallback).
   Traducir; el euskera, por traductor nativo.
4. **Producción:** reservas reales + pasarela de pago (Stripe), channel manager
   (iCal Booking/Expedia), facturación, SEO/hreflang/RGPD y deploy con dominio
   canónico. Igual que el roadmap de Kirana (Fases 4–7).

---

## 6. Tokens de diseño (heredados de la maqueta)

```
--paper:#F2F3EE; --paper-2:#E7E9E0; --ink:#1E211B; --pine:#2B3A2E;
--moss:#5F6E52; --oak:#B49A72; --mist:#6C7065;
--serif:"Cormorant Garamond", Georgia, serif;
--sans:"Hanken Grotesk", system-ui, sans-serif;
```

> Paleta cálida y natural que encaja con una casona junto al mar. Se puede
> ajustar a la identidad visual real de Arimune cuando se disponga de ella.

---

*Arimune · hotel boutique junto al mar · Bakio (Bizkaia). El mar, la calma y la
buena mesa.*
