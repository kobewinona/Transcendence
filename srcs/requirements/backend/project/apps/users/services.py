from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_intra_user(intra_user_data):
    intra_id = intra_user_data.get("id")
    email = intra_user_data.get("email")
    username = intra_user_data.get("login")
    avatar = intra_user_data.get("image", {}).get("link")

    if not intra_id or not email:
        raise ValueError("Missing intra_id or email in Intra response")

    user, created = User.objects.get_or_create(
        intra_id=intra_id,
        defaults={
            "email": email,
            "username": username,
            "auth_provider": "intra",
            "avatar": avatar,
        },
    )

    # Update existing user fields if necessary
    if not created:
        updated = False
        if user.avatar != avatar:
            user.avatar = avatar
            updated = True
        if user.username != username:
            user.username = username
            updated = True
        if user.email != email:
            user.email = email
            updated = True

        if updated:
            user.save()

    return user
