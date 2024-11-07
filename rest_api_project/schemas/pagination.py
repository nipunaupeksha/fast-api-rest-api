from pydantic import BaseModel
from typing import List
from schemas.user import User


class PaginatedUserReponse(BaseModel):
    totalResults: int
    itemsPerPage: int
    users: List[User]
