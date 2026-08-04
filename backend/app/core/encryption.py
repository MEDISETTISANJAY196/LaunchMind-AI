from cryptography.fernet import Fernet
from app.core.config import settings

cipher = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt(text: str) -> str:
    return cipher.decrypt(text.encode()).decode()