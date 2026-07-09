@property
def github_private_key(self) -> str:
    # Check env variable first, fall back to file
    import os
    key_from_env = os.environ.get("GITHUB_PRIVATE_KEY")
    if key_from_env:
        return key_from_env
    key_path = Path(self.github_private_key_path)
    if not key_path.exists():
        raise FileNotFoundError(f"Private key not found at {key_path}")
    return key_path.read_text()
