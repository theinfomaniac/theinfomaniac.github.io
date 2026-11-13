# Biochem Club website

Simple, independent Biochem Club website based on your Interlink HTML/CSS/JS template. There are separate HTML files for Home, Meetings, Activities, Notes, Discussion, About, Join, and Admin. Meetings are usually on Thursdays.

1. Unzip everything into one folder.
2. Open `index.html` for the homepage, or `admin.html` to edit announcements and text.
3. Local preview works without an account. Changes saved in the local preview are only visible in your browser.
4. To publish without a backend, download the updated `site-data.js` file from Admin, replace the original, and redeploy the site.
5. To publish immediately to all visitors using an authenticated admin login, follow **`SETUP.md`**, create a Supabase project, run `supabase-setup.sql`, and put your public project settings in `supabase-config.js`.
6. Publish the folder with Netlify, Cloudflare Pages, or GitHub Pages.

**The Featurebase feedback portal remains a placeholder until you approve the opt-in Phase 2D embed.** The separate React Featurebase project from the prior version is not included in this static package.
