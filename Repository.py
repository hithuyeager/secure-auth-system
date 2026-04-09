from database import pool


class Repo:
    #function to add username,password into database
    async def add_user(self,username: str, password: str):
        async with pool.acquire() as connection:
            await connection.fetchval(
                "INSERT INTO auth_table (username, password) VALUES ($1,$2) RETURNING id",
                username,
                password
            )
    #function to get password from database
    async def fetch_password(self,username: str):
        async with pool.acquire() as connection:
            password = await connection.fetchoneval(
                " SELECT password FROM users_auth WHERE username = $1",username
            )
            return password
    #function to check if username exists in database
    async def check_username(self,username: str):
        async with pool.acquire() as connection:
            result = await connection.fetchoneval(
                "SELECT COUNT(*) FROM users_auth WHERE username = $1",username
            )
            return result > 0