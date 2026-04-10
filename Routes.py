from fastapi import APIRouter,Depends,status
from service import Service
from depends import get_user_service
from schemas import User,RefreshRequest
from jwt_token_manager import get_current_user
from Repository import Repo
from password_hashing import hash_password
from jwt_token_manager import create_access_token,create_refresh_token

router = APIRouter(prefix="/users")

@router.post("/signin",status_code=status.HTTP_201_CREATED)
async def user_signin(user: User,
                      service: Service = Depends(get_user_service)
                      ):
    result = await service.signin(user.username,user.password)
    return {"message" : "success"}
@router.post("/login")
async def user_login(user: User,
                     service: Service = Depends(get_user_service)
                     ):
    id = await service.login(user.username,user.password)
    access_token = create_access_token({"sub" : str(id)})
    refresh_token = create_refresh_token({"sub" : str(id)})
    await Repo().update_refresh_token(id,hash_password(refresh_token))
    return {
        "access token" : access_token,
        "refresh_token" : refresh_token,
        "token-type" : "bearer"
    }
@router.post("/refresh") 
async def refresh(body: RefreshRequest , service: Service = Depends(get_user_service) ,user_id : str = Depends(get_current_user) ):
    data = await service.update_refresh_token(user_id,body.refresh_token)
    return {
        "access token" : data["access_token"],
        "refresh_token" : data["refresh_token"],
        "token-type" : "bearer"
    }
    
@router.get("/greetings")
async def greetings(user_id: str = Depends(get_current_user), service: Service = Depends(get_user_service)):
    username = await service.get_username(user_id)
    return {
        "message" : f"hi {username} , How are you <3"
    }



