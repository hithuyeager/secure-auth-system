from fastapi import FastAPI
from Routes import router
from contextlib import asynccontextmanager
from database import connect_to_db,close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db
    yield
    await close_db

app = FastAPI(lifespan=lifespan)
app.include_router(router)