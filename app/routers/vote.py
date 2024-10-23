from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database, oauth2, models, schemas

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir ==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f" user {current_user.id} has already Voted on post {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfuly added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfuly deleted vote"}

