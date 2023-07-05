import os
import sys
import logging
from sql.sql_strings_login import SqlStrings as SQL_STMT
import hashlib
import random
import string

try:
   from config.conn_pgsql import DatabasePGSQL
except:
   from ..config.conn_pgsql import DatabasePGSQL


def pass_md5(password):
           
    return hashlib.md5(password.encode()).hexdigest().upper()


def post_login(kwargs):
    try:
        
        query = SQL_STMT.qry_login_pgsql.format(
            kwargs['username'],kwargs['password'])
        #print(query)
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()

        return res
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err

def token_generator(size=32, chars=string.ascii_lowercase+string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


def version_apk():
    try:
        
        query = SQL_STMT.qry_version_pgsql
 
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, {}).fetchone()
       
        return res
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err

def oUser2_login(kwargs):
    try:
       
        query = SQL_STMT.qry_o_users_pgsql.format(
            str(kwargs))
        
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()
       
        return res
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err

def preregistro(kwargs):
    try:
       
        query = SQL_STMT.qry_preregistro_pgsql.format(
            str(kwargs))
        
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()
        if res:
            return 1
        else:
            return 0
        
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err



def token_add(kwargs):
    try:
        
        query = SQL_STMT.ins_token_pgsql
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        conexion.query(query, kwargs)
       
        return True
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err