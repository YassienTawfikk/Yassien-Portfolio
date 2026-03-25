
const CACHE_NAME = 'yassien-portfolio-v3';
const ASSETS_CACHE = 'assets-cache-v3';
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

// Fetch Event
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // ONLY handle same-origin requests.
    // Cross-origin (postimg, fonts, CDNs) are left to the browser — no interception.
    if (url.origin !== self.location.origin) return;

    // 1. Navigation Requests (HTML pages) -> Network First with cache fallback
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // 2. Same-origin static assets (CSS/JS/images) -> Stale-While-Revalidate
    event.respondWith(
        caches.open(ASSETS_CACHE).then((cache) => {
            return cache.match(event.request).then((cachedResponse) => {
                const fetchPromise = fetch(event.request).then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        cache.put(event.request, networkResponse.clone());
                    }
                    return networkResponse;
                }).catch(() => cachedResponse);

                return cachedResponse || fetchPromise;
            });
        })
    );
});
