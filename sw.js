const CACHE='bait-v2';
const ASSETS=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png','maskable-512.png','qr-install.png','exceljs.min.js'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
/* never answer with nothing (Safari then shows «FetchEvent.respondWith … Returned response is null») */
const OFFLINE='<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
  '<title>مصاريف البيت</title><body style="margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:-apple-system,Segoe UI,Tahoma,sans-serif;background:#0f766e;color:#fff;text-align:center;padding:24px">'+
  '<div><div style="font-size:54px">📶</div><h2 style="margin:10px 0">النت مش واصل دلوقتي</h2><p style="opacity:.85;line-height:1.7">مصاريفك محفوظة على الموبايل — ما اتمسحش حاجة.<br>شغّلي النت ودوسي «جرّبي تاني».</p>'+
  '<button onclick="location.reload()" style="font-size:18px;padding:14px 28px;border:0;border-radius:14px;background:#fff;color:#0f766e;font-weight:700">🔄 جرّبي تاني</button></div></body></html>';
const offline=()=>new Response(OFFLINE,{status:503,headers:{'Content-Type':'text/html; charset=utf-8'}});
self.addEventListener('fetch',e=>{
  const r=e.request; if(r.method!=='GET'||new URL(r.url).origin!==location.origin) return;
  if(new URL(r.url).pathname.endsWith('/version.json')) return;   // always from the network
  if(r.mode==='navigate'){e.respondWith((async()=>{
    try{const res=await fetch(r);
      if(res&&res.ok&&res.type==='basic'){const cp=res.clone();caches.open(CACHE).then(c=>c.put('index.html',cp)).catch(()=>{})}
      return res}
    catch(err){return (await caches.match('index.html'))||(await caches.match('./'))||offline()}})());return}
  e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{if(res&&res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp)).catch(()=>{})}return res}))
    .catch(()=>Response.error()));
});
