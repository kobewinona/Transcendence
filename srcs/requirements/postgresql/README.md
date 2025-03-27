## 🛢️ PostgreSQL – Secure Database Setup

### 📦 Role in the Project

PostgreSQL is used as the **relational database** for the Django backend.  
It stores persistent application data such as:

- 👤 User accounts and authentication sessions
- 🎯 Match history, game scores
- 🗂️ Any application-specific data tied to the project logic

---

### 🔐 Secure Startup with Vault

PostgreSQL uses a **dynamic secrets injection mechanism** powered by **Vault Agent**:

1. PostgreSQL does **not embed credentials inside the Docker image**.
2. Instead, it **waits for Vault Agent** to generate a file at:

```bash
/run/secrets/postgres_env/.env.db
