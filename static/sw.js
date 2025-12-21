const CACHE_NAME = 'project-images-cache-v1';
const URLS_TO_CACHE_PATTERNS = [
    'github.com/user-attachments/assets/',
    'githubusercontent.com'
];

self.addEventListener('install', event => {
    // Immediate activation
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', event => {
    const requestUrl = event.request.url;

    // Check if the request is for an external project image (GitHub/UserContent)
    const isTargetImage = URLS_TO_CACHE_PATTERNS.some(pattern => requestUrl.includes(pattern));

    if (isTargetImage) {
        event.respondWith(
            caches.match(event.request).then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(event.request).then(networkResponse => {
                    // Check if we received a valid response
                    // IMPORTANT: We MUST allow type 'opaque' (status 0) for cross-origin images (GitHub)
                    if (!networkResponse || (networkResponse.status !== 200 && networkResponse.type !== 'opaque') || (networkResponse.type !== 'cors' && networkResponse.type !== 'basic' && networkResponse.type !== 'opaque')) {
                        return networkResponse;
                    }

                    // Clone the response because it's a stream and can only be consumed once
                    const responseToCache = networkResponse.clone();

                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseToCache);
                    });

                    return networkResponse;
                }).catch(() => {
                    // Fallback or nothing if offline and not in cache
                });
            })
        );
    }
});
