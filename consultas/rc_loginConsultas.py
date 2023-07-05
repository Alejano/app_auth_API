import os
import sys
import logging
from sql.rc_sql_login import SqlStrings as SQL_STMT
import hashlib

try:
   from config.conn_pgsql import DatabasePGSQL
except:
   from ..config.conn_pgsql import DatabasePGSQL


def pass_md5(password):
           
    return hashlib.md5(password.encode()).hexdigest().upper()


def cambia_pass(kwargs):
    try:  
 
        query = SQL_STMT.qry_cambia_pass.format(
            kwargs['p_personaid'],kwargs['p_edituserid'],kwargs['p_editadt'])

        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()
        
        return res
    except Exception as err:
        print("error login",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err


def post_user(kwargs):
    try:  

        query = SQL_STMT.qry_email_pgsql.format(
            kwargs['username'])
        print(query)
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()
        
        return res
    except Exception as err:
        print("error login",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err


def post_login(kwargs):
    try:  
    
        if kwargs['password']:
                    
            query = SQL_STMT.qry_login_funcion_pgsql.format(
                kwargs['username'],kwargs['password'].upper())

        print(query)
        logging.info('Query: {}'.format(query))   
        conexion = DatabasePGSQL()
        conexion.open()
        res=conexion.query(query, kwargs).fetchone()
        
        return res
    except Exception as err:
        print("error login",err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err
