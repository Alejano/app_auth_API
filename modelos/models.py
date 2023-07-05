from pydantic import BaseModel
from typing import Union
from starlette.requests import Request
import asyncio


class Token(BaseModel):
    access_token: str
    token_type: str


class Usuarios(BaseModel):
    usuario: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Usuario_registrado(BaseModel):
    id_usuario: int
    usernameDummy: str


class DependencyClass:
    async def async_dep(self, request: Request):
        await asyncio.sleep(0)
        return False

    def sync_dep(self, request: Request):
        return True

 
