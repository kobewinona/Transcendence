## 🌐 Nginx – Static Assets Server & API/WebSocket Proxy

### Role of Nginx in the Project

Nginx acts as a **reverse proxy** and **static file server** for the frontend (SPA), while also handling **proxying to the backend API** and **WebSocket connections**.

It is exposed **internally only** (port 8080), and all external traffic goes through **Apache**, which proxies to Nginx.

---

### 🔧 Key Features

| Feature                          | Description |
|----------------------------------|-------------|
| **Static File Server**           | Serves frontend build (`index.html`, JS, CSS, fonts) from `/usr/share/nginx/html` |
| **API Proxy**                    | Routes `/api/` requests to the Django backend on `backend:8000` |
| **WebSocket Support**            | Supports `/ws/` routes via HTTP/1.1 upgrade headers |
| **SPA Routing**                  | Unmatched routes fallback to `/index.html` |
| **Security Headers**             | Hardened using `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`, etc. |
| **Gzip Compression**             | Reduces bandwidth for text-based content |
| **Connection Tuning**            | Optimized for latency, file delivery, keep-alives |
| **Cache Headers**                | Assets in `/assets/` are cached for 30 days (`immutable`) |

---

### 🔐 Security Hardening

Nginx includes security-focused headers to mitigate common web threats:

- `X-Frame-Options`: Prevents clickjacking
- `X-XSS-Protection`: Enables basic XSS filters
- `X-Content-Type-Options`: Prevents MIME sniffing
- `Content-Security-Policy`: Strict policy with `self` source for scripts and styles
- `Referrer-Policy`: Reduces referrer data exposure

```nginx
add_header Content-Security-Policy "default-src 'self';
  script-src 'self';
  style-src 'self';
  img-src 'self' data: https://upload.wikimedia.org https://cdn.intra.42.fr;
  connect-src 'self' https://localhost wss://localhost https://api.intra.42.fr" always;
```

---

### 🕸️ Networking

Nginx is part of the `ft_transcendence` Docker network:

```yaml
networks:
  ft_transcendence:
    name: ft_transcendence
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.200.0/24
```

---

### 📜 Logs

Nginx logs all requests and errors internally:

```markdown
- `access.log` includes all frontend/API requests
- `websocket.log` specifically logs `/ws/` WebSocket connections
```

These logs help for observability and debugging.