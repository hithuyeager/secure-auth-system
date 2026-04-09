import database


class Repo:
    #function to add username,password into database
    async def add_user(self,username: str, password: str):
        async with database.pool.acquire() as connection:
            result = await connection.fetchval(
                "INSERT INTO users_auth (username, password) VALUES ($1,$2) RETURNING id",
                username,
                password
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