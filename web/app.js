'use strict';
const $ = id => document.getElementById(id);
const controls=['query','category','maturity','licence','sort','hide-archived'];
const escapeHTML=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const permissive=new Set(['MIT','BSD-2-Clause','BSD-3-Clause','Apache-2.0','ISC','Zlib','Unlicense','CC0-1.0','BSL-1.0']);
const copyleft=new Set(['GPL-2.0','GPL-2.0-only','GPL-2.0-or-later','GPL-3.0','GPL-3.0-only','GPL-3.0-or-later','LGPL-2.1','LGPL-2.1-only','LGPL-2.1-or-later','LGPL-3.0','LGPL-3.0-only','LGPL-3.0-or-later','AGPL-3.0','AGPL-3.0-only','MPL-2.0']);
let data,categoryNames;
function licenceGroup(entry){const id=entry.metadata.license;return permissive.has(id)?'permissive':copyleft.has(id)?'copyleft':'review';}
function render(){
  const query=$('query').value.toLowerCase().trim().split(/\s+/).filter(Boolean),category=$('category').value,maturity=$('maturity').value,licence=$('licence').value;
  let entries=data.entries.filter(e=>{const haystack=[e.name,e.repo,e.summary,e.best_for,e.caveat,...e.tags,e.metadata.language,categoryNames[e.category]].join(' ').toLowerCase();return query.every(word=>haystack.includes(word))&&(!category||e.category===category)&&(!maturity||e.maturity===maturity)&&(!licence||licenceGroup(e)===licence)&&(!$('hide-archived').checked||!e.metadata.archived);});
  const order=$('sort').value;
  entries.sort((a,b)=>order==='stars'?b.metadata.stargazers_count-a.metadata.stargazers_count:order==='updated'?String(b.metadata.pushed_at).localeCompare(String(a.metadata.pushed_at)):a.name.localeCompare(b.name));
  $('result-count').textContent=`${entries.length} of ${data.entries.length} repositories · snapshot ${data.snapshot}`;
  $('empty').hidden=entries.length>0;
  $('results').innerHTML=entries.map(e=>{const r=e.metadata;return `<article class="card"><p class="category">${escapeHTML(categoryNames[e.category])}</p><h3><a href="${escapeHTML(r.html_url)}">${escapeHTML(e.name)}</a></h3><p class="repo">${escapeHTML(e.repo)}</p><p class="summary">${escapeHTML(e.summary)}</p><p class="use">For: ${escapeHTML(e.best_for)}</p><div class="tags">${e.tags.map(t=>`<span class="tag">${escapeHTML(t)}</span>`).join('')}</div><div class="meta">${escapeHTML(e.maturity)} · ${escapeHTML(r.language||'mixed / unspecified')} · ${escapeHTML(r.license)}<br>${Number(r.stargazers_count).toLocaleString()} stars in snapshot · pushed ${escapeHTML(String(r.pushed_at||'unknown').slice(0,10))}${r.archived?' · <strong class="archived">archived</strong>':''}</div><div class="links"><a href="${escapeHTML(r.html_url)}">Repository ↗</a><a href="${escapeHTML(e.docs_url)}">Documentation ↗</a></div>${e.caveat?`<details><summary>Selection note</summary><p>${escapeHTML(e.caveat)}</p></details>`:''}</article>`;}).join('');
  const params=new URLSearchParams();for(const id of controls){const c=$(id);if(c.type==='checkbox'){if(c.checked)params.set(id,'1');}else if(c.value&&!(id==='sort'&&c.value==='name'))params.set(id,c.value);}
  const suffix=params.toString();history.replaceState(null,'',location.pathname+(suffix?'?'+suffix:'')+location.hash);
}
async function init(){
  const response=await fetch('data.json');if(!response.ok)throw new Error('Catalogue could not be loaded');data=await response.json();categoryNames=Object.fromEntries(data.categories.map(c=>[c.id,c.title]));
  for(const c of data.categories){const option=document.createElement('option');option.value=c.id;option.textContent=c.title;$('category').append(option);}
  $('coverage').textContent=`${data.entries.length} repositories · ${data.categories.length} topics · ${data.external.length} official external resources · checked ${data.snapshot}`;
  const params=new URLSearchParams(location.search);for(const id of controls){if(params.has(id)){const c=$(id);if(c.type==='checkbox')c.checked=params.get(id)==='1';else c.value=params.get(id);}}
  for(const id of controls)$(id).addEventListener(id==='query'?'input':'change',render);
  $('filters').addEventListener('submit',event=>event.preventDefault());$('filters').addEventListener('reset',()=>setTimeout(render,0));
  $('external').innerHTML=data.external.map(e=>`<article class="external"><h3><a href="${escapeHTML(e.url)}">${escapeHTML(e.name)} ↗</a></h3><p>${escapeHTML(e.summary)}</p><small>${escapeHTML(e.access_note)}</small></article>`).join('');
  document.addEventListener('keydown',event=>{if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){event.preventDefault();$('query').focus();}});render();
}
init().catch(error=>{$('coverage').textContent='The live directory is unavailable. The complete GitHub index and PDF remain accessible.';$('result-count').textContent=error.message;});
