pid_file = "/tmp/vault-agent.pid"

auto_auth {
  method "approle" {
    config = {
      role_id_file_path = "/vault/auth/role_id"
      secret_id_file_path = "/vault/auth/secret_id"
      remove_secret_id_file_after_reading = false
    }
  }
    sink "file" {
    config = {
      path = "/vault/.vault-token"
    }
  }
}

cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address = "0.0.0.0:8201"
  tls_disable = true
}

vault {
  address = "http://vault:8200"
}

template {
  destination = "/vault/certs/apache.crt"
  contents = <<EOF
{{ with secret "secret/data/ssl/certificate.crt" }}
{{ .Data.data.content }}
{{ end }}
EOF
}

template {
  destination = "/vault/certs/apache.key"
  contents = <<EOF
{{ with secret "secret/data/ssl/certificate.key" }}
{{ .Data.data.content }}
{{ end }}
EOF
}

template {
  source      = "/vault/config/templates/init-users.sql.ctmpl"
  destination = "/vault/postgres/init-users.sql"
  perms       = "0644"
}

template {
  destination = "/vault/postgres/.env.db"
  contents = <<EOF
{{ with secret "secret/data/postgres/admin" }}
POSTGRES_DB={{ .Data.data.POSTGRES_DB }}
POSTGRES_USER={{ .Data.data.POSTGRES_USER }}
POSTGRES_PASSWORD={{ .Data.data.POSTGRES_PASSWORD }}
{{ end }}
EOF
}

template {
  destination = "/vault/postgres_backend/.env.db"
  contents = <<EOF
{{ with secret "secret/data/postgres/admin" }}
POSTGRES_DB={{ .Data.data.POSTGRES_DB }}
{{ end }}
{{ with secret "secret/postgres/backend" }}
POSTGRES_USER={{ .Data.data.BACKEND_USER }}
POSTGRES_PASSWORD={{ .Data.data.BACKEND_PASSWORD }}
{{ end }}
EOF
}

template {
  destination = "/vault/backend/.env.key"
  contents = <<EOF
{{ with secret "secret/data/backend" }}
RESEND_API_KEY={{ .Data.data.RESEND_API_KEY }}
CLIENT_ID={{ .Data.data.CLIENT_ID }}
CLIENT_SECRET={{ .Data.data.CLIENT_SECRET }}
SECRET_KEY={{ .Data.data.SECRET_KEY }}
{{ end }}
EOF
}

template {
  source      = "/vault/config/templates/data-source-postgres.ctmpl"
  destination = "/vault/postgres_exporter/.env.exporter"
  perms       = "0644"
}

template {
  source      = "/vault/config/templates/grafana_ini.ctmpl"
  destination = "/vault/grafana/grafana.ini"
  perms       = "0644"
}


exit_after_auth = false
