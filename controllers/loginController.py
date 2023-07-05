from fastapi import APIRouter, Depends, status

from consultas.loginConsultas import post_login, pass_md5, version_apk,oUser2_login,token_generator,preregistro,token_add
from fastapi.responses import JSONResponse
from datetime import datetime
from modelos.models import DependencyClass
from modelos.loginModels import LoginModel

import json
import os
import sys
import logging

router = APIRouter(
    prefix="/api",
    tags=["loginController"],
    responses={404: {"description": "Not found"}},
)
dependency = DependencyClass()

def xstr(s):
    return '' if s is None else str(s)

@router.post("/login")
async def loginapp(datos: LoginModel, r=Depends(dependency.sync_dep)):
    datos_form = datos.dict(exclude_unset=True)

    try:

        logging.info("datos_form: {}".format(datos_form))
        datos_form['password']=pass_md5(datos_form['password'])  
         
        oUser = post_login(datos_form)
        #print(oUser)
        version=version_apk()
    
        resp = {}

        if oUser != None:
            oUser=dict(oUser)
            
            resp['version']=version[0]
            resp['error']="0"
            resp['errorDesc']=""
            oUser2=oUser2_login(str(oUser['userid']))
            #print(oUser)
            token =token_generator()
            #FALTA GAURDAR TOEKN EN o_token
            token_form={}
         
            token_form['createat']  =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            token_form['updateat']  =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            token_form['token'] = token
            token_form['userid']  = oUser['userid']

            save_token=token_add(token_form)
            esPreregistro = preregistro(datos_form['username'])
            
            resp['message'] = """{}|{}|{}|{}|{}|{}|{}|{}|{}""".format(oUser['perfil'],token,oUser2['name'],xstr(oUser['imagen']),
                                xstr(oUser['personaid']),str(esPreregistro),xstr(oUser['personaid']),xstr(oUser['estado']),xstr(oUser['estadotxt']))
                
            resp['dateRec']  =datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            resp['dateResp']  =datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
            return JSONResponse(status_code=status.HTTP_200_OK, content=dict(resp))
        else:
            resp['error'] = 2
            resp['errorDesc'] = "Error de usuario y/o contraseña"
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=dict(resp))
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))

        resp['error'] = 1
        resp['errorDesc'] = err
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=dict(resp))

