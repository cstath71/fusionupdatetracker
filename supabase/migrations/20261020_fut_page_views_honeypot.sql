-- Fusion Updates: cookie-free page-view counter and honeypot drop counter.
-- Separate fut_ tables (the project also hosts ShopBot Index's sbi_ tables).
-- Only daily totals are stored: page path, referrer domain, UTM tags and day. No IPs, no cookies, no identifiers.
create table if not exists public.fut_page_views (
  day date not null,
  path text not null,
  ref_domain text not null default '',
  utm_source text not null default '',
  utm_medium text not null default '',
  utm_campaign text not null default '',
  views integer not null default 0,
  primary key (day, path, ref_domain, utm_source, utm_medium, utm_campaign)
);
alter table public.fut_page_views enable row level security;  -- no policies: only service_role can read or write
revoke all on public.fut_page_views from anon, authenticated;

-- Honeypot drops on fut-subscribe: a count per day, nothing else.
create table if not exists public.fut_honeypot_drops (
  day date primary key,
  drops integer not null default 0
);
alter table public.fut_honeypot_drops enable row level security;
revoke all on public.fut_honeypot_drops from anon, authenticated;

create or replace function public.fut_count_view(p_path text, p_ref text, p_us text, p_um text, p_uc text)
returns void language sql security definer set search_path = '' as $$
  insert into public.fut_page_views as v (day, path, ref_domain, utm_source, utm_medium, utm_campaign, views)
  values ((now() at time zone 'utc')::date, left(p_path,200), left(coalesce(p_ref,''),100), left(coalesce(p_us,''),64), left(coalesce(p_um,''),64), left(coalesce(p_uc,''),64), 1)
  on conflict (day, path, ref_domain, utm_source, utm_medium, utm_campaign) do update set views = v.views + 1;
$$;
create or replace function public.fut_count_honeypot()
returns void language sql security definer set search_path = '' as $$
  insert into public.fut_honeypot_drops as h (day, drops) values ((now() at time zone 'utc')::date, 1)
  on conflict (day) do update set drops = h.drops + 1;
$$;
revoke all on function public.fut_count_view(text,text,text,text,text) from public, anon, authenticated;
revoke all on function public.fut_count_honeypot() from public, anon, authenticated;
grant execute on function public.fut_count_view(text,text,text,text,text) to service_role;
grant execute on function public.fut_count_honeypot() to service_role;
