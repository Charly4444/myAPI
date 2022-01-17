from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
import schemas
import models  # I'm importing all models for the tables I've created for use Here
from database import get_db
from sqlalchemy.orm import session
import utils
from routers import oauth2

router = APIRouter(prefix="/users", tags=["users"])


# to RETRIEVE all USERS
@router.get("/", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK)
def get_users(db: session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


# to get PARTICULAR USER
@router.get("/{idn}", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
def get_user(idn: int, db: session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == idn)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User NOT Found!")
    return user


# to CREATE a USER
@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    # ,current_user: schemas.UserOut = Depends(oauth2.get_current_user)
    # I removed the above dependency so that creating a new user doesn't require being logged-in
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())  # this is like a table object and it returns a dict
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # the argument inside is to be displayed after clearing out the memory
    return new_user

# to DELETE USER
@router.delete("/{idn}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(idn: int, db: session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == idn)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {idn} does not exist!")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{idn}", response_model=schemas.UserOut, status_code=status.HTTP_202_ACCEPTED)
def update_user(idn: int, updated_user: schemas.UserCreate, db: session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    hashed_password = utils.hash(updated_user.password)
    updated_user.password = hashed_password
    user_query = db.query(models.User).filter(models.User.id == idn)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {idn} does not exist!")
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit/update this user!")
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()
