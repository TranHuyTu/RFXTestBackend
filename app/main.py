from fastapi import FastAPI
from . import routes

app = FastAPI()
app.include_router(router=routes.router, prefix="/api", tags=["users"])