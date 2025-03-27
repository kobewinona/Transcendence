## 🔐 Vault – Centralized Secrets Management

### What is Vault?

Vault is a **secure secret management tool** developed by HashiCorp.  
In this project, it plays a critical role in:

- 📦 **Storing sensitive data** like:
  - SSL certificates for Apache
  - Database credentials (PostgreSQL)
  - API keys for the backend
  - Grafana admin credentials

- 🧑‍💻 Providing secrets **on demand** via Vault Agent to services that need them — securely and without hardcoding anything.

- 🔒 Protecting all credentials using access control policies (ACLs) and encryption-at-rest.

---

### 🧠 How Does Vault Work in This Project?

1. **Vault starts sealed and uninitialized**
2. A special container `vault-init`:
   - Checks if Vault is initialized
   - If not: initializes Vault, saves unseal keys and root token
   - Unseals Vault using 3 keys
   - Writes secrets to paths like `secret/backend`, `secret/postgres`, etc.
   - Creates policies + AppRole authentication for `vault-agent`
3. **Vault Agent** runs in another container:
   - Authenticates using AppRole (`role_id` + `secret_id`)
   - Pulls secrets securely via templates
   - Writes them to mounted volumes consumed by other services

---

### 🔄 Secrets Flow

| Secret               | Vault Path           | Consumed By      |
|----------------------|----------------------|------------------|
| `certificate.crt/key` | `secret/ssl/`        | Apache           |
| `POSTGRES_*`         | `secret/postgres/`   | PostgreSQL       |
| `RESEND_API_KEY`     | `secret/backend/`    | Backend (Django) |
| `GRAFANA_*`          | `secret/grafana/`    | Grafana          |

These secrets are **not embedded into images or code**. They are **injected at runtime** via Vault Agent templates.

---

### 🧰 vault-init: Automatic Setup

The `vault-init` container is responsible for:

- Waiting for Vault to be ready
- Initializing Vault (if not already)
- Saving unseal keys and root token to mounted volumes
- Automatically unsealing Vault using first 3 keys
- Creating:
  - `vault-init-policy` (admin access for provisioning)
  - `vault-agent-policy` (read-only access for apps)
  - AppRole for Vault Agent
- Writing secrets into Vault from the `secrets/` folder

**Directory structure expected before launch:**


---

### 📁 Vault Volumes

Secrets are rendered to Docker volumes mounted into services:

```yaml
volumes:
  - vault_backend_env:/vault/backend
  - vault_postgre_env:/vault/postgres
  - vault_grafana_env:/vault/grafana
  - vault_certs:/vault/ssl
```

### 🛡️ Security Notes

- Vault runs in an isolated Docker network (vault_network), not exposed publicly.

- TLS is disabled inside the Docker network — Apache handles public-facing HTTPS.

- vault-agent uses least privilege via fine-tuned AppRole policies.

- All unseal keys and tokens are stored outside the images, in the /secrets/unseal_keys/ folder.

### ✅ Why Use Vault?
Using Vault in this project guarantees:

- 🔐 Confidentiality: secrets are never committed or exposed

- 🚫 No leaks: no credentials in Dockerfiles or .env files

- 👮‍♂️ Access control: thanks to policy-based AppRoles

- 🔁 Dynamic secret delivery: injected at runtime only