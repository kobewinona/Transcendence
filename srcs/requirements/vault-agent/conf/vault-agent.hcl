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


exit_after_auth = false
