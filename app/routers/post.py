from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from fastapi.openapi.models import Response
from sqlalchemy import  func
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, models, oauth2
from app.database import get_db
from app.schemas import PostCreate


router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int =10, skip: int =0, search: Optional[str] = ""):

    #Filtro para pegar somente o post do usuário logado
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
             join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).
             group_by(models.Post.id).
             filter(models.Post.title.contains(search)).limit(limit).offset(skip).
             all())

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
            join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).
            group_by(models.Post.id).
            filter(models.Post.id == id).
            first())

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id}, not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  current_user:  int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id}, not exist")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of post with id: {id}")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id}, not exist")

    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of post with id: {id}")

    updated_post.update(post.model_dump())
    db.commit()
    return updated_post.first()