# Biochem Club — publishing and admin setup

This is a plain HTML/CSS/JS multi-page site. There is no school affiliation. Most meetings are on Thursdays unless you change them.

## Try the site on your computer

Unzip the folder and open `index.html`. All pages are separate `.html` files. `admin.html` works in **local/offline mode** without an account. You can edit text, announcements, meeting details, public contact email, and notes links; use **Save local preview** to test it on your browser, or **Download site-data.js** and replace the existing file in the site folder. You must then upload/redeploy the changed file for everyone else to see it.

## Recommended free hosting: Cloudflare Pages

1. Create a GitHub repository with the site files at its root and push them.
2. In Cloudflare, open Workers & Pages → Create → Pages → Connect to Git.
3. Choose the repo. For a plain HTML site, **no build command is needed**. Set the output directory to `/` (the repo root, sometimes named `.`).
4. Deploy. Cloudflare provides a temporary `*.pages.dev` address and HTTPS.
5. Update by committing files to GitHub; Cloudflare redeploys automatically.
6. For a custom domain, add it in Pages → Custom domains, then apply the DNS instructions. Buying a custom domain is typically not free.

Alternative: Netlify's drag-and-drop deploy is a quick way to publish the unzipped folder; GitHub Pages can host the same files from a public repository. Both work with separate HTML files.

## Make the admin page publish updates immediately (free tier)

This uses **Supabase** with a free database and email/password authentication. The public site reads announcements and content from Supabase, and **only explicitly approved admin users** can update it.

1. Create a Supabase project at https://supabase.com/ (free plan is sufficient for a small club; inactive free projects may pause).
2. Go to SQL Editor and run `supabase-setup.sql`.
3. In Authentication → Users, create/invite a user account for yourself. Verify it before trying to sign in. **Do not use your school password**.
4. Copy that account's **User ID (UUID)** and run this in SQL Editor, replacing the placeholder: `insert into public.club_admins(user_id) values ('YOUR-USER-UUID');`
5. In Project Settings → API, copy the **Project URL** and **publishable/anon key** (NOT the service_role/secret key). Open `supabase-config.js` and paste them.
6. Commit/upload the updated `supabase-config.js` to your host.
7. Open `/admin.html` on your website. Sign in with your approved account, make edits, and press **Publish changes**. All pages fetch the updates on load.
8. To revoke admin access, remove the user's row from `public.club_admins`. You can optionally disable public signup in Supabase Auth settings; only allowlisted users can publish regardless.

**Important:** Do not put the admin password, a database password, or a Supabase service role key in HTML or JavaScript. Publishing is protected by Supabase Row Level Security (RLS), not by hiding `admin.html`. The `supabase-config.js` publishable key is meant to be public.

**Note:** Once Supabase is configured and the database row contains published data, those saved values take precedence over the default `site-data.js`. Initially the row is empty and the defaults still show.

## Editing the club notes

Google Docs → File → Share → Publish to web → Embed. Copy the published *Google Docs* iframe URL into the admin Notes field; optionally add the normal document URL. Notes are intended for public reading, so don't publish private names, emails, or other information without permission.

## Featurebase discussion board

`feedback.html` is reserved for Featurebase. The actual discussion portal embed remains **unwired** because Featurebase Phase 2D is opt-in and has not been approved yet. The separate React version from the previous delivery includes anonymous Featurebase Phase 1, but this simple static HTML build does not initialize the React SDK. If you choose 2D later, we can wire the portal with the correct SDK for your published site.

## Troubleshooting

- **No announcements?** They're hidden if there are no announcement entries or only blank titles.
- **Edits are visible only on your own computer?** You used Save local preview, not Publish. For static-only publishing, deploy the downloaded `site-data.js`.
- **Sign in works but publishing fails?** Check that the user UUID exists in `club_admins`, then confirm RLS policies were created by the SQL script.
- **Published site still shows old content?** Check the browser console for network errors and verify the Supabase project is active.
- **Links to other pages don't work?** Upload all HTML files and scripts together in the root folder.
- **Meeting details blank?** Fill them in on Admin. Avoid publishing a location until you're ready for it to be public.
