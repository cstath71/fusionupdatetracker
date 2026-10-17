-- Returns the Resend settings for fut-subscribe from Supabase Vault.
-- SECURITY DEFINER so it can read vault.decrypted_secrets; callable only by service_role (the edge function's server-side client).
-- welcome_enabled: 'true' only if the vault secret fut_welcome_enabled is set to 'true' (default off).
create or replace function public.fut_resend_config()
returns table (api_key text, segment_id text, welcome_enabled boolean)
language sql
security definer
set search_path = ''
stable
as $$
  select
    (select decrypted_secret from vault.decrypted_secrets where name = 'fut_resend_api_key' limit 1),
    (select decrypted_secret from vault.decrypted_secrets where name = 'fut_resend_segment_id' limit 1),
    coalesce((select decrypted_secret = 'true' from vault.decrypted_secrets where name = 'fut_welcome_enabled' limit 1), false);
$$;
revoke all on function public.fut_resend_config() from public;
revoke all on function public.fut_resend_config() from anon, authenticated;
grant execute on function public.fut_resend_config() to service_role;
