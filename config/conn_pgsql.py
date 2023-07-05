import os
import sys
import logging
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv(".env")
config = {"user": os.getenv("USER_POSTGRESQL"),
          "password": os.getenv("PASS_POSTGRESQL"),
          "host": os.getenv("HOST_POSTGRESQL"),
          "port": os.getenv("PORT_POSTGRESQL"),
          "database": os.getenv("DB_POSTGRESQL")}


class DatabasePGSQL:
    #######################################################################

    def __init__(self, url=None):

        self.conn = None
        self.cursor = None

        if url:
            self.open(url)

    #######################################################################

    def open(self):

        self.conn = psycopg2.connect(**config)

        self.cursor = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        logging.info("Conexión {} creada".format(config["database"]))

    #######################################################################

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            logging.info("Conexión {} cerrada".format(config["database"]))

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()

    #######################################################################

    def get(self, table, columns, limit=None):

        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows)-limit if limit else 0:]

    #######################################################################

    def getLast(self, table, columns):

        return self.get(table, columns, limit=1)

    #######################################################################

    def write(self, table, columns, data, kwargs):

        try:
            query = "INSERT INTO %s ( %s ) VALUES ( %s )" % (
                table, columns, data)

            self.cursor.execute(query, kwargs)
            self.conn.commit()
            return True
        except Exception as error:
            logging.error("Eror al grabar los datos")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                          format(error, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
            try:
                print("entra 1")
                print("error write ", error)
                self.cursor.execute(query, list(kwargs.values()))
                self.conn.commit()
                return True
            except Exception as error2:
                print("entra 2")
                print("error write ", error2)
                self.cursor.execute(query, list(kwargs))
                self.conn.commit()
                return True

    #######################################################################

    def query(self, sql, kwargs=False):
        try:
            if kwargs:
                self.cursor.execute(sql, kwargs)
            else:
                self.cursor.execute(sql)

            self.conn.commit()
            return self.cursor
        except Exception as error:
            print(error)