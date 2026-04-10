from fastapi import APIRouter,Depends,status
from service import Service
from depends import get_user_service
from schemas import User

from jwt_token_manager import create_access_token,create_refresh_token

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
    access_token = create_access_token({"sub" : str(id)})
    refresh_token = create_refresh_token({"sub" : str(id)})
    id = await service.login(user.username,user.password,refresh_token)
    return {
        "access token" : access_token,
        "refresh_token" : refresh_token,
        "token-type" : "bearer"
    }

    
