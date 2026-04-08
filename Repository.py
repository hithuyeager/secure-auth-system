from database import pool


class Repo:
    #function to add password into database
    async def add_password(self,password: str, username: str):
        async with pool.acquire() as connection:
            await connection.execute(
                "INSERT INTO auth_table (username, password) VALUES ($1, $2)",
                username,
                password
            )