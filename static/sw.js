
const CACHE_NAME = 'yassien-portfolio-v2';
const ASSETS_CACHE = 'assets-cache-v2';
const PRECACHE_URLS = []; // Will be populated by build script during deployment

// Install Event: Cache core static assets immediately
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(ASSETS_CACHE).then((cache) => {
            return cache.addAll(PRECACHE_URLS);
        })
    );
    self.skipWaiting();
});

// Activate Event: Clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== ASSETS_CACHE) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event: Hybrid Strategy
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Only handle http/https
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

    // 1. Navigation Requests (HTML pages) -> Network First
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // 2. Same-origin static assets (CSS/JS/images) -> Stale-While-Revalidate
    if (url.origin === self.location.origin) {
        event.respondWith(
            caches.open(ASSETS_CACHE).then((cache) => {
                return cache.match(event.request).then((cachedResponse) => {
                    const fetchPromise = fetch(event.request).then((networkResponse) => {
                        if (networkResponse.status === 200) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => cachedResponse);

                    return cachedResponse || fetchPromise;
                });
            })
        );
        return;
    }

    // 3. Cross-origin resources (postimg, fonts, CDNs) -> Network First, cache on success
    //    Do NOT use respondWith for cross-origin — let the browser handle it natively.
    //    Only intercept if we have a cached copy to serve as fallback.
    if (event.request.destination === 'image' ||
        event.request.destination === 'style' ||
        event.request.destination === 'font') {
        event.respondWith(
            fetch(event.request).then((networkResponse) => {
                // Only cache same-origin or CORS responses (status > 0)
                if (networkResponse.status === 200) {
                    const clone = networkResponse.clone();
                    caches.open(ASSETS_CACHE).then((cache) => cache.put(event.request, clone));
                }
                return networkResponse;
            }).catch(() => {
                // Network failed — try cache, otherwise let browser show its default error
                return caches.match(event.request);
            })
        );
        return;
    }

    // Default: Don't intercept — let the browser handle it natively
});
