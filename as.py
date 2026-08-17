def generate_jwt() -> str:
    settings = get_settings()

    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + 540,
        "iss": int(settings.github_app_id)  # must be integer not string
    }

    token = jwt.encode(
        payload,
        settings.github_private_key,
        algorithm="RS256"
    )
