from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas
import models  # I'm importing all models for the tables I've created for use Here
from database import get_db
from sqlalchemy.orm import session
from routers import oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def vote(vote: schemas.Vote, db: session = Depends(get_db),
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {vote.post_id}")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    # search the vote table, its columns to see if an entry of Post_id, User_id has been made
    # in other words, if the user has liked the post whose id is provided
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has already voted")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote!"}
        # so if the vote was not found, we create a vote for this user
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you have not voted on this post")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "successfully deleted vote"}
