# Importa la conexión con la base de datos desde la configuración.
from flask_app.config.mysqlconnection import connectToMySQL

# Definición de la clase Appointment que representa una cita
class Appointment:
    def __init__(self, data):
        # Inicializa una instancia de Appointment con los datos recibidos
        self.id = data['appointment_id']     
        self.date = data['date']               
        self.hour = data['hour']              
        self.place = data['place']             
        self.state = data['state']             
        self.patient_id = data['patient_id']   


    # Agendar una cita
    @classmethod
    def schedule_appointment(cls, formulario, user_id):
        # Consulta SQL para insertar una nueva cita en la base de datos
        query = """
            INSERT INTO appointment (date, hour, place, state, user_id, patient_id)
            VALUES (%(date)s, %(hour)s, %(place)s, %(state)s, %(user_id)s, %(patient_id)s);
        """
        
        # Añadir user_id y patient_id al formulario antes de realizar la consulta
        formulario['user_id'] = user_id

        # Ejecuta la consulta y devuelve el resultado (ID de la cita insertada)
        return connectToMySQL('lifeblue_db').query_db(query, formulario)
    

    # Ver las citas agendadas
    @classmethod
    def get_appointments(cls, user_id):
        # Consulta SQL para obtener las citas agendadas del usuario
        query = """
                SELECT 
                    appointment.*, 
                    per.first_name AS patient_first_name, 
                    per.last_name AS patient_last_name
                FROM appointment
                JOIN patient p ON appointment.patient_id = p.id
                JOIN person per ON p.person_id = per.id
                WHERE appointment.user_id = %(user_id)s;
                """
        
        # Ejecuta la consulta y devuelve las citas del usuario
        return connectToMySQL('lifeblue_db').query_db(query, {'user_id': user_id})


    # Método de clase para obtener una cita por su ID
    @classmethod
    def appointment_by_id(cls, appointment_id):
        # Consulta SQL para obtener una cita específica por su ID
        query = """SELECT 
                    a.id AS appointment_id,
                    a.date,
                    a.hour,
                    a.place,
                    a.state,
                    a.patient_id
                FROM 
                    appointment a 
                JOIN 
                    patient p ON a.patient_id = p.id 
                WHERE 
                    a.id = %(id)s;"""

        # Ejecuta la consulta y obtiene el resultado
        result = connectToMySQL('lifeblue_db').query_db(query, {'id': appointment_id})

        # Si se encuentra la cita, se retorna una instancia de Appointment
        if result:
            return cls(result[0])  # Asegúrate de que el constructor de Appointment maneje estos campos
        else:
            return None  # Devuelve None si no se encuentra la cita


    # Método para cancelar una cita
    @classmethod
    def cancel_appointment(cls, appointment_id, user_id):
        # Consulta SQL para actualizar el estado de una cita a 'Cancelada'
        query = """
            UPDATE appointment 
            SET state = 'Cancelada' 
            WHERE id = %(appointment_id)s AND user_id = %(user_id)s
        """

        # Datos a pasar a la consulta
        data = {
            'appointment_id': appointment_id,
            'user_id': user_id
        }
        # Ejecuta la consulta y devuelve el resultado
        result = connectToMySQL('lifeblue_db').query_db(query, data)
        return result


    # Método para marcar una cita como completada
    @classmethod
    def completed_appointment(cls, appointment_id, user_id):
        # Consulta SQL para actualizar el estado de una cita a 'Completada'
        query = """
            UPDATE appointment 
            SET state = 'Completada' 
            WHERE id = %(appointment_id)s AND user_id = %(user_id)s
        """

        # Datos a pasar a la consulta
        data = {
            'appointment_id': appointment_id,
            'user_id': user_id
        }
        # Ejecuta la consulta y devuelve el resultado
        result = connectToMySQL('lifeblue_db').query_db(query, data)
        return result
    
    
    # Método para reprogramar una cita
    @classmethod
    def reschedule(cls, formulario):
        # Consulta SQL para actualizar los datos de una cita existente
        query = """
                UPDATE appointment
                SET date = %(date)s, 
                    hour = %(hour)s, 
                    place = %(place)s
                WHERE id = %(appointment_id)s 
                AND user_id = %(user_id)s;
                """
        
        # Ejecuta la consulta para actualizar los datos y devuelve el resultado
        results = connectToMySQL('lifeblue_db').query_db(query, formulario)

        return results
