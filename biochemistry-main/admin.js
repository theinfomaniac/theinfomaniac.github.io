// Admin mode uses Supabase Auth + database RLS for live publishing.
// Without Supabase setup, local preview and downloading site-data.js still work.
const config=supabaseConfig();
let jwt='',activeAdmin=false,editing={...CLUB,announcements:[...(CLUB.announcements||[])],meetingUpdates:[...(CLUB.meetingUpdates||[])]};
const $=id=>document.getElementById(id);
const status=message=>{$('admin-status').textContent=message;};
function textField(label,value,name,index,key){
  const wrap=document.createElement('div');
  const l=document.createElement('label');l.textContent=label;
  const input=document.createElement(name==='body'||name==='description'?'textarea':'input');
  input.value=value||'';input.dataset.index=index;input.dataset.key=key;input.dataset.part=name;
  input.addEventListener('input',()=>{editing[key][index][name]=input.value;});
  wrap.append(l,input);return wrap;
}
function drawItems(key,containerId,parts){
  const container=$(containerId);container.replaceChildren();
  if(!editing[key].length){const p=document.createElement('p');p.className='admin-empty';p.textContent='Nothing added yet.';container.append(p)}
  editing[key].forEach((item,index)=>{
    const card=document.createElement('div');card.className='admin-item';
    const title=document.createElement('div');title.className='admin-item-top';
    const s=document.createElement('strong');s.textContent=(key==='announcements'?'Announcement ':'Meeting date ')+(index+1);
    const del=document.createElement('button');del.type='button';del.className='small-button';del.textContent='Remove';del.addEventListener('click',()=>{editing[key].splice(index,1);drawItems(key,containerId,parts)});
    title.append(s,del);card.append(title);
    for(const [name,label] of parts){card.append(textField(label,item[name],name,index,key))}
    container.append(card);
  });
}
function drawAll(){
  document.querySelectorAll('[data-field]').forEach(field=>{field.value=editing[field.dataset.field]||''});
  drawItems('announcements','announcement-list',[['title','Title'],['date','Date (optional)'],['body','Message']]);
  drawItems('meetingUpdates','updates-list',[['date','Date'],['description','Details']]);
}
function gather(){
  document.querySelectorAll('[data-field]').forEach(field=>{editing[field.dataset.field]=field.value.trim()});
  editing.announcements=editing.announcements.map(x=>({title:String(x.title||'').trim(),date:String(x.date||'').trim(),body:String(x.body||'').trim()})).filter(x=>x.title);
  editing.meetingUpdates=editing.meetingUpdates.map(x=>({date:String(x.date||'').trim(),description:String(x.description||'').trim()})).filter(x=>x.date||x.description);
  if(editing.notesEmbedUrl&&!validGoogleUrl(editing.notesEmbedUrl))throw new Error('Google Docs embed URL must start with https://docs.google.com/');
  if(editing.notesDocumentUrl&&!validGoogleUrl(editing.notesDocumentUrl))throw new Error('Google Docs link must start with https://docs.google.com/');
  if(editing.contactEmail&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editing.contactEmail))throw new Error('Enter a valid public contact email or leave it blank.');
  return JSON.parse(JSON.stringify(editing));
}
async function api(path,options={}){
  if(!config)throw new Error('Set up Supabase first.');
  const headers={apikey:config.anonKey,'Content-Type':'application/json',...options.headers};
  if(jwt)headers.Authorization='Bearer '+jwt;
  const res=await fetch(config.url+path,{method:options.method||'GET',headers,body:options.body?JSON.stringify(options.body):undefined});
  let data;try{data=await res.json()}catch{data={}};
  if(!res.ok)throw Error(data.msg||data.error_description||data.message||('Request failed: '+res.status));
  return data;
}
function accessState(authorized){
  activeAdmin=authorized;
  $('admin-editor').hidden=!!config&&!authorized;
  $('login-area').hidden=!config||authorized;
  $('login-actions').hidden=!config||!authorized;
  $('publish-button').disabled=!config||!authorized;
  $('mode-description').textContent=config
    ? authorized?'Connected. Publishing updates this website for every visitor.':'Live publishing is enabled. Sign in with an approved admin account to edit.'
    :'Offline editor: you can preview changes in this browser or download site-data.js to upload with your site. For public updates without re-uploading, connect Supabase.';
  $('publish-hint').textContent=config?'Publishing saves to your Supabase database. Visitors see the update the next time they load the page.':'Live publishing needs Supabase. Use Download site-data.js, replace the file in your site folder, and redeploy the folder.';
}
$('login-form').addEventListener('submit',async e=>{
  e.preventDefault();const btn=e.currentTarget.querySelector('button[type=submit]');btn.disabled=true;
  try{
    const data=await api('/auth/v1/token?grant_type=password',{method:'POST',body:{email:$('email').value.trim(),password:$('password').value}});
    jwt=data.access_token;
    // An account is authorized only when the SQL admin allowlist contains its UID.
    const rows=await api('/rest/v1/club_admins?select=user_id&user_id=eq.'+encodeURIComponent(data.user.id));
    if(!Array.isArray(rows)||!rows.length)throw Error('This account is not an approved club admin. Add its User ID in Supabase using SETUP.md.');
    $('password').value='';$('session-label').textContent=data.user.email;
    const live=await api('/rest/v1/club_site_content?id=eq.1&select=data');
    if(Array.isArray(live)&&live[0]?.data)editing={...CLUB,...live[0].data};
    drawAll();accessState(true);status('Signed in. You can publish changes.');
  }catch(err){jwt='';accessState(false);$('login-status').textContent=err.message;status(err.message)}finally{btn.disabled=false}
});
$('signout-button').addEventListener('click',()=>{jwt='';activeAdmin=false;accessState(false);status('Signed out.')});
$('add-announcement').addEventListener('click',()=>{editing.announcements.push({title:'',date:'',body:''});drawItems('announcements','announcement-list',[['title','Title'],['date','Date (optional)'],['body','Message']])});
$('add-meeting-update').addEventListener('click',()=>{editing.meetingUpdates.push({date:'',description:''});drawItems('meetingUpdates','updates-list',[['date','Date'],['description','Details']])});
$('preview-button').addEventListener('click',()=>{try{localStorage.setItem('biochem-admin-preview',JSON.stringify(gather()));status('Local preview saved. Open a site page in this browser to see it. This has NOT published changes for everyone.')}catch(err){status(err.message)}});
$('clear-preview').addEventListener('click',()=>{localStorage.removeItem('biochem-admin-preview');status('Local preview cleared. Reload any open pages to see published/default content.')});
$('download-button').addEventListener('click',()=>{try{const data=gather();const blob=new Blob(['// Biochem Club default content\nconst CLUB = '+JSON.stringify(data,null,2)+';\n'],{type:'text/javascript'});const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download='site-data.js';a.click();setTimeout(()=>URL.revokeObjectURL(u),4000);status('Downloaded site-data.js. Replace the file in your site folder and redeploy to publish without a database.')}catch(err){status(err.message)}});
$('publish-button').addEventListener('click',async()=>{
  if(!activeAdmin||!jwt){status('Sign in before publishing.');return}
  try{const data=gather();const rows=await api('/rest/v1/club_site_content?id=eq.1',{method:'PATCH',headers:{Prefer:'return=representation'},body:{data}});
    if(!Array.isArray(rows)||!rows.length)throw Error('Update was not accepted. Check your Supabase admin permissions.');
    Object.assign(CLUB,data);try{localStorage.removeItem('biochem-admin-preview')}catch{};status('Published successfully. Anyone loading the site now will see these changes.');
  }catch(err){status('Could not publish: '+err.message)}
});
accessState(false);
if(!config){
  try{const prior=JSON.parse(localStorage.getItem('biochem-admin-preview')||'null');if(prior && typeof prior==='object')editing={...editing,...prior};}catch{}
  drawAll();status('Local editing ready. Changes will not update your public site unless you download and deploy the file.');
}
