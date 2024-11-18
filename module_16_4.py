# Модели данных Pydantic
# Задача "Модель пользователя":
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/users')
async def get_all_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(username: str, age: int) -> User:
    user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> List[User]:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return users
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> List[User]:
    try:
        del_user = users[user_id - 1]
        if del_user.id == user_id:
            users.remove(del_user)
            return users
        else:
            raise HTTPException(status_code=404, detail='User was not found')
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

