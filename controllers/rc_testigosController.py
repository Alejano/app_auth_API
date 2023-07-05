from fastapi import APIRouter, Depends, status

from consultas.rc_testigoConsultas import ins_testigo,update_testigo,get_CuentasTestigos,get_testigos,get_imagestestigos,get_count_testigos,get_testigosREF,get_count_testigosREF,is_call_center
from fastapi.responses import JSONResponse
from datetime import datetime
from modelos.models import DependencyClass
from modelos.loginModels import Usuario_registrado
from modelos.rc_testigoModel import TestigoModel
from controllers.rc_buckets import base64tojpg,upload_fileGC,download_fileGC
from funciones.rc_utils import get_estadoid
from controllers.rc_loginController import get_current_active_user
import json
import os
import sys
import logging

router = APIRouter(
    prefix="/api/v2",
    tags=["testigosController"],
    responses={404: {"description": "Not found"}},
)
dependency = DependencyClass()


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
         ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

@router.post("/testigos")
async def testigos(info : TestigoModel ,current_user: Usuario_registrado = Depends(get_current_active_user)):
	#print("LLego")
	#print(info)
	try:
		cliente_data = info.dict(exclude_unset=True)
		cliente_data['userid']=current_user['userid']
		#cliente_data['estado']="Ciudad de México"
		cliente_data['createdat']=datetime.now()
		#print(cliente_data['estado'])
		if cliente_data['estado'] not in range(24,59): 
			cliente_data['estado']=get_estadoid(normalize(str(cliente_data['estado']).upper()))

		#await
  
		#call = { "userid":cliente_data['userid'],"origentestigoid":cliente_data["origentestigoid"]}
		#call_response = await is_call_center(call)
		#print(call_response)
		#cliente_data['origentestigoid'] = call_response
		response = ins_testigo(cliente_data)
		
		catalogos_lista = []
		if response:
			
			for cata in response:                
				catalogos_lista.append(dict(cata))
    
			#print(catalogos_lista)
   
			temp_imgs=[]
			for key in cliente_data.keys():
				if "img" in key and cliente_data[key]!="":
					filename=base64tojpg(cliente_data[key])
					if filename is not False:
						
						temp_imgs.append(os.path.abspath('img_testigos/'+filename))
			#print(catalogos_lista[0]["testigoid"])
			#list_files =[]
			#list_files.append("../img_testigos/"+ base64tojpg(newjpgtxt))


			update=upload_fileGC(temp_imgs,catalogos_lista[0]["inserta_o_testigo"])
			update["testigoid"]=catalogos_lista[0]["inserta_o_testigo"]
			#print(update)
			update_testigo(update)

			#testigosCount = {}
			response=get_CuentasTestigos({"userid":cliente_data['userid']})
			suma=0
			for l in response:
				valor = l[0].replace("(","").replace(")","").replace("\"","").split(",")
				#[valor[0]] = valor[1]
				suma=int(valor[1])+suma
			

			#testigosCount["TOTAL"] = str(suma)
			return JSONResponse(status_code=status.HTTP_200_OK, content={"respuesta":str(suma)})
		else:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "error"})
	except Exception as err:				
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
						format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "error"})

@router.get("/testigos")
async def getTestigos(limite: int,pagina: int,testigoid: str,nombre_user: str,nombre_referente: str,tipopublicidadid: str,estadoid: str,fechaini: str,fechafin: str,tipocapturaid: str,current_user: Usuario_registrado = Depends(get_current_active_user)):
    
	try:
				
		response=get_testigos({"limite":limite,"pagina":pagina,"testigoid": testigoid,"userid": current_user[0],"nombre_user": nombre_user,"nombre_referente": nombre_referente,"tipopublicidadid": tipopublicidadid,"estadoid": estadoid,"fechaini": fechaini,"fechafin": fechafin,"origencapturaid": tipocapturaid})
		catalogos_lista = []
		if response:
			for cata in response:
				catalogos_lista.append(json.loads(json.dumps(dict(cata), default=str)))				
			
			return JSONResponse(status_code=status.HTTP_200_OK, content=catalogos_lista)
		
	except Exception as err:
		print(err)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
    		format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")

