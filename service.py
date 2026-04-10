from password_hashing import hash_password,verify_password
import errors

class Service:
    def __init__(self,repo):
        self.repo = repo

    async def signin(self,username: str,password: str,refresh_token: str):
        is_exist =await self.repo.check_username(username)
        if not is_exist:
            hashed_password = hash_password(password)
            hashed_refresh_token = hash_password(refresh_token)
            id = await self.repo.add_user(username,hashed_password,hashed_refresh_token)
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