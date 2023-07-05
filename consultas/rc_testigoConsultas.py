import os
import sys
import logging
from sql.rc_sql_testigos import SqlStrings as SQL_STMT

try:
   from config.conn_pgsql import DatabasePGSQL
except:
   from ..config.conn_pgsql import DatabasePGSQL

def update_testigo(kwargs):
    try:
       
 
        query = SQL_STMT.update_testigos_pgsql.format(
            kwargs['img1'],kwargs['img2'],kwargs['img3'],kwargs['img4'],
   kwargs['img5'], kwargs['img6'], kwargs['img7'], kwargs['img8'],
    kwargs['img9'], kwargs['img10'], kwargs['testigoid'])
        logging.info('Query: {}'.format(query))
        #print(query)
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query)
   
        return True
    except Exception as err:
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err
def is_call_center(kwargs):
    """
    recibe catalogo
    devuelve datos catalogo
    """
    try:
               
        is_call = SQL_STMT.is_call_center.format( kwargs['userid'],kwargs["origentestigoid"])
        conexion = DatabasePGSQL()
        conexion.open()
        origentestigoid = conexion.query(is_call)
        
        print(is_call)
        print(origentestigoid)
        return origentestigoid
    except Exception as err:
 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err
    
def ins_testigo(kwargs):
    """
    recibe catalogo
    devuelve datos catalogo
    """
    try:
       
        query = SQL_STMT.ins_testigos_pgsql.format(
             kwargs['userid'],
  kwargs['direccion'], kwargs['lat'], kwargs['lon'], kwargs['endireccion'], kwargs['estado'],
  kwargs['municipio'],kwargs['tipopublicidad'],kwargs['fecha'], kwargs['personaje'], kwargs['categoria'],
    kwargs['partidos'], kwargs['createat'], kwargs['lat2'], kwargs['lon2'],  kwargs['verificadofecha2'],  kwargs['idreferencia'] ,kwargs['placeid'], kwargs['origentestigoid']
             )
        logging.info('Query: {}'.format(query))
        
        conexion = DatabasePGSQL()
        conexion.open()       
        rec = conexion.query(query)
        #print(query)
        return rec
    except Exception as err:
 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(err, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
        return err

def get_testigos(kwargs):
    try:
        #print(kwargs)
        #["testigoid"],["userid"],["nombre_user"],["nombre_referente"],["tipopublicidadid"],["estadoid"],["fechaini"],["fechafin"]	

        
        if( kwargs["limite"] !='null' ): kwargs["limite"] = str(kwargs["limite"])
        if( kwargs["pagina"] !='null' ): kwargs["pagina"] = str(kwargs["pagina"])
        if( kwargs["testigoid"] !='null' ): kwargs["testigoid"] = str(kwargs["testigoid"])
        if( kwargs["userid"] !='null' ): kwargs["userid"] = str(kwargs["userid"])
        if( kwargs["nombre_user"] !='null' ): kwargs['nombre_user'] = "'"+kwargs['nombre_user']+"'"
        if( kwargs["nombre_referente"] !='null' ): kwargs['nombre_referente'] = "'"+kwargs['nombre_referente']+"'"
        if( kwargs["tipopublicidadid"] !='null' ): kwargs["tipopublicidadid"] = str(kwargs["tipopublicidadid"])
        if( kwargs["estadoid"] !='null' ): kwargs["estadoid"] = str(kwargs["estadoid"])
        if( kwargs["fechaini"] !='null' ): kwargs["fechaini"] = "'"+kwargs["fechaini"]+"'"
        if( kwargs["fechafin"] !='null' ): kwargs["fechafin"] = "'"+kwargs["fechafin"]+"'"
        if( kwargs["origencapturaid"] !='null' ): kwargs["origencapturaid"] = str(kwargs["origencapturaid"])
    
       	        
        #query = SQL_STMT.get_Testigos.format(kwargs["limite"],kwargs["pagina"],kwargs["testigoid"],kwargs["userid"],
        # kwargs["nombre_user"],kwargs["nombre_referente"],kwargs["tipopublicidadid"],kwargs["estadoid"],
        # kwargs["fechaini"],kwargs["fechafin"]);
        query = """SELECT * from redesc.get_testigos_search_pages(
            """+kwargs["limite"]+""",
            """+kwargs["pagina"]+""",
            """+kwargs["testigoid"]+""",
            """+kwargs["userid"]+""",
            """+kwargs["nombre_user"]+""",
            """+kwargs["nombre_referente"]+""",
            """+kwargs["tipopublicidadid"]+""",
            """+kwargs["estadoid"]+""",
            """+kwargs["fechaini"]+""",
            """+kwargs["fechafin"]+""",
            """+kwargs["origencapturaid"]+""");"""	
        
        
        #print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err

def get_count_testigos(kwargs):
    try:
        
        if( kwargs["testigoid"] !='null' ): kwargs["testigoid"] = str(kwargs["testigoid"])
        if( kwargs["userid"] !='null' ): kwargs["userid"] = str(kwargs["userid"])
        if( kwargs["nombre_user"] !='null' ): kwargs['nombre_user'] = "'"+kwargs['nombre_user']+"'"
        if( kwargs["nombre_referente"] !='null' ): kwargs['nombre_referente'] = "'"+kwargs['nombre_referente']+"'"
        if( kwargs["tipopublicidadid"] !='null' ): kwargs["tipopublicidadid"] = str(kwargs["tipopublicidadid"])
        if( kwargs["estadoid"] !='null' ): kwargs["estadoid"] = str(kwargs["estadoid"])
        if( kwargs["fechaini"] !='null' ): kwargs["fechaini"] = "'"+kwargs["fechaini"]+"'"
        if( kwargs["fechafin"] !='null' ): kwargs["fechafin"] = "'"+kwargs["fechafin"]+"'"
        if( kwargs["origencapturaid"] !='null' ): kwargs["origencapturaid"] = str(kwargs["origencapturaid"])
    
        #print(kwargs)
        #["testigoid"],["userid"],["nombre_user"],["nombre_referente"],["tipopublicidadid"],["estadoid"],["fechaini"],["fechafin"]			
        query = """SELECT count(*) from redesc.get_testigos_search_pages(
            10000000000,
            0,
            """+kwargs["testigoid"]+""",
            """+kwargs["userid"]+""",
            """+kwargs["nombre_user"]+""",
            """+kwargs["nombre_referente"]+""",
            """+kwargs["tipopublicidadid"]+""",
            """+kwargs["estadoid"]+""",
            """+kwargs["fechaini"]+""",
            """+kwargs["fechafin"]+""",
            """+kwargs["origencapturaid"]+""");"""
        #print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err

def get_testigosREF(kwargs):
    try:
        #print(kwargs)
        #["testigoid"],["userid"],["nombre_user"],["nombre_referente"],["tipopublicidadid"],["estadoid"],["fechaini"],["fechafin"]	

        
        if( kwargs["limite"] !='null' ): kwargs["limite"] = str(kwargs["limite"])
        if( kwargs["pagina"] !='null' ): kwargs["pagina"] = str(kwargs["pagina"])
        if( kwargs["testigoid"] !='null' ): kwargs["testigoid"] = str(kwargs["testigoid"])
        if( kwargs["userid"] !='null' ): kwargs["userid"] = str(kwargs["userid"])
        if( kwargs["nombre_user"] !='null' ): kwargs['nombre_user'] = "'"+kwargs['nombre_user']+"'"
        if( kwargs["nombre_referente"] !='null' ): kwargs['nombre_referente'] = "'"+kwargs['nombre_referente']+"'"
        if( kwargs["tipopublicidadid"] !='null' ): kwargs["tipopublicidadid"] = str(kwargs["tipopublicidadid"])
        if( kwargs["estadoid"] !='null' ): kwargs["estadoid"] = str(kwargs["estadoid"])
        if( kwargs["fechaini"] !='null' ): kwargs["fechaini"] = "'"+kwargs["fechaini"]+"'"
        if( kwargs["fechafin"] !='null' ): kwargs["fechafin"] = "'"+kwargs["fechafin"]+"'"
        if( kwargs["origencapturaid"] !='null' ): kwargs["origencapturaid"] = str(kwargs["origencapturaid"])
    
              
        #query = SQL_STMT.get_Testigos.format(kwargs["limite"],kwargs["pagina"],kwargs["testigoid"],kwargs["userid"],
        # kwargs["nombre_user"],kwargs["nombre_referente"],kwargs["tipopublicidadid"],kwargs["estadoid"],
        # kwargs["fechaini"],kwargs["fechafin"]);
        query = """SELECT * from redesc.get_testigos_refs_search_pages(
            """+kwargs["limite"]+""",
            """+kwargs["pagina"]+""",
            """+kwargs["testigoid"]+""",
            """+kwargs["userid"]+""",
            """+kwargs["nombre_user"]+""",
            """+kwargs["nombre_referente"]+""",
            """+kwargs["tipopublicidadid"]+""",
            """+kwargs["estadoid"]+""",
            """+kwargs["fechaini"]+""",
            """+kwargs["fechafin"]+""",
            """+kwargs["origencapturaid"]+""");"""	
        
        
        #print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err

def get_count_testigosREF(kwargs):
    try:
        
        if( kwargs["testigoid"] !='null' ): kwargs["testigoid"] = str(kwargs["testigoid"])
        if( kwargs["userid"] !='null' ): kwargs["userid"] = str(kwargs["userid"])
        if( kwargs["nombre_user"] !='null' ): kwargs['nombre_user'] = "'"+kwargs['nombre_user']+"'"
        if( kwargs["nombre_referente"] !='null' ): kwargs['nombre_referente'] = "'"+kwargs['nombre_referente']+"'"
        if( kwargs["tipopublicidadid"] !='null' ): kwargs["tipopublicidadid"] = str(kwargs["tipopublicidadid"])
        if( kwargs["estadoid"] !='null' ): kwargs["estadoid"] = str(kwargs["estadoid"])
        if( kwargs["fechaini"] !='null' ): kwargs["fechaini"] = "'"+kwargs["fechaini"]+"'"
        if( kwargs["fechafin"] !='null' ): kwargs["fechafin"] = "'"+kwargs["fechafin"]+"'"
        if( kwargs["origencapturaid"] !='null' ): kwargs["origencapturaid"] = str(kwargs["origencapturaid"])
        
        #print(kwargs)
        #["testigoid"],["userid"],["nombre_user"],["nombre_referente"],["tipopublicidadid"],["estadoid"],["fechaini"],["fechafin"]			
        query = """SELECT count(*) from redesc.get_testigos_refs_search_pages(
            10000000000,
            0,
            """+kwargs["testigoid"]+""",
            """+kwargs["userid"]+""",
            """+kwargs["nombre_user"]+""",
            """+kwargs["nombre_referente"]+""",
            """+kwargs["tipopublicidadid"]+""",
            """+kwargs["estadoid"]+""",
            """+kwargs["fechaini"]+""",
            """+kwargs["fechafin"]+""",
            """+kwargs["origencapturaid"]+""");"""	
        #print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err
    
     
def get_imagestestigos(kwargs):
    try:
        #print(kwargs)
        query = SQL_STMT.get_imagenTestigos.format(kwargs["testigo"]);
        #print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err
    
def get_CuentasTestigos(kwargs):
    """
    recibe telefono
    devuelve datos telefono
    """
    try:
        query = SQL_STMT.get_CuentasTestigos.format(
            kwargs['userid'])
        print(query)
        logging.info('Query: {}'.format(query))
        conexion = DatabasePGSQL()
        conexion.open()
        rec = conexion.query(query).fetchall()

        return rec
    except Exception as err:
        print(err)
        return err

