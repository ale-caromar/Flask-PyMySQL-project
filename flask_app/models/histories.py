# Importa la conexión con la base de datos desde la configuración.
from flask_app.config.mysqlconnection import connectToMySQL

# Importa la clase Person
from flask_app.models.persons import Person

# Importa la clase User
from flask_app.models.users import User

# Definir la clase History
class History:
    #Inicializa una instancia de la clase History con los datos proporcionados.
    def __init__(self, data): # data es un diccionario que contiene la información de history.
        #Self permite acceder a los atributos y métodos de la instancia actual.
        self.id = data['id']
        self.reason_consult = data['reason_consult']
        self.medication = data['medication']
        self.personal_history = data['personal_history']
        self.personal_area = data['personal_area']
        self.social_area = data['social_area']
        self.familiar_area = data['familiar_area']
        self.occupational_area = data['occupational_area']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


