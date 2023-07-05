from datetime import timedelta
from google.cloud import storage
from base64 import b64decode
import imghdr
import base64
import uuid
import os
import pathlib
import logging
from fastapi.responses import JSONResponse
from fastapi import  status
import sys


def base64tojpg(string64):

    base64_img_bytes = string64.encode('utf-8')
    extension=get_extension(string64)
    #print(extension)
    if not extension:
        return False
    filename=   '{}.{}'.format(str(uuid.uuid4()),extension) 
    #print(filename)
    try:
        
        with open(os.path.abspath('img_testigos/'+filename), 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            #print("guarda imagen")
            file_to_save.write(decoded_image_data)
            return filename
    except Exception as err:
        print(err)
        return False


def upload_fileGC(list_files,testigoid):
    try:
        #print(os.path.abspath('controllers/creds2.json'))
        client = storage.Client.from_service_account_json(json_credentials_path=os.path.abspath('controllers/creds2.json'))
        bucket = storage.Bucket(client, 'rcimg')
        dit_img={}
        cont=1
        for str_file_name in list_files:
            head, tail = os.path.split(str_file_name)
            #print("file: ",tail)
            dit_img["img"+str(cont)]=tail
            #exit()
            # The name of file on GCS once uploaded
            blob = bucket.blob(tail)
            # Path of the local file to upload
            blob.upload_from_filename(str_file_name)
            #print("sube: ", str_file_name)
            file_to_rem = pathlib.Path(str_file_name)
            file_to_rem.unlink()
            cont=cont+1
        
        if cont<11:
            for i in range(cont, 11, 1):
                dit_img["img"+str(cont)]=""
                cont=cont+1
        return dit_img
    except Exception as err:
        print("error: ",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "error"})

def download_fileGC(file_name):
    try:
        client = storage.Client.from_service_account_json(json_credentials_path=os.path.abspath('controllers/creds2.json'))
        bucket = storage.Bucket(client, 'rcimg')
        blob = bucket.get_blob(file_name)
        #print("baja: ", blob)
        #print("baja: ", blob.public_url)
        #print("baja: ", blob.media_link)    
        blob_url = blob.generate_signed_url(expiration=timedelta(hours=1))
        #print("baja: ", blob_url)
        return blob_url
    except Exception as err:
        print("error: ",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "error"})

def download_fileGC_volantes(file_name):
    try:
        client = storage.Client.from_service_account_json(json_credentials_path=os.path.abspath('controllers/creds2.json'))
        bucket = storage.Bucket(client, 'volanteos')
        blob = bucket.get_blob(file_name)
        #print("baja: ", blob)
        #print("baja: ", blob.public_url)
        #print("baja: ", blob.media_link)    
        blob_url = blob.generate_signed_url(expiration=timedelta(hours=1))
        #print("baja: ", blob_url)
        return blob_url
    except Exception as err:
        print("error: ",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "error"})


def get_extension(file):
    decoded_string = b64decode(file)
    extension = imghdr.what(None, h=decoded_string)

    return extension

