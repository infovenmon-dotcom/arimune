/**
 * Envío de email transaccional. Usa Brevo si BREVO_API_KEY está configurada;
 * si no, no envía (modo demo) y no rompe el flujo de reserva.
 * Remitente configurable con EMAIL_FROM (por defecto hotel@arimune.es).
 */
const FROM_EMAIL = process.env.EMAIL_FROM || 'hotel@arimune.es';
const FROM_NAME = process.env.EMAIL_FROM_NAME || 'Arimune';

export async function sendEmail(opts: { to: string; name?: string; subject: string; html: string }): Promise<{ ok: boolean; skipped?: boolean }> {
  const key = process.env.BREVO_API_KEY;
  if (!key || !opts.to) return { ok: false, skipped: true }; // sin proveedor → no se envía
  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: { 'api-key': key, 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({
        sender: { email: FROM_EMAIL, name: FROM_NAME },
        to: [{ email: opts.to, name: opts.name || undefined }],
        subject: opts.subject,
        htmlContent: opts.html,
      }),
    });
    return { ok: res.ok };
  } catch {
    return { ok: false };
  }
}

// Textos por idioma (fallback a ES). EU = euskera.
const T: Record<string, Record<string, string>> = {
  es: { sub: 'Confirmación de tu reserva · Arimune', hi: 'Hola', thanks: '¡Gracias por reservar en Arimune!', your: 'Tu reserva', room: 'Habitación', cin: 'Entrada', cout: 'Salida', nights: 'Noches', total: 'Total', foot: 'Te esperamos en Bakio. Cualquier duda, responde a este email.', bye: 'Un saludo,' },
  en: { sub: 'Your booking confirmation · Arimune', hi: 'Hi', thanks: 'Thanks for booking at Arimune!', your: 'Your booking', room: 'Room', cin: 'Check-in', cout: 'Check-out', nights: 'Nights', total: 'Total', foot: 'We look forward to seeing you in Bakio. Any questions, just reply to this email.', bye: 'Best,' },
  fr: { sub: 'Confirmation de votre réservation · Arimune', hi: 'Bonjour', thanks: 'Merci d’avoir réservé chez Arimune !', your: 'Votre réservation', room: 'Chambre', cin: 'Arrivée', cout: 'Départ', nights: 'Nuits', total: 'Total', foot: 'À bientôt à Bakio. Pour toute question, répondez à cet email.', bye: 'Cordialement,' },
  de: { sub: 'Bestätigung deiner Buchung · Arimune', hi: 'Hallo', thanks: 'Danke für deine Buchung bei Arimune!', your: 'Deine Buchung', room: 'Zimmer', cin: 'Anreise', cout: 'Abreise', nights: 'Nächte', total: 'Gesamt', foot: 'Wir freuen uns auf dich in Bakio. Bei Fragen einfach auf diese E-Mail antworten.', bye: 'Herzliche Grüße,' },
  it: { sub: 'Conferma della tua prenotazione · Arimune', hi: 'Ciao', thanks: 'Grazie per aver prenotato a Arimune!', your: 'La tua prenotazione', room: 'Camera', cin: 'Check-in', cout: 'Check-out', nights: 'Notti', total: 'Totale', foot: 'Ti aspettiamo a Bakio. Per qualsiasi domanda, rispondi a questa email.', bye: 'Un saluto,' },
  eu: { sub: 'Zure erreserbaren baieztapena · Arimune', hi: 'Kaixo', thanks: 'Eskerrik asko Arimunen erreserbatzeagatik!', your: 'Zure erreserba', room: 'Gela', cin: 'Sarrera', cout: 'Irteera', nights: 'Gauak', total: 'Guztira', foot: 'Bakion zain zaitugu. Zalantzarik baduzu, erantzun email honi.', bye: 'Agur bero bat,' },
};

export function bookingEmail(
  lang: string,
  b: { name?: string; room: string; in: string; out: string; nights: number; total: number }
): { subject: string; html: string } {
  const t = T[(lang || 'es').slice(0, 2).toLowerCase()] || T.es;
  const euro = (n: number) => n.toLocaleString('es-ES') + ' €';
  const fecha = (s: string) => s.split('-').reverse().join('/');
  const row = (k: string, v: string) =>
    `<tr><td style="padding:6px 0;color:#5b5f54">${k}</td><td style="padding:6px 0;text-align:right;font-weight:600">${v}</td></tr>`;
  const html = `<div style="font-family:system-ui,Arial,sans-serif;max-width:520px;margin:auto;color:#1E211B">
    <div style="background:#2B3A2E;color:#F4F5F0;padding:22px;border-radius:14px 14px 0 0">
      <div style="font-family:Georgia,serif;font-size:24px">arimune</div>
      <div style="font-size:12px;color:#BFC7B4;letter-spacing:.1em;text-transform:uppercase">Bakio · Bizkaia</div>
    </div>
    <div style="border:1px solid #E2E5DA;border-top:0;border-radius:0 0 14px 14px;padding:22px">
      <p>${t.hi} ${b.name || ''},</p>
      <p style="font-size:18px;font-family:Georgia,serif;color:#2B3A2E">${t.thanks}</p>
      <table style="width:100%;border-collapse:collapse;margin:14px 0;font-size:14px">
        <tr><td colspan="2" style="border-bottom:1px solid #E2E5DA;padding-bottom:6px;color:#5F6E52;font-weight:600">${t.your}</td></tr>
        ${row(t.room, b.room)}
        ${row(t.cin, fecha(b.in))}
        ${row(t.cout, fecha(b.out))}
        ${row(t.nights, String(b.nights))}
        ${row(t.total, euro(b.total))}
      </table>
      <p style="font-size:13px;color:#5b5f54">${t.foot}</p>
      <p style="font-size:13px;color:#5b5f54">${t.bye}<br><b>Arimune</b></p>
    </div>
  </div>`;
  return { subject: t.sub, html };
}
