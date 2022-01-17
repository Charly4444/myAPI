from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas
import models  # importing models of created tables
import utils
from database import get_db
from sqlalchemy.orm import session
from routers import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

# notice we can use the password request form to receive input still as dictionary
# to do so we no longer reference the schema as earlier
# this is another method, and it's shown below


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)
    # picked out the username field of the RequestForm and will use it later for createtoken
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    if not utils.verify(user_credentials.password, user.password):
        # so if they don't match still raise exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
