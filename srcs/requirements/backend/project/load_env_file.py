def load_env_file(path):
    secrets = {}
    try:
        with open(path, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    secrets[key] = value
    except FileNotFoundError:
        print(f"⚠️ Secret file did not find in: {path}")
    except Exception as e:
        print(f"❌ Error in download secrets in: {path} : {e}")
    return secrets
