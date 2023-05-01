from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import exc
from sqlalchemy import and_, or_, not_
from fastapi import Query
from accounts.auth.auth_bearer import JWTBearer
from core.database import get_db
from utils.paginations import add_pagination
from . import models
from . import schemas


router = APIRouter(prefix="/blog/api/v1", tags=["Blog"])


@router.get('/post/')
async def post_list(
    db: Session = Depends(get_db),
    search: str = Query(None, description='Filter by title and content'),
    page: int = Query(1, description='number of page you want to see'),
    page_size: int = Query(10, description='amount of items in each page'),
    ordering: str = Query(None, description='order items by')

):
    posts = db.query(models.PostModel)
    if search is not None:
        posts = posts.filter(
            models.PostModel.title.contains(search) | models.PostModel.content.contains(search))

    if ordering is not None:
        try:
            posts = posts.order_by(text(ordering))
        except exc.SQLAlchemyError:
            pass
    
    posts = posts.filter( models.PostModel.is_published == True)
    
    posts, total_items, total_pages = add_pagination(posts, page, page_size)

    posts = posts.all()
    results = [jsonable_encoder(
        schemas.PostResponse.from_orm(post)) for post in posts]
    return JSONResponse(content={
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "results": results,
    }, status_code=status.HTTP_200_OK)


@router.get('/post/{id}/')
async def post_detail(id: int, db: Session = Depends(get_db)):
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id,models.PostModel.is_published == True).first()
    if not post_obj:
        raise HTTPException(status_code=404, detail="post not found")
    return JSONResponse(content=jsonable_encoder(schemas.PostResponse.from_orm(post_obj)), status_code=status.HTTP_200_OK)


@router.get('/user/post/')
async def post_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(JWTBearer()),
    search: str = Query(None, description='Filter by title and content'),
    page: int = Query(1, description='number of page you want to see'),
    page_size: int = Query(10, description='amount of items in each page'),
    ordering: str = Query(None, description='order items by')
):
    posts = db.query(models.PostModel).filter(models.PostModel.user == user_id)
    if search is not None:
        posts = posts.filter(
            models.PostModel.title.contains(search) | models.PostModel.content.contains(search))

    if ordering is not None:
        try:
            posts = posts.order_by(text(ordering))
        except exc.SQLAlchemyError:
            pass

    posts, total_items, total_pages = add_pagination(posts, page, page_size)
    posts = posts.all()
    results = [jsonable_encoder(
        schemas.PostResponse.from_orm(post)) for post in posts]

    return JSONResponse(content={
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "results": results,
    }, status_code=status.HTTP_200_OK)


@router.get('/user/post/{id}/')
async def post_detail(id: int, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    # raise HTTPException(status_code=500,detail="details are missing")
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id, models.PostModel.user == user_id).first()
    if not post_obj:
        raise HTTPException(status_code=404, detail="post not found")
    return JSONResponse(content=post_obj.json(), status_code=status.HTTP_200_OK)


@router.post('/user/post/')
async def post_create(request: schemas.PostSchema, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    post_obj = models.PostModel(
        title=request.title, content=request.content, user=user_id)
    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)
    return JSONResponse(jsonable_encoder(schemas.PostResponse.from_orm(post_obj)), status_code=status.HTTP_201_CREATED)


@router.put('/user/post/{id}/')
async def post_update(id: int, request: schemas.PostSchema, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id, models.PostModel.user == user_id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.update(request.dict())
    db.commit()
    return JSONResponse(content=jsonable_encoder(post_obj.first()), status_code=status.HTTP_202_ACCEPTED)


@router.patch('/user/post/{id}/')
async def post_partial_update(id: int, request: schemas.PostUpdateSchema, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id, models.PostModel.user == user_id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.update(request.dict(exclude_unset=True))
    db.commit()
    return JSONResponse(content=jsonable_encoder(post_obj.first()), status_code=status.HTTP_202_ACCEPTED)


@router.delete('/user/post/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(id: int, db: Session = Depends(get_db), user_id: int = Depends(JWTBearer())):
    post_obj = db.query(models.PostModel).filter(
        models.PostModel.id == id, models.PostModel.user == user_id)
    if not post_obj.first():
        raise HTTPException(status_code=404, detail="post not found")
    post_obj.delete(synchronize_session=False)
    db.commit()
    return
