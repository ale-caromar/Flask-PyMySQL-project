#Importar Flask
from flask import Flask 

#Crea una instancia de flask
app = Flask (__name__)

#Establecemos una secret key
app.secret_key = "Mi llave secreta"