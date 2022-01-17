from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# This class inherits the pydantic Basemodel
# which we have used for setting the content of some request like post request
class UserCreate(BaseModel):
    email: EmailStr         # we use this EmailStr class to validate a proper email
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # defaulting the value so its optional
    # class Config:
    #     orm_mode = True

class PostCreate(PostBase):  # has also inherited the owner_id field I added now
    pass


# class PostOut(BaseModel):
#     id: int
#     title: str
#     content: str
#     created_at: datetime
#     owner_id: int
#     owner: UserOut
#     class Config:
#         orm_mode = True

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner: UserOut
    class Config:
        orm_mode = True
# The last two lines above allows any object referencing the PostOut model with these attributes
# to now be treated or converted to a dictionary, since results in the main file like new_post, post
# return dictionaries i.e: {title:some title, content: some content}

class PostOutWithVote(BaseModel):
    Post: PostOut
    votes: int
    class Config:
        orm_mode = True
# a schema for the access_token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
