def get_auth_provider(access_token):
    if "." in access_token:
        return "internal"
    return "intra"
