import os
import logging
import pymssql
from dotenv import load_dotenv


load_dotenv(".env")
config = {"user": os.getenv("USER_MSSQL"),
          "password": os.getenv("PASS_MSSQL"),
          "host": os.getenv("HOST_MSSQL"),
          "database": os.getenv("DB_MSSQL")}


class DatabaseMSSQL:

    def __init__(self, url=None):

        self.conn = None
        self.cursor = None

        if url:
            self.open(url)

        # Create a SQL Server database connection.

        def open(self):
            ''' 
            Take inputs server instance name, database name, username and password 
            Return a SQL Server database connection 
            '''
            self.conn = pymssql.connect(**config)
            self.cursor = self.conn.cursor()

            logging.info("Conexión {} creada".format(config["database"]))

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

        def query(self, sql, kwargs=False):

            if kwargs:
                self.cursor.execute(sql, kwargs)
            else:
                self.cursor.execute(sql)

            self.conn.commit()
            return self.cursor
