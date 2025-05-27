from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .middleware import register_middleware
from .errors import register_all_errors

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server has been stopped.")

version = "v1"

app = FastAPI(
    version=version,
    title="Bookly",
    description="A REST API for book review web service",
    # lifespan=life_span
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact={
        "email":"ankitparkhi16@gmail.com"
    },
    openapi_url=f"/api/{version}/openapi.json",
)

register_all_errors(app)
register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])