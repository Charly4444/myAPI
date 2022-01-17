from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):  # a function to return our hashed pwd
    return pwd_context.hash(password)
# we create a Cryptographic object and use it's hashing method to hash our pwd

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
