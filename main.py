from fastapi import FastAPI
from database import Base, engine

from routers import auth_router, admin_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(user_router.router)