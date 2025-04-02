# Backend – Django API + Gameplay Logic

The backend is built with Python and Django, backed by a PostgreSQL database running in a dedicated container. It exposes a secure API and manages all core features like authentication, users, real-time gameplay, and tournaments.

## 📦 Dependencies & Subject Compliance

> _“The use of libraries or tools that provide an immediate complete solution for a global feature or a module is prohibited.”_  
> _Small libraries that solve a simple and unique task are allowed. Teams must justify any usage that isn’t explicitly approved._

This project strictly adheres to the subject rules by **avoiding full-stack or feature-complete third-party solutions**. Below is a breakdown of key packages and their justifications:

---

### ✅ Core Framework & Required Extensions

| Package | Justification                                                                                                                                    |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `django` | Core web framework; required for building the backend logic, ORM, routing, and views.                                                            |
| `djangorestframework` | Adds API serialization and viewsets – **does not solve a full module**, but extends Django for REST APIs.                                        |
| `channels`, `daphne` | Needed for **WebSocket support** in Django (required for real-time Pong gameplay). Does not solve any game logic.                                |
| `psycopg2-binary` | PostgreSQL database driver for Django ORM. Used for database as part of a separate module.                                                       |
| `django-otp`, `pyotp` | Used for sending and verifying **2FA OTP codes** via email. They provide **narrow, single-purpose** functionality. Used as part of a 2FA module. |
| `django-cors-headers` | Small utility to allow cross-origin requests from the frontend (required in SPA setups required by the subject).                                 |
| `django-environ`, `python-dotenv` | Help manage `.env` variables and secret injection (especially with Vault).                                                                       |
| `rest_framework_simplejwt`, `pyjwt` | Used to manually handle **JWT token generation**, refresh, and blacklisting. Does not abstract full authentication flow.                         |

---

### ✅ Utility & Support Libraries

| Package | Justification |
|--------|---------------|
| `requests`, `requests-oauthlib`, `oauthlib` | Used for calling external APIs (e.g. 42 Intra, Resend, RandomUser). They **do not replace core logic**. |
| `resend` | Sends OTP emails – **a single-purpose task**, isolated to the 2FA feature. |
| `watchfiles` | Dev-only: watches file changes and restarts services during development. |
| `colorama` | Enables colorized logs (purely cosmetic, used in custom logger). |
| `whitenoise` | Serves static files in production, a minimal alternative to a CDN or Nginx. |
| `pillow` | Image field support (used optionally for avatars). Does not process or manage media logic. |
| `sqlparse` | Used internally by Django for SQL formatting. |
| `twisted`, `tornado`, `autobahn`, etc. | Required as transitive dependencies of `channels` and `daphne`. Not directly used by the project. |

---

### ✅ Dev-only Tools

| Package | Justification |
|--------|---------------|
| `black`, `mypy`, `django-stubs`, `djangorestframework-stubs` | Used for formatting, typing, and linting – **non-functional** in production. |
| `pipenv`, `virtualenv` | Standard tools to manage Python environment and dependency locking. |

---

All third-party packages were chosen **only when absolutely necessary**, and all business logic (authentication, game engine, tournament management) is **implemented from scratch**, in full compliance with the subject.

## 🧩 Process Management – Django + ASGI via Supervisor

The backend runs multiple Python services in parallel using **Supervisor**, ensuring clean startup, restarts, and logging for each process.

---

### 🏭 Supervisor Overview

- Defined in: `supervisord.conf` and `supervisord.dev.conf`
- Used to launch and manage:
  - Django REST API (port `8001`)
  - ASGI WebSocket server via Daphne (port `8000`)
  - File watcher (only in development)

---

### 🚀 Production Services

- **`daphne`**: Serves ASGI for WebSocket communication
- **`django`**: Serves the REST API (no auto-reload)
- All logs stream to `stdout`/`stderr`, perfect for Docker

---

### 🧪 Development Mode

- Adds a third process: **`watchfiles`**
  - Watches file changes
  - Runs Mypy type checks
  - Restarts `django` and `daphne` when clean
- Controlled via: `supervisord.dev.conf`

---

### 🔧 Docker Entrypoint & Setup

- Uses a shared image for dev/prod with `SUPERVISOR_CONF_PATH` env var to toggle config
- Builds and starts with:
  - Pipenv-managed Python dependencies
  - Static file collection
  - Executable entrypoint script
  - Logs written to `/logs` and container output

---

This Supervisor setup allows **parallel service management**, **live reloads during development**, and **process isolation in production**, all fully Dockerized and ready for CI/CD.

## ⚙️ Django Settings Overview

The `settings.py` file is structured and modular, optimized for secure production and local development using `.env` files and Vault integration.

---

### 🏗️ Core Project Setup

- Environment mode: `development` or `production` via `APP_ENV_MODE`
- App URLs and WebSocket endpoints configured via environment variables
- Uses a **custom user model**: `users.CustomUser`

---

### 📦 Installed Apps

Includes:
- Core Django apps
- Third-party tools: `channels`, `rest_framework`, `corsheaders`
- Custom project apps: `pong`, `oauth`, `users`, `tournaments`

---

### 🔒 Security & Auth

- Secure cookies (`CSRF`, `SESSION`) in production mode
- Uses **JWT with refresh/access tokens**
- Secure cookie options for refresh tokens (`HttpOnly`, `SameSite`, `Secure`)
- Auth backends:
  - Default Django auth
  - Custom `JWTOrIntraAuthentication` backend
- Password validation rules enabled

### 🔐 Password Hashing in Django

To comply with the security constraint that passwords must **not be stored in plain text**, this project relies on Django’s built-in authentication system, which **automatically hashes passwords** before saving them to the database.

---

### 🔍 How It Works in Django

- Django uses the [`AbstractUser`](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model) base class.
- The `set_password()` method automatically hashes the password using the default hasher.
- The password is stored in the database as a long string with a prefix that indicates the algorithm used.

**Example hashed password:**
`pbkdf2_sha256$600000$6yT1DrWDe7eq$aYdfzv+Gp0e9T2g7VLhKk7QOCJ4bEOLRcXBeU7PBg5Y=`

### 🛡️ Encryption Algorithm Used

- **Default algorithm**: `PBKDF2` with `SHA-256`
- **Hasher**: `pbkdf2_sha256`
- **Iterations**: 600,000 (as of Django 5.1)

### 🧪 How to Verify in PostgreSQL (Proof)

To check that passwords are indeed hashed in the database:

#### 1. Find the Postgres container name
```bash
docker ps
```

#### 2. Open a shell into the container (replace 'postgres' if needed)
```bash
docker exec -it postgres bash
```

#### 3. Enter the psql prompt
```bash
psql -U $POSTGRES_USER -d $POSTGRES_DB
```

#### 4. Query the users table
```bash
SELECT username, email, password FROM users_customuser;
```

---

### 🌐 CORS & CSRF

- CORS only allows the frontend (`APP_URL`)
- Credentials and secure headers supported
- CSRF trusted origins include frontend and Intra 42 API

---

### 🛢️ Database

- PostgreSQL setup via secrets loaded from Vault (`.env.db`)
- Database credentials not hardcoded

---

### 🧵 WebSockets & Channels

- Uses **Django Channels** with `InMemoryChannelLayer` (no Redis for now)
- ASGI enabled via `project.asgi.application`

---

### 📂 Static Files

- Static assets served from `/static/`
- Optimized for Docker builds with `STATIC_ROOT`

---

### 🌍 Localization

- Language: `en-us`
- Timezone: `UTC`
- Internationalization and timezone support enabled

---

### ⚙️ REST Framework

- All API endpoints require authentication by default
- Custom exception handler used for consistent error responses
- Only authenticated users can access API routes

---

### 🔑 Vault Integration

- Secrets (DB, backend) loaded from files injected by **Vault Agent**
- Centralized and secure secret management

---

This configuration ensures production readiness with strict security defaults, modular environment overrides, and full integration with JWT auth and WebSockets.

## 🧩 Django Apps Overview

| App                                                    | Description |
|--------------------------------------------------------|-------------|
| [**oauth**](#-oauth--authentication--42-integration)  | Handles user authentication, including **42 intra OAuth**, email OTP, and session logic. |
| [**pong**](#-pong--realtime-gameplay-engine)           | Core game engine using **WebSockets**, processes ball/paddle physics and real-time score updates. |
| [**tournaments**](#-tournaments--stages-matches--winners) | Manages **tournament structure**, match progression, results, and winner tracking. |
| [**users**](#-users--profiles--game-stats)             | Custom user model, profile info, and stats tracking like match history and rankings. |

### 🔐 oauth – Authentication & 42 Integration
This app manages all user authentication using two secure sign-in methods:

---

#### 1️⃣ Two-Factor Authentication (Email OTP)

- Based on Django REST Framework with JWT.
- Users log in with credentials and receive a one-time password (OTP) via email.
- The OTP email is sent through the Resend API, using a Django HTML template.
- Once the user submits the correct OTP:
    - A **refresh token** is issued via a `Set-Cookie` header (HttpOnly, Secure, SameSite=Lax).
    - An **access token** is returned in the response body and saved in localStorage.
- The backend uses JWT authentication classes to protect sensitive routes.
- A `/refresh_tokens/` endpoint lets the frontend rotate expired tokens by:
    - Blacklisting old tokens.
    - Issuing new ones.
- On logout, tokens are added to a blacklist to prevent reuse.

---

#### 2️⃣ 42 Intra OAuth2 Login

- Users can authenticate via their 42 Intra account.
- The frontend redirects users to the 42 authorization page with necessary credentials.
- After successful login, 42 redirects back to the backend with an authorization code.
- The backend exchanges the code for tokens, fetches the user’s profile from 42, and either creates or updates the user in the database.
- The access token is sent to the frontend via URL query params, while the refresh token is securely stored in a cookie.

---

### 🏓 pong – Real-Time Gameplay Engine
This app powers the Pong game logic using **WebSockets** via Django Channels. It handles matchmaking, game state, physics, and real-time communication with the frontend.

---

#### 🔌 WebSocket Lifecycle

- Once a user is authenticated, the frontend establishes a WebSocket connection.
- The `PongConsumer` manages the full game session per connection.
- The session tracks states like **idle**, **in progress**, **paused**, and **ended**.

---

#### 🧠 Game Loop & Logic

- When idle, the frontend can trigger a **demo mode** where two AI players play automatically.
- The game runs in an **async loop** that:
  - Updates paddle positions and ball physics.
  - Calculates score, boundaries, and rebounds.
  - Sends game state to the frontend as **binary payloads** for performance.
- The frontend renders the game state however it chooses.

---

#### 🎮 Game Actions

The frontend can control the session by sending actions like:

- `update_dimensions`: Update canvas dimensions
- `start`: Start a game session
- `pause` / `resume`: Temporarily stop or continue the game loop
- `stop`: End the session
- `update_paddle`: Move a paddle in response to user input

---

#### 🏆 Tournament Integration

- If the game is part of a tournament, the loop will trigger bracket updates after the match ends.
- The tournament model is updated with the winner and progresses the bracket recursively as needed.

---

### 🏆 tournaments – Stages, Matches & Winners
This app manages the structure and lifecycle of tournaments, from creation to declaring a winner. It integrates closely with the `pong` app to automate progression through matches.

---

#### 🔁 Bracket Management

- Supports classic elimination stages: **1/16 → Final**.
- Automatically pairs players and calculates matchups.
- Tracks tournament `status`, `winner`, and `notified` states.

---

#### 👥 Player Auto-Fill with AI

- If the number of players is **not a power of two**, the system calculates the missing slots and:
  - Fetches **random user names** via a public API.
  - Fills the bracket with AI-controlled players.
  - Ensures names are unique by requesting a larger batch and filtering duplicates.

---

#### ⚙️ Integration with Gameplay

- Tournament matches trigger actual games using the `pong` app.
- Once a match finishes, the winner is:
  - Recorded in the tournament model.
  - Progressed to the next round **recursively**.
- All updates are handled automatically after the game loop completes.

---

### 👤 users – Profiles & Game Stats
This app defines a **custom user model** that extends Django's `AbstractUser` to support authentication and profile features tailored for the app.

---

#### 🧬 Custom Fields

- Uses **email as the primary login field**.
- Supports both internal and 42 Intra sign-ins via the `auth_provider` field.
- Stores additional user info:
  - `intra_id` for 42 integration
  - `avatar` (optional URL)
  - `username` (optional display name)

---

#### 🛡️ Validation & Serialization

- The `UserSerializer` exposes key fields to the frontend: `id`, `username`, `email`, `auth_provider`, `intra_id`, and `avatar`.
- Built-in validation ensures unique emails and intra IDs.
- When a user submits invalid data (e.g. duplicate email), the serializer returns clear error messages that the frontend can display.

## 📢 Logging Configuration

The project uses a **custom color-coded logging system** to improve readability and quickly distinguish between backend components during development and debugging.

---

### 🎨 Custom Formatter

Logs are colorized by:

- **Log level**:
  - `DEBUG`: Blue
  - `INFO`: Green
  - `WARNING`: Yellow
  - `ERROR`: Red
  - `CRITICAL`: Bold Red
- **Logger name** (app-specific):
  - `game_logs`: Cyan
  - `auth_logs`: Light Green
  - `tournaments_logs`: Light Blue
  - `fast-reload_logs`: Magenta

This makes it easy to visually separate logs by **origin and severity**.

---

### 🧭 Logger Setup

Defined in `settings.py` with per-app granularity:

- `game_logs`: Game state updates from WebSocket loop
- `auth_logs`: Authentication and token flow events
- `tournaments_logs`: Bracket and progression handling
- `fast-reload_logs`: Development reload/debug events

Each logger outputs to `console` using the `CustomFormatter`.

Logging level is dynamic:
- `DEBUG` in development
- `INFO` in production

---

This setup helps manage **high-frequency WebSocket output** and provides clarity when tracking state changes, auth events, or tournament updates in real time.

## 🔁 Fast Reload – File Watcher & Auto-Restart

To streamline development, the project includes a custom Django management command that **watches for file changes** and automatically restarts backend services.

---

### 🚀 How It Works

- Located in: `core/management/commands/`
- Uses the `watchfiles` library to recursively monitor all files in the project directory.
- Ignores changes to `.log`, `.pyc`, and `__pycache__` files.
- On file change:
  1. Runs **Mypy** for static analysis.
  2. If no issues are found, it **restarts `django` and `daphne`** using `supervisorctl`.

---

### 📢 Logging

- All logs are output using the `fast-reload_logs` logger.
- Example logs:
  - File change detection
  - Mypy pass/fail messages
  - Service restart status

---

This command runs in a **dedicated background process** and writes directly to the container’s stdout, offering live feedback during development while enforcing type safety.
