import logging
import os
import sys
import os.path
import socket
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime


def init_logger():
    """ Inicializa el logger (logging nativo)
    """
    try:
        HOSTNAME = socket.gethostname()
        LOG_FILENAME = secure_filename(
            '{}_{}_api_rc.log'.format(
                datetime.now().strftime('%Y%m'), HOSTNAME))
        log_path = os.path.join(
            os.path.join(
                os.getenv('ROOT_PATH'),
                os.getenv('BASKET_DIR')),
            os.getenv('APP_LOG_DIR'))
        Path(log_path).mkdir(parents=True, exist_ok=True)
        log_file = os.path.join(log_path, LOG_FILENAME)
        FORMAT = '%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s'
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format=FORMAT
        )
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error('{} | Error de tipo {} en el archivo {}, línea: {}'.
                      format(ex, str(exc_type), str(fname), str(exc_tb.tb_lineno)))
