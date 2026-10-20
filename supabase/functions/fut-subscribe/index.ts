import { createClient } from "npm:@supabase/supabase-js@2";

// Public signup endpoint for FusionUpdateTracker. No secrets in the client.
const ALLOWED = ["https://fusionupdates.com", "https://www.fusionupdates.com", "https://cstath71.github.io", "http://localhost:4321"];
const AREAS = ["All modules", "Financials", "Procurement", "Supply Chain & Manufacturing", "Logistics", "Project Management", "HCM"];
const EMAIL_RE = /^[^\s@<>()\[\],;:"]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$/;
const MAX_PER_HOUR = 5;

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return { "Access-Control-Allow-Origin": o, "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "content-type", "Vary": "Origin" };
}
const json = (b: unknown, s: number, h: Record<string, string>) => new Response(JSON.stringify(b), { status: s, headers: { ...h, "Content-Type": "application/json" } });

async function sha256(s: string) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  const h = cors(origin);
  if (req.method === "OPTIONS") return new Response("ok", { headers: h });
  if (req.method !== "POST") return json({ ok: false, error: "method" }, 405, h);
  if (origin && !ALLOWED.includes(origin)) return json({ ok: false, error: "origin" }, 403, h);

  let body: Record<string, unknown> = {};
  try {
    const ct = req.headers.get("content-type") || "";
    if (ct.includes("application/json")) body = await req.json();
    else body = Object.fromEntries((await req.formData()).entries());
  } catch { return json({ ok: false, error: "bad_request" }, 400, h); }

  // Honeypot: real users never fill the hidden 'website' field. Pretend success, and add 1 to today's drop count
  // (public.fut_honeypot_drops holds a number per day only: no email, IP or field contents).
  if (String(body.website ?? "").trim() !== "") {
    try {
      const sbh = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
      await sbh.rpc("fut_count_honeypot");
    } catch { /* counting is best effort */ }
    return json({ ok: true }, 200, h);
  }

  const email = String(body.email ?? "").trim().toLowerCase();
  if (email.length > 254 || !EMAIL_RE.test(email)) return json({ ok: false, error: "invalid_email" }, 400, h);
  const area = AREAS.includes(String(body.area)) ? String(body.area) : "All modules";

  const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
  const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "unknown";
  const ipHash = await sha256("fut:" + ip);

  // Rate limit: max MAX_PER_HOUR attempts per IP per hour.
  const since = new Date(Date.now() - 3600_000).toISOString();
  const { count } = await sb.from("fut_signup_attempts").select("id", { count: "exact", head: true }).eq("ip_hash", ipHash).gte("created_at", since);
  if ((count ?? 0) >= MAX_PER_HOUR) return json({ ok: false, error: "rate_limited" }, 429, h);
  await sb.from("fut_signup_attempts").insert({ ip_hash: ipHash });

  const { error } = await sb.from("fut_subscribers").upsert({ email, area, ip_hash: ipHash, unsubscribed_at: null }, { onConflict: "email" });
  if (error) return json({ ok: false, error: "store_failed" }, 500, h);

  // Mirror into the Resend segment. Settings come from function secrets (RESEND_API_KEY, RESEND_SEGMENT_ID) if set,
  // otherwise from Supabase Vault via public.fut_resend_config() (executable by service_role only).
  let key = Deno.env.get("RESEND_API_KEY");
  let seg = Deno.env.get("RESEND_SEGMENT_ID");
  let welcome = false;
  try {
    const { data } = await sb.rpc("fut_resend_config");
    const cfg = Array.isArray(data) ? data[0] : data;
    key = key || cfg?.api_key || undefined;
    seg = seg || cfg?.segment_id || undefined;
    welcome = cfg?.welcome_enabled === true;
  } catch { /* no vault config */ }
  if (key && seg) {
    try {
      const auth = { Authorization: `Bearer ${key}`, "Content-Type": "application/json" };
      // Existing contact: add it to the segment without touching its global subscription status. No welcome.
      let r = await fetch(`https://api.resend.com/contacts/${encodeURIComponent(email)}/segments/${seg}`, { method: "POST", headers: auth });
      let created: string | null = null;
      if (r.status === 404) {
        // Not a contact yet: create it directly in the segment.
        r = await fetch("https://api.resend.com/contacts", { method: "POST", headers: auth, body: JSON.stringify({ email, unsubscribed: false, segments: [{ id: seg }] }) });
        if (r.ok) created = (await r.clone().json().catch(() => ({})))?.id ?? null;
      }
      // Welcome (event fut.subscribed -> automation "Fusion Updates welcome"): only for newly created contacts,
      // only when vault secret fut_welcome_enabled = 'true', never for reserved test domains.
      const testDomain = /@(example\.(com|net|org)|[^@]+\.(test|example|invalid|localhost))$/i.test(email);
      if (created && welcome && !testDomain) {
        await fetch("https://api.resend.com/events/send", { method: "POST", headers: auth, body: JSON.stringify({ event: "fut.subscribed", contact_id: created }) }).catch(() => {});
      }
      if (r.ok) await sb.from("fut_subscribers").update({ synced_to_resend_at: new Date().toISOString() }).eq("email", email);
    } catch { /* keep the Supabase row; sync later */ }
  }
  return json({ ok: true }, 200, h);
});
