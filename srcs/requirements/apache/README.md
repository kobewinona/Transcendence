## 🔁 Apache – Reverse Proxy & Web Application Firewall (WAF)

### Role of Apache in the Project

Apache acts as a **reverse proxy** and a **Web Application Firewall (WAF)** in your infrastructure. Its primary responsibilities are:

- 🔄 **Routing incoming HTTPS traffic**:
  - Forwards all user requests securely to either:
    - **Nginx** (serving the frontend and backend),
    - or **Grafana** (monitoring dashboard),
    depending on the domain or URL path.

- 🔐 **Enhancing security using ModSecurity**:
  - Apache is configured with **ModSecurity**, a Web Application Firewall, to inspect, filter, and block malicious requests such as:
    - SQL injections,
    - XSS attacks,
    - common web vulnerabilities (OWASP Top 10).

---

### Key Apache Features in this Project

| Feature                        | Description |
|-------------------------------|-------------|
| **HTTPS Enabled**             | Apache handles SSL/TLS via `certificate.crt` and `certificate.key` mounted from Vault secrets. |
| **Virtual Hosts**             | Two vhosts configured on port `443`: <br> - `localhost`: routes to the main app (via Nginx) <br> - `monitoring.localhost`: routes to Grafana |
| **WAF ModSecurity Rules**     | Specific rules are applied or disabled on sensitive routes like `/api/` and `/ws/` to avoid false positives while maintaining security |
| **Headers Hardening**         | Apache sets security headers like `Strict-Transport-Security`, `Upgrade`, and `Connection` to enforce secure behavior |
| **Access Restrictions**       | Prevents access to hidden files and enforces strong defaults for security |

---

### Why Apache + Nginx?

Even if **Nginx** is already used to serve static files and proxy backend/API traffic, **Apache** was added **explicitly to comply with the “Cybersecurity” module**:

> _"Implement WAF/ModSecurity with Hardened Configuration and HashiCorp Vault for Secrets Management."_

Nginx doesn't support ModSecurity natively in its open-source version (only via complex builds or Nginx Plus). Apache is the **industry-standard choice** for integrating **ModSecurity** efficiently.

---

### Networking

Apache is part of the `ft_transcendence` Docker network:

```yaml
networks:
  ft_transcendence:
    name: ft_transcendence
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.200.0/24
