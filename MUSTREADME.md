inside your system root folder  ie MARATHON_PROJECT 

To install the system make a virtual environemt

     python -m venv {env name here }

install requirements for the project ( I used pip freeze command)

    pip install requirements.tzt

_______________________________
 
SSL's were generated using openssl ..
ssl generated are inside ssl folder

Run Server with SSL capabilities

    uvicon was ussed to serve the project over https  ...

      uvicorn MARATHON_PROJECT.asgi:application --host localhost --port 8000 --ssl-keyfile ssl/server.key --ssl-certfile ssl/server.crt

Runs Server to server static files and assets

       python manage.py runserver 8001


________________________
