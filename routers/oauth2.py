from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import schemas
from database import get_db
from sqlalchemy.orm import session
import models
from config import settings

SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ALGORITHM = settings.algorithm

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # object to pick up the token from this url


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        idn: int = payload.get("user_id")
        if not idn:
            raise credentials_exception
        token_data = schemas.TokenData(id=idn)  # using the TokenData schema to verify we have a token data within token
    except JWTError:
        raise credentials_exception
    return token_data  # return the token data when function is called, in this case the user id
# so if we finish the decomposition and get the token data then we have verified the token,
# Nothing much was done in the verification just to confirm that an expected datatype is in the token


# This function confirms that the user is logged in by confirming he has a valid token
def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate!",
                                          headers={"WWW-Authenticate": "Bearer"})
    # we now perform further confirmation, we use the extracted payload info in user_id to
    # reconfirm the existence of such a user in our database
    token_data = verify_access_token(token, credentials_exception)
    user_chek = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user_chek
# the first instance of objects related to the user_id is now being returned here as a dictionary