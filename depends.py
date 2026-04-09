from service import Service
from Repository import Repo

def get_user_service():
    repo = Repo()
    service = Service(repo)
    return service
