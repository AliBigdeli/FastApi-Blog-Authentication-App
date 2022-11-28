from fastapi import APIRouter
# from core import database



router = APIRouter(
    prefix = "/blog/api/v1",
    tags=["Blog"]
)

# get_db = database.get_db

@router.get('/post/')
def post_list():
    return {"data":[1,2,3,]}

@router.get('/post/{id}/')
def post_detail(id:int):
    return {"post":id}

@router.post('/post/')
def post_create(title,content):
    return {"title":title, "content":content}

@router.put('/post/{id}/')
def post_update(id:int,title,content):
    return {"id":id,"title":title, "content":content}

@router.patch('/post/{id}/')
def post_update(id:int,title,content):
    return {"id":id,"title":title, "content":content}

@router.delete('/post/{id}/')
def post_delete(id:int):
    return {"detail":"item has removed"}