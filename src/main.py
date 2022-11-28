from fastapi import FastAPI
from fastapi.responses import RedirectResponse
# from core.database import engine
from blog import router as blog_router
from account import router as account_router
from core.meta_tags import tags_metadata


app = FastAPI(
    title="Simple Blog Api",
    description="this is a simple blog app with minimal usage of authentication and post managing",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ali Bigdeli",
        "url": "https://alibigdeli.github.io/",
        "email": "bigdeli.ali3@gmail.com",
    },
    license_info={
        "name": "MIT"
    },
    openapi_tags=tags_metadata
)


# models.Base.metadata.create_all(engine)

app.include_router(blog_router.router)
app.include_router(account_router.router)
