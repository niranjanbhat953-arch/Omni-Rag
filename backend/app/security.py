from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from jose import JWTError, jwt
from .settings import get_settings

settings = get_settings()
hasher = PasswordHasher()

class InvalidToken(Exception):
    pass

def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password(password: str, encoded: str) -> bool:
    try:
        return hasher.verify(encoded, password)
    except Exception:
        return False

def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {'sub': subject, 'type': 'access', 'exp': now + timedelta(minutes=settings.access_token_expire_minutes), 'iat': now}
    return jwt.encode(payload, settings.secret_key, algorithm='HS256')

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        if payload.get('type') != 'access' or not payload.get('sub'):
            raise InvalidToken()
        return str(payload['sub'])
    except JWTError as exc:
        raise InvalidToken() from exc
