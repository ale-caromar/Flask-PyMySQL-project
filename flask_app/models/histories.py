# Importa la conexión con la base de datos desde la configuración.
from flask_app.config.mysqlconnection import connectToMySQL


# Definir la clase History
class History:
    #Inicializa una instancia de la clase History con los datos proporcionados.
    def __init__(self, data): # data es un diccionario que contiene la información de history.
        #Self permite acceder a los atributos y métodos de la instancia actual.
        self.id = data['id']
        self.reason_consult = data['reason_consult']
        self.medication = data['medication']
        self.personal_history = data['personal_history']
        self.familiar_history = data['familiar_history']
        self.personal_area = data['personal_area']
        self.social_area = data['social_area']
        self.familiar_area = data['familiar_area']
        self.occupational_area = data['occupational_area']

    @classmethod
    def add_entry(cls, formulario):
        # Define una consulta SQL para insertar un nuevo registro en la tabla 'history'
        query = """
                    INSERT INTO history (reason_consult, medication, personal_history, familiar_history,
                    personal_area, social_area, familiar_area, occupational_area, user_id, patient_id, created_at)
                    VALUES (%(reason_consult)s, %(medication)s, %(personal_history)s, %(familiar_history)s, 
                    %(personal_area)s, %(social_area)s, %(familiar_area)s, %(occupational_area)s, 
                    %(user_id)s, %(patient_id)s, NOW());
                """
        
        # Ejecuta la consulta SQL usando la función 'query_db' y pasa los datos del formulario
        # Se espera que 'formulario' contenga los campos necesarios para la inserción.
        results = connectToMySQL('lifeblue_db').query_db(query, formulario)
        
        # Devuelve el resultado de la consulta, que puede ser el ID del nuevo registro insertado.
        return results