@router.get("/testigosCount")
async def getCountTestigos(testigoid: str,nombre_user: str,nombre_referente: str,tipopublicidadid: str,estadoid: str,fechaini: str,fechafin: str,tipocapturaid: str,current_user: Usuario_registrado = Depends(get_current_active_user)):
    
	try:
		
		response=get_count_testigos({"testigoid": testigoid,"userid": current_user[0],"nombre_user": nombre_user,"nombre_referente": nombre_referente,"tipopublicidadid": tipopublicidadid,"estadoid": estadoid,"fechaini": fechaini,"fechafin": fechafin,"origencapturaid": tipocapturaid})
		catalogos_lista = {}
		if response:
			for cata in response:
				catalogos_lista=(json.loads(json.dumps(dict(cata), default=str)))
			
			return JSONResponse(status_code=status.HTTP_200_OK, content=catalogos_lista)
		
	except Exception as err:
		print(err)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
    		format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")

@router.get("/testigosREF")
async def getTestigosREF(limite: int,pagina: int,testigoid: str,nombre_user: str,nombre_referente: str,tipopublicidadid: str,estadoid: str,fechaini: str,fechafin: str,tipocapturaid: str,current_user: Usuario_registrado = Depends(get_current_active_user)):
    
	try:
				
		response=get_testigosREF({"limite":limite,"pagina":pagina,"testigoid": testigoid,"userid": current_user[0],"nombre_user": nombre_user,"nombre_referente": nombre_referente,"tipopublicidadid": tipopublicidadid,"estadoid": estadoid,"fechaini": fechaini,"fechafin": fechafin,"origencapturaid": tipocapturaid})
		catalogos_lista = []
		if response:
			for cata in response:
				catalogos_lista.append(json.loads(json.dumps(dict(cata), default=str)))
			
			return JSONResponse(status_code=status.HTTP_200_OK, content=catalogos_lista)
		
	except Exception as err:
		print(err)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
    		format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")

@router.get("/testigosCountREF")
async def getCountTestigosREF(testigoid: str,nombre_user: str,nombre_referente: str,tipopublicidadid: str,estadoid: str,fechaini: str,fechafin: str,tipocapturaid: str,current_user: Usuario_registrado = Depends(get_current_active_user)):
    
	try:
		
		response=get_count_testigosREF({"testigoid": testigoid,"userid": current_user[0],"nombre_user": nombre_user,"nombre_referente": nombre_referente,"tipopublicidadid": tipopublicidadid,"estadoid": estadoid,"fechaini": fechaini,"fechafin": fechafin,"origencapturaid":tipocapturaid})
		catalogos_lista = {}
		if response:
			for cata in response:
				catalogos_lista=(json.loads(json.dumps(dict(cata), default=str)))
			
			return JSONResponse(status_code=status.HTTP_200_OK, content=catalogos_lista)
		
	except Exception as err:
		print(err)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
    		format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")


@router.get("/getimgTestigo")
async def getImgsTestigos(testigo: int,current_user: Usuario_registrado = Depends(get_current_active_user)):
	try:		
		response=get_imagestestigos({"testigo":testigo})
		catalogos_lista = []
		index = 1
		name_file={}
		if response:
			for cata in response:
				#catalogos_lista.append(json.loads(json.dumps(dict(cata), default=str)))
				name_file = json.loads(json.dumps(dict(cata), default=str))
				#print(name_file)
				for name in name_file:
					#print(name)
					if(name_file[name]):
						download=download_fileGC(name_file[name])
						#type(download)
						catalogos_lista.append({"data"+str(index):download})
						index = index + 1
					
			
			return JSONResponse(status_code=status.HTTP_200_OK, content=catalogos_lista)
		
	except Exception as err:
		print(err)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
    		format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
		print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")


@router.get("/getCuentasTestigos")
#se arma sin MODELO porque es un GET, solo uso la variable telefono
async def getCuentasTestigos(userid: int):
    try:
        testigosCount = {}
        response=get_CuentasTestigos({"userid":userid})
        suma=0
        for l in response:
            valor = l[0].replace("(","").replace(")","").replace("\"","").split(",")
            testigosCount[valor[0]] = valor[1]
            suma=int(valor[1])+suma
          

        testigosCount["TOTAL"] = str(suma)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"respuesta":testigosCount})
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
            format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        print('{} | Error de tipo {} en el archivo {}, línea: {}'.format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))  
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="error api")
    
    