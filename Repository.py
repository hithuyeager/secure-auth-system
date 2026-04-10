import database


class Repo:
    #function to add username,password into database
    async def add_user(self,username: str, password: str):
        async with database.pool.acquire() as connection:
            result = await connection.fetchval(
                "INSERT INTO users_auth (username, password) VALUES ($1,$2) RETURNING id",
                username,
                password,
            )
            return result
    #function to get password from database
    async def fetch_password(self,username: str):
        async with database.pool.acquire() as connection:
            password = await connection.fetchval(
                " SELECT password FROM users_auth WHERE username = $1",username
            )
            return password
    #function to check if username exists in database
    async def check_username(self,username: str):
        async with database.pool.acquire() as connection:
            result = await connection.fetchval(
                "SELECT COUNT(*) FROM users_auth WHERE username = $1",username
            )
            return result > 0
    async def get_user_id(self,username: str):
        async with database.pool.acquire() as connection:
            id = await connection.fetchval("SELECT id FROM users_auth WHERE username = $1",username)
            return id
    async def update_refresh_token(self,user_id: str,refresh_token: str):
        async with database.pool.acquire() as connection:
            await connection.execute( """ UPDATE users_auth 
                                     SET refresh_token = $1 
                                     WHERE id = $2""",
                                     refresh_token,
                                     user_id
                                     )
    async def get_hashed_refresh_token(self,user_id):
        async with database.pool.acquire() as connection:
            hashed_refresh_token = await connection.fetchval(" SELECT refresh_token FROM users_auth WHERE id = $1",user_id )
            return hashed_refresh_token
    async def get_username(self,user_id: str):
        async with database.pool.acquire() as connection:
            user_name =await connection.fetchval("SELECT username FROM users_auth WHERE id = $1",user_id)
            return user_name
        
              
            