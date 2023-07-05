git clone https://github.com/krenfermo/fastapi_prueba

cd fastapi_prueba

python -m pip install virtualenv 

python -m virtualenv env_api
# o segun version 
python3 -m virtualenv env_api

source env_api/bin/activate

pip install -r requerimientos.txt

uvicorn app:app --reload --port 8080 --host 0.0.0.0

navegar http://127.0.0.1:8080 

hacer LOGIN EN ESQUINA SUPERIOR DERECHA LOGO VERDE " AUTHORIZE"
USERNAME:  usuario
pass:  loquesea
CLOSE

probar ahi usuarios/me/

Navegar en otra pestaña http://127.0.0.1:8080/google/login
    Despues de hacer login, regresa un HTTPS, SOLO BORRAREL HTTPS Y DEJAR HTTPS Y DAR ENTER

Navegar en otra pestaña http://127.0.0.1:8080/fb/login
    Despues de hacer login, regresa un HTTPS, SOLO BORRAREL HTTPS Y DEJAR HTTPS Y DAR ENTER



