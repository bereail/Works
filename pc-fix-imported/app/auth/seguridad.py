from passlib.context import CryptContext

_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    return _contexto.hash(password)


def verificar_password(password: str, hash_guardado: str) -> bool:
    return _contexto.verify(password, hash_guardado)
