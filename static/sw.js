
const CACHE_NAME = 'yassien-portfolio-v1';
const ASSETS_CACHE = 'assets-cache-v1';
const PRECACHE_URLS = []; // Will be populated by build script during deployment

// Install Event: Cache core static assets immediately
self.addEventListener('install', (event) => {
    // Aggressive Pre-caching
    event.waitUntil(
        caches.open(ASSETS_CACHE).then((cache) => {
            // Add core assets + dynamic image list
            return cache.addAll(PRECACHE_URLS);
        })
    );
    self.skipWaiting(); // Activate worker immediately
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

    // 1. Navigation Requests (HTML pages) -> Network First
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => {
                    return caches.match(event.request);
                })
        );
        return;
    }

    // 2. External Images (PostImages, GitHub Assets) & Static Files (CSS/JS) -> Stale-While-Revalidate
    if ((url.protocol === 'http:' || url.protocol === 'https:') &&
        (
            event.request.destination === 'image' ||
            event.request.destination === 'style' ||
            event.request.destination === 'script' ||
            url.hostname.includes('postimg.cc') ||
            url.hostname.includes('githubusercontent.com')
        )) {
        event.respondWith(
            caches.open(ASSETS_CACHE).then((cache) => {
                return cache.match(event.request).then((cachedResponse) => {
                    const fetchPromise = fetch(event.request).then((networkResponse) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                    // Return cached response immediately if available, otherwise wait for network
                    return cachedResponse || fetchPromise;
                });
            })
        );
        return;
    }

    // Default: Network Only
    event.respondWith(fetch(event.request));
});
