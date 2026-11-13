/* the app moved to TrueLoop: drop this cache and unregister */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('cuag-')).map(k=>caches.delete(k)))).then(()=>self.registration.unregister()))});
