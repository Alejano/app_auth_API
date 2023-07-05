from fastapi import APIRouter, Depends, status,HTTPException,Request
 
from consultas.rc_loginConsultas import post_login,post_user, pass_md5,cambia_pass
from fastapi.responses import JSONResponse
from datetime import datetime
from modelos.models import DependencyClass
from modelos.loginModels import Usuario_registrado,CurpModel,ResetPassModel,UsuarioModel
from modelos.models import Token, Usuarios, TokenData
from funciones.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from json import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from funciones.maincurp import generarCurp
from funciones.rc_utils import get_estadocurp

import json
import os
import sys
import logging


router = APIRouter(
    prefix="/api/v2",
    tags=["loginController"],
    responses={404: {"description": "Not found"}},
)
dependency = DependencyClass()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def xstr(s):
    return '' if s is None else str(s)


def check_user(username: str):

    datos_form={}
    datos_form['username']=username.rstrip().lstrip()
    #datos_form['password']=pass_md5(password.rstrip().lstrip()) 
    print("va check")
    oUser = post_user(datos_form)
    print(oUser)
    return oUser
     

def authenticate_user(username: str, password: str):
    user = check_user(username)
    if not user:
        return False
    datos_form={}
    datos_form['username']=username.rstrip().lstrip()
    datos_form['password']=pass_md5(password.rstrip().lstrip()) 

    login=post_login(datos_form)
    print("login",login)
    if not login:
        return False
    #if not verify_password(password, user['password']):
    #    return False,
    
    return login


def get_current_active_user(token: str = Depends(oauth2_scheme)) -> Usuarios:
    # skipping for simplicity...
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
        user = check_user(token_data.username)
       
        return user

    except JWTError:
        pass
   

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/me/", response_model=Usuario_registrado)
async def read_users_me(current_user: Usuario_registrado = Depends(get_current_active_user)):
    try:
        current_user=json.loads(json.dumps(dict(current_user), default=str))
        return JSONResponse(status_code=status.HTTP_200_OK, content=current_user)
    except:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"error":"error"})


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        resp={}
        resp['error'] = 1
        resp['errorDesc'] = "Incorrect username or password"
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=dict(resp))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer","username":user['username']}

@router.post("/registro", response_model=Token)
async def registro(form_data: UsuarioModel):
    print(form_data)
    
    return {"ok": True}
