#Importar la app desde el __init__
from flask_app import app

#Importar controlador de users 
from flask_app.controllers import users_controller
#Importar controlador de patients
from flask_app.controllers import patients_controller
#Importar el controlador de agenda
from flask_app.controllers import appointment_controller
#Importar el controlador de historias clínicas
from flask_app.controllers import histories_controller

#Ejecuta la aplicación
if __name__ == "__main__": #verifica si el script se está ejecutando directamente o si se está importando en otro módulo.
    app.run (debug = True) #app.run pone en marcha el servidor y debug activa el modo depuración

