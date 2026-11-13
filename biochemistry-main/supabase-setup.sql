-- Run in the Supabase SQL Editor after creating your project.
-- This allows anonymous READ but only approved admins can WRITE.
create table if not exists public.club_site_content (
  id integer primary key default 1 check (id=1),
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);
create table if not exists public.club_admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);
alter table public.club_site_content enable row level security;
alter table public.club_admins enable row level security;

grant usage on schema public to anon, authenticated;
grant select on public.club_site_content to anon, authenticated;
grant update (data,updated_at) on public.club_site_content to authenticated;
grant select on public.club_admins to authenticated;

create or replace function public.is_club_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists(select 1 from public.club_admins where user_id = (select auth.uid()));
$$;
revoke all on function public.is_club_admin() from public, anon;
grant execute on function public.is_club_admin() to authenticated;

create policy "Site content is public" on public.club_site_content
for select to anon, authenticated using (true);
create policy "Only club admins can edit" on public.club_site_content
for update to authenticated using ((select public.is_club_admin()))
with check ((select public.is_club_admin()));
create policy "Admins may see only their own approval" on public.club_admins
for select to authenticated using (user_id = (select auth.uid()));

insert into public.club_site_content(id,data) values (1,'{}'::jsonb)
on conflict(id) do nothing;
-- NEXT, create an admin user in Supabase Authentication > Users, then run:
-- insert into public.club_admins(user_id) values ('YOUR-AUTH-USER-UUID');
-- Never put a Supabase service_role key in browser JavaScript.
