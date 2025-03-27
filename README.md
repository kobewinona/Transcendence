# ft_transcendence

This repository contains the full infrastructure for the `ft_transcendence` project, including reverse proxy, HTTPS, monitoring, secrets management, and service orchestration using Docker and Vault.

---

## 🚀 How to Launch the Project

To start the full infrastructure stack, simply run:

```bash
make
```

This will build all custom Docker images and start all containers using `docker-compose`.

---

## ⚙️ Prerequisites Before Starting

### 1. Update your `/etc/hosts`

You must add the following entry to access Grafana securely:

```
127.0.0.1 monitoring.localhost
```

This is required so that Apache and Grafana routing works correctly with HTTPS and reverse proxying.

---

### 2. Create the `secrets/` Directory and Files

Before running the project, you must manually create the following structure:

```
secrets/
├── api
│   └── .env.key
├── grafana
│   └── .env.grafana
├── postgres
│   └── .env.db
├── ssl
│   ├── certificate.crt
│   └── certificate.key
└── unseal_keys
    ├── init.json
    ├── root_token.txt
    ├── unseal_keys.txt
    └── vault-init-token.txt
```

Each file must contain valid content as described below.

---

## 📄 File Formats

### `secrets/api/.env.key`
```env
RESEND_API_KEY=<?secrets?>
CLIENT_ID=<?secrets?>
CLIENT_SECRET=<?secrets?>
```

### `secrets/grafana/.env.grafana`
```env
USER_ADMIN_GRAFANA=<?secrets?>
MDP_ADMIN_GRAFANA=<?secrets?>
```

> ⚠️ These values will be used as **Grafana admin login and password**.

### `secrets/postgres/.env.db`
```env
POSTGRES_DB=<?secrets?>
POSTGRES_USER=<?secrets?>
POSTGRES_PASSWORD=<?secrets?>
```

### `secrets/ssl/certificate.crt`
```
<?secrets?>
```

### `secrets/ssl/certificate.key`
```
<?secrets?>
```

> 🔐 These are your **self-signed SSL/TLS certificates** used by Apache to serve the app securely over HTTPS.

### `secrets/unseal_keys/`

These files will be **automatically populated** by the Vault initialization process (`vault-init` container), but must exist (even empty) before starting:

- `init.json`
- `root_token.txt`
- `unseal_keys.txt`
- `vault-init-token.txt`

---

## ✅ Once Prerequisites Are Met

After updating `/etc/hosts` and preparing the `secrets/` structure:

```bash
make
```

Then access:

- Application: `https://localhost`
- Grafana: `https://monitoring.localhost`

---

## 🌐 Docker Compose Networks Overview

This project uses four isolated Docker networks to separate responsibilities and ensure better security and clarity between services.

### `ft_transcendence`
- **Purpose**: Main application network for web traffic.
- **Connected services**: `apache`, `nginx`, `frontend`, `backend`, `vault-agent`, `grafana`
- **Why**: Allows web services to communicate securely and directly (e.g., Apache reverse proxy to Nginx and Grafana).

### `database_network`
- **Purpose**: Isolated network for the PostgreSQL database.
- **Connected services**: `postgres`, `backend`
- **Why**: Prevents unauthorized services from accessing the database directly.

### `vault_network`
- **Purpose**: Secure network for Vault secrets management.
- **Connected services**: `vault`, `vault-init`, `vault-agent`, `postgres`
- **Why**: Limits secret access to only trusted services and allows static IP mapping for Vault.

### `monitoring_network`
- **Purpose**: Dedicated network for observability tools.
- **Connected services**: `prometheus`, `grafana`, `alertmanager`, `node_exporter`
- **Why**: Keeps monitoring traffic and ports isolated from the main application for security and clarity.

> 🧠 Using separate networks improves modularity, security, and control over service communication.

---

## 🛠 Tech Stack

- Docker & Docker Compose
- Apache (HTTPS + Reverse Proxy)
- Nginx (frontend + backend gateway)
- PostgreSQL
- Vault & Vault Agent (Secrets Management)
- Prometheus + Alertmanager (Monitoring + Alerting)
- Grafana (Dashboards)

---

## 👨‍💻 Author

Project created as part of the `ft_transcendence` evaluation at 42.
