from passlib.context import CryptContext


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    # bcrypt is preferred over MD5 or SHA-256 for password storage because
    # bcrypt is intentionally slow and uses a configurable work factor,
    # making brute-force attacks more computationally expensive.
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)