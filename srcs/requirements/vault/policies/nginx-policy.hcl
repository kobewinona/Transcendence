# Allow Nginx to read SSL certificate
path "secret/nginx_ssl" {
    capabilities = ["read", "list"]
}