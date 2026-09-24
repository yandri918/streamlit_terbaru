const CACHE_NAME = 'krisan-pro-v2.2';
const OFFLINE_URLS = ['/', '/style.css', '/app.js', '/manifest.json'];

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  // Network-first for all requests: try network, update cache, fallback to cache on error
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        if (event.request.url.includes('/api/')) {
          return new Response(
            JSON.stringify({ success: false, message: 'Offline', data: null }),
            { headers: { 'Content-Type': 'application/json' } }
          );
        }
        return caches.match(event.request);
      })
  );
});
