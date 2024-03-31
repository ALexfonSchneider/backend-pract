from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from schemes.User import User, UserCreate, UserCreatedReponse, UserRead, UserReadList, UserUpdate
from data import users

router_users = APIRouter(prefix="/users")

@router_users.get("/", response_model=UserReadList)
def get_users():
    return UserReadList(users=[UserRead(**user.dict()) for user in users])


@router_users.post("/", response_model=UserCreatedReponse)
def create_user(user: UserCreate):
    id = 0 if len(users) == 0 else users[-1].id + 1
    users.append(User(**user.dict(), id=id))
    return UserCreatedReponse(id=id)


@router_users.put("/", responses={"404": {"detail": "user does not exist"}})
def update_user(user: UserUpdate):
    user_to_update = list(filter(lambda user_in_list: user_in_list.id == user.id, users))
    if len(user_to_update) == 0:
        raise HTTPException(status_code=404, detail="user does not exist")
    user_to_update = user_to_update[0]
    for attr, value in user.dict().items():
        setattr(user_to_update, attr, value)
    return Response(status_code=200)
        

@router_users.get("/{user_id}", response_model=UserRead, responses={"404": {"detail": "user does not exist"}})
def get_user(user_id: int):
    user = list(filter(lambda user: user.id == user_id, users))
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user[0]


@router_users.delete("/{user_id}", responses={"404": {"detail": "user does not exist"}})
def delete_user(user_id: int):
    user = list(filter(lambda user: user.id == user_id, users))
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="user does not exist")
    users.remove(user[0])
    return Response(status_code=200)
    