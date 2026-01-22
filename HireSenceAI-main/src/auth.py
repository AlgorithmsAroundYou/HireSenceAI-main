import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "admin": hash_password("admin"),
    "user1": hash_password("admin"),
}

def login(username: str, password: str) -> bool:
    if username in USERS:
        return USERS[username] == hash_password(password)
    return False
