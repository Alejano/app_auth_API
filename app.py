import logging
from fastapi import Depends, FastAPI, status
from datetime import  timedelta

from funciones.security import  ACCESS_TOKEN_EXPIRE_MINUTES
from modelos.models import Token, DependencyClass

from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from controllers import loginController
from controllers import rc_testigosController,rc_loginController
from controllers.rc_loginController import authenticate_user,create_access_token,OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from config.logger import init_logger

from dotenv import load_dotenv
import os
load_dotenv("/.env")


#### Load logger ####
init_logger()

app = FastAPI()
dependency = DependencyClass()
origins = ["*"]

logging.info('Logging initialized.')
logging.info('API RC Starting...')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def json_default(o):
    import datetime
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


@app.get("/api/versionApp")
def read_root():
    return {"FA": os.getenv("APP_VERSION")}

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        resp={}
        resp['error'] = 1
        resp['errorDesc'] = "Incorrect username or password"
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=dict(resp))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

"""
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['usernameDummy']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/usuarios/me/", response_model=Usuario_registrado)
async def read_users_me(current_user: Usuario_registrado = Depends(get_current_active_user)):

    return jsonable_encoder(current_user)
"""
# aqui van los controler
app.include_router(rc_loginController.router)
app.include_router(rc_testigosController.router)


logging.info('API RC Started.')
