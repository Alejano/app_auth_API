from pydantic import BaseModel


class LoginModel(BaseModel):
    username: str
    password: str

class Usuario_registrado(BaseModel):
    userid: int
    personaid: int
    username: str
    perfilid: int
    enable:  str

class CurpModel(BaseModel):   
    nombre: str
    paterno: str
    materno: str
    ddmmyyyy: str    
    estadoid: str
    generoid: str

class ResetPassModel(BaseModel):   
    referidoid: int

class UsuarioModel(BaseModel):
    gender: str
    Name: str 
    location: str
    email: str
    Login: str      
    registered: str
    phone: str
    cell: str
    Id: int 
    picture: str
    nat: str
