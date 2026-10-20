-- Private read-out of the Fusion Updates counters (run in the Supabase SQL editor or via the Supabase connector).
-- Days are UTC. Change the interval to widen the window.

-- 1. Views per day
select day, sum(views) as views from public.fut_page_views where day >= current_date - interval '28 days' group by day order by day desc;

-- 2. Top pages
select path, sum(views) as views from public.fut_page_views where day >= current_date - interval '28 days' group by path order by views desc limit 30;

-- 3. Where visitors came from (referrer domain; '' = direct, bookmarks, or browsers that send no referrer)
select ref_domain, sum(views) as views from public.fut_page_views where day >= current_date - interval '28 days' group by ref_domain order by views desc;

-- 4. Tagged links (utm_source / utm_medium / utm_campaign)
select utm_source, utm_medium, utm_campaign, sum(views) as views from public.fut_page_views
where day >= current_date - interval '28 days' and (utm_source <> '' or utm_medium <> '' or utm_campaign <> '')
group by 1,2,3 order by views desc;

-- 5. Honeypot drops on the signup function (bots, or browsers autofilling the hidden field)
select day, drops from public.fut_honeypot_drops order by day desc limit 28;
