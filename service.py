from password_hashing import hash_password,verify_password
import errors
from jwt_token_manager import token_rotation,create_refresh_token

class Service:
    def __init__(self,repo):
        self.repo = repo

    async def signin(self,username: str,password: str):
        is_exist =await self.repo.check_username(username)
        if not is_exist:
            hashed_password = hash_password(password)
            id = await self.repo.add_user(username,hashed_password)
            return id
        else: 
            raise errors.UserAlreadyExistError()



    async def login(self,username: str,password: str) :
        is_exist = await self.repo.check_username(username)
        if is_exist:
            hashed_password = await self.repo.fetch_password(username)
            is_correct_password = verify_password(password,hashed_password)
            if is_correct_password:
                return await self.repo.get_user_id(username)
            else:
                raise errors.WrongPasswordError()
        else:
            raise errors.UserNotFoundError()
        
    async def update_refresh_token(self,user_id: str , refresh_token: str):
        hashed_refresh_token = await self.repo.get_hashed_refreshed(user_id)
        is_token_valid = verify_password(refresh_token,hashed_refresh_token)
        if is_token_valid:
            data = token_rotation(refresh_token)
            new_refresh_token = data["refresh_token"]
            updating_new_refresh_token = self.repo.update_refresh_token(user_id,new_refresh_token)
            return data
        else:
            raise errors.InvalidToken()
    async def get_username(self,user_id: str):
        username = await self.repo.get_username(user_id)
        return username