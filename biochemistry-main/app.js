// Biochem Club public pages. Sidebar functions based on the Interlink template.
const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
function toggleSidebar(){
  if(!sidebar || !toggleButton)return;
  sidebar.classList.toggle('close');toggleButton.classList.toggle('rotate');
  toggleButton.setAttribute('aria-expanded',String(!sidebar.classList.contains('close')));
  closeAllSubMenus();
}
function toggleSubMenu(button){
  const sub=button.nextElementSibling;if(!sub)return;
  if(!sub.classList.contains('show'))closeAllSubMenus();
  const open=sub.classList.toggle('show');button.classList.toggle('rotate',open);
  button.setAttribute('aria-expanded',String(open));
  if(sidebar?.classList.contains('close')){sidebar.classList.remove('close');toggleButton?.classList.remove('rotate');toggleButton?.setAttribute('aria-expanded','true');}
}
function closeAllSubMenus(){
  if(!sidebar)return;
  sidebar.querySelectorAll('.sub-menu.show').forEach(menu=>{menu.classList.remove('show');menu.previousElementSibling?.classList.remove('rotate');menu.previousElementSibling?.setAttribute('aria-expanded','false');});
}
function toggleTheme(){
  const mode=document.body.classList.contains('dark-mode')?'light':'dark';
  document.body.classList.toggle('dark-mode',mode==='dark');
  document.body.classList.toggle('light-mode',mode==='light');
  try{localStorage.setItem('biochem-theme',mode)}catch{}
}
try{if(localStorage.getItem('biochem-theme')==='light'){document.body.classList.remove('dark-mode');document.body.classList.add('light-mode')}}catch{}

function validGoogleUrl(value){
  try{const u=new URL(value);return u.protocol==='https:' && u.hostname==='docs.google.com' ? u.href : '';}catch{return ''}
}
function showText(key,placeholder){
  const lookup={'meeting-frequency':'meetingFrequency','meeting-time':'meetingTime','meeting-location':'meetingLocation','next-meeting':'nextMeeting'};
  const val=CLUB[lookup[key]];
  return val || placeholder;
}
function refreshContent(){
  document.querySelectorAll('[data-edit]').forEach(el=>{
    const key=el.dataset.edit;
    if(typeof CLUB[key]==='string')el.textContent=CLUB[key];
  });
  const placeholders={'meeting-frequency':'Most Thursdays','meeting-time':'To be announced','meeting-location':'To be announced','next-meeting':'Next confirmed date will be posted here'};
  document.querySelectorAll('[data-club]').forEach(el=>{
    const key=el.dataset.club, v=showText(key,placeholders[key]||'To be announced');
    el.textContent=v;el.classList.toggle('status-note',!CLUB[({'meeting-frequency':'meetingFrequency','meeting-time':'meetingTime','meeting-location':'meetingLocation','next-meeting':'nextMeeting'})[key]]);
  });
  const box=document.getElementById('announcements');
  if(box){
    box.querySelectorAll('.notice-item').forEach(n=>n.remove());
    const notices=Array.isArray(CLUB.announcements)?CLUB.announcements:[];
    box.hidden=notices.length===0;
    for(const n of notices){
      const row=document.createElement('div');row.className='notice-item';
      const strong=document.createElement('strong');strong.textContent=n.title||'';row.appendChild(strong);
      if(n.date){const t=document.createElement('time');t.textContent=n.date;row.append(t)}
      if(n.body){const p=document.createElement('p');p.textContent=n.body;row.append(p)}
      box.append(row);
    }
  }
  const topics=document.getElementById('activity-topics');
  if(topics){topics.replaceChildren();String(CLUB.activitiesTopics||'').split(/\n/).map(s=>s.trim()).filter(Boolean).forEach(topic=>{const li=document.createElement('li');const s=document.createElement('strong');s.textContent=topic;li.append(s);topics.append(li)})}
  const tbody=document.getElementById('meeting-updates');
  if(tbody){tbody.replaceChildren();const updates=Array.isArray(CLUB.meetingUpdates)?CLUB.meetingUpdates:[];
    if(!updates.length){const tr=document.createElement('tr');const td=document.createElement('td');td.colSpan=2;td.textContent='No confirmed dates posted yet. Meetings are usually on Thursdays.';tr.append(td);tbody.append(tr)}
    for(const item of updates){const tr=document.createElement('tr');for(const k of ['date','description']){const td=document.createElement('td');td.textContent=item[k]||'';tr.append(td)}tbody.append(tr)}
  }
  const contact=document.getElementById('contact-link');const noContact=document.getElementById('contact-empty');
  const email=String(CLUB.contactEmail||'').trim();
  if(contact){contact.hidden=!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);if(!contact.hidden)contact.href='mailto:'+email;}
  if(noContact)noContact.hidden=!!(contact&&!contact.hidden);
  const panel=document.getElementById('notes-panel');const holder=document.getElementById('notes-placeholder');
  if(panel){panel.querySelectorAll('iframe,.doc-live-link').forEach(n=>n.remove());const url=validGoogleUrl(CLUB.notesEmbedUrl);
    if(holder)holder.hidden=!!url;
    if(url){const frame=document.createElement('iframe');frame.className='doc-frame';frame.src=url;frame.loading='lazy';frame.title='Biochem Club Google Docs notes';panel.append(frame);
      const external=validGoogleUrl(CLUB.notesDocumentUrl);if(external){const p=document.createElement('p');p.className='doc-live-link';const a=document.createElement('a');a.href=external;a.target='_blank';a.rel='noopener noreferrer';a.textContent='Open notes in Google Docs';p.append(a);panel.append(p)} }
  }
}
function supabaseConfig(){
  const c=window.BIOCHEM_SUPABASE||{};
  try{const url=new URL(c.url||'');if(url.protocol!=='https:'||!c.anonKey)return null;return {url:url.origin,anonKey:c.anonKey};}catch{return null}
}
async function fetchPublished(){
  const c=supabaseConfig();if(!c)return;
  try{
    const r=await fetch(c.url+'/rest/v1/club_site_content?id=eq.1&select=data',{headers:{apikey:c.anonKey}});
    if(!r.ok)throw Error('HTTP '+r.status);
    const rows=await r.json();if(rows.length&&rows[0].data&&typeof rows[0].data==='object'){Object.assign(CLUB,rows[0].data);refreshContent()}
  }catch(err){console.warn('Could not load published club content:',err); const main=document.querySelector('main');if(main){const p=document.createElement('p');p.className='small-note';p.textContent='Live updates could not load. This page is showing the saved site information.';main.prepend(p)}}
}
function applyPreview(){
  try{const text=localStorage.getItem('biochem-admin-preview');if(!text)return;
    const content=JSON.parse(text);if(content&&typeof content==='object'){
      Object.assign(CLUB,content);refreshContent();
      const main=document.querySelector('main');if(main){const badge=document.createElement('div');badge.className='preview-banner';badge.textContent='Local preview: only this browser sees these changes. Open Admin to publish or clear your preview.';main.prepend(badge)}
    }
  }catch{}
}
refreshContent();
fetchPublished().finally(applyPreview);
