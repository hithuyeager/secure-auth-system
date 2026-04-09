from fastapi import FastAPI,Request
from Routes import router
from contextlib import asynccontextmanager
from database import connect_db,close_db
from fastapi.responses import JSONResponse
from errors import AppError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request,exc: AppError):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "status" : "error",
            "message" : exc.message
        }
    )
