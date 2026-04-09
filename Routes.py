from fastapi import APIRouter,Depends,status
from service import Service
from depends import get_user_service
from schemas import User

router = APIRouter(prefix="/users")

@router.post("/signin",status_code=status.HTTP_201_CREATED)
async def user_signin(user: User,
                      service: Service = Depends(get_user_service)
                      ):
    result = await service.signin(user.username,user.password)
    return result
@router.post("/login")
async def user_login(user: User,
                     service: Service = Depends(get_user_service)
                     ):
    result = await service.login(user.username,user.password)
    return result
