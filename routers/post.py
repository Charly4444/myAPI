from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
import schemas
import models  # importing all models for tables created
from database import get_db
from sqlalchemy.orm import session
from routers import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["posts"])


# the tags option is they just for Documentation purposes

@router.get("/home")
async def root(db: session = Depends(get_db)):
    return {"message": "Home Page"}


# t0 get ALL POSTS (assuming that we've created some posts in the table)
@router.get("/", response_model=List[schemas.PostOutWithVote])
def get_posts(db: session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # the below method show how we introduce different query parameters
    # the contains method is used to query the rows as other filter
# posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(offset).all()
    # we can filter out to get just the post owned by the logged-in user using the below instead of the above
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # return posts
    return results

# we get list of dictionaries here, so we have converted the received response model to a List
# as we have done above so that the posts is successfully matched with the response model


# to get PARTICULAR POST
@router.get("/{idn}", response_model=schemas.PostOutWithVote, status_code=status.HTTP_200_OK)
def get_posts(idn: int, db: session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == idn).first()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == idn) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {idn} not found")
    return results


# to Create a NEW POST
@router.post("/", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.id)  # just stored and printed this our token data
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # we've added extra field of owner_id to the Post schema data of user_id which we've fetched from token
    # The above is a shorthand method to convert to dictionary and unpack to produce output
    # as 'title'='post.title', 'content'='post.content','published'='post.published'
    # This serves as arguments when creating the new_post object from the models.Post class
    # to use a method like db.add, you have to input a sqlalchemy object which is what is created as
    # new post and added to the sqlalchemy created table
    db.add(new_post)  # adding the new_post to the database
    db.commit()
    db.refresh(new_post)
    return new_post


# You need to know the nature of the data you're returning that will allow you to prepare the
# response model properly to match it to avoid running into errors


# to DELETE POST
@router.delete("/{idn}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(idn: int, db: session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == idn)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {idn} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can only delete your posts")
    post_query.delete(synchronize_session=False)  # Now deleting the post
    # db.delete(post_query)  # without the above line this way also works
    # the important Note is that you can't use two methods so if you're using a delete method
    # then, you have to remove the .first method to attach/include the delete method that is
    # only the plain query will be passed into a particular method not a method
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# remember that once you attach a method be it '.first()' or '.delete' or '.update' once
# attached to a query it executes that query but prior to that the query is still as a plain query


# to UPDATE PARTICULAR POST
@router.put("/{idn}", response_model=schemas.PostOut, status_code=status.HTTP_202_ACCEPTED)
def update_post(idn: int, upost: schemas.PostCreate, db: session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == idn)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {idn} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="sorry can only update your own post")
    post_query.update(upost.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
# When result is returned it is sent to the response model for re-shaping and then sent to Output
