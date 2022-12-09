from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.database import get_db
from . import models
from . import schemas


router = APIRouter(prefix="/blog/api/v1", tags=["Blog"])


@router.get('/post/')
def post_list(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return JSONResponse(content=jsonable_encoder(posts), status_code=status.HTTP_200_OK)


@router.get('/post/{id}/')
def post_detail(id: int, db: Session = Depends(get_db)):
    # raise HTTPException(status_code=500,detail="details are missing")
    post_obj = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_obj:
        raise HTTPException(status_code=404, detail="post not found")
    return JSONResponse(content=post_obj.json(), status_code=status.HTTP_200_OK)


@router.post('/post/')
def post_create(request: schemas.PostSchema, db: Session = Depends(get_db)):
    post_obj = models.Post(title=request.title, content=request.content)
    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)
    return JSONResponse(jsonable_encoder(post_obj), status_code=status.HTTP_201_CREATED)


@router.put('/post/{id}/')
def post_update(id: int, request: schemas.PostSchema, db: Session = Depends(get_db)):
    post_obj = db.query(models.Post).filter(models.Post.id == id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.update(request.dict())
    db.commit()
    return JSONResponse(content=jsonable_encoder(post_obj.first()), status_code=status.HTTP_202_ACCEPTED)


@router.patch('/post/{id}/')
def post_partial_update(id: int, request: schemas.PostUpdateSchema, db: Session = Depends(get_db)):
    post_obj = db.query(models.Post).filter(models.Post.id == id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.update(request.dict(exclude_unset=True))
    db.commit()
    return JSONResponse(content=jsonable_encoder(post_obj.first()), status_code=status.HTTP_202_ACCEPTED)


@router.delete('/post/{id}/')
def post_delete(id: int, db: Session = Depends(get_db)):
    post_obj = db.query(models.Post).filter(models.Post.id == id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.delete(synchronize_session=False)
    db.commit()
    return
