# Importa la conexión con la base de datos desde la configuración.
from flask_app.config.mysqlconnection import connectToMySQL

#Importa la clase Person
from flask_app.models.persons import Person

# Importa el módulo de expresiones regulares para validaciones.
import re
# Expresión regular para validar el formato del correo electrónico.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Importa la función flash para mostrar mensajes de error o confirmación en el formulario.
from flask import flash, session

#Define la clase Patient 
class Patient(Person):
    # Constructor de la clase Patient. Inicializa los atributos de Person y agrega los de Patient.
    def __init__(self, data):
        # Inicializa los atributos de la clase padre Person.
        super().__init__(data)
        # Inicializa los atributos específicos de Patient.
        self.id = data['id']
        self.occupation = data['occupation']
        self.birthdate = data['birthdate']
        self.birth_place = data['birth_place']
        self.civil_status = data['civil_status']
        self.eps = data['eps']
        self.residence = data['residence']
        self.emergency_contact = data['emergency_contact']
        self.emergency_number = data['emergency_number']
        self.emergency_relationship = data['emergency_relationship']


    #Función para crear el registro de un paciente
    @classmethod
    def save_patient(cls, formulario, user_id):
        # Consulta SQL para insertar los datos en la tabla person.
        person_query = """
            INSERT INTO person (first_name, last_name, docu_type, docu_number, email, phone, address)
            VALUES (%(first_name)s, %(last_name)s, %(docu_type)s, %(docu_number)s, %(email)s, %(phone)s, %(address)s)
            """
        # Ejecuta la consulta para insertar los datos en la tabla person
        person_id = connectToMySQL('lifeblue_db').query_db(person_query, formulario)

        # Se añade el person_id al formulario para asociarlo con la tabla patient.
        formulario['person_id'] = person_id
        # Se añade el ID del usuario que registra al paciente.
        formulario['user_id'] = user_id  

        # Consulta SQL para insertar un nuevo registro en la tabla patient.
        patient_query = """
            INSERT INTO patient (
                person_id, user_id, occupation, birthdate, birth_place, civil_status, eps, residence,
                emergency_contact, emergency_number, emergency_relationship
            ) VALUES (
                %(person_id)s, %(user_id)s, %(occupation)s, %(birthdate)s, %(birth_place)s, %(civil_status)s, %(eps)s, %(residence)s,
                %(emergency_contact)s, %(emergency_number)s, %(emergency_relationship)s
            )
            """
        # Ejecuta la consulta para insertar los datos del paciente en la tabla patient.
        patient_id = connectToMySQL('lifeblue_db').query_db(patient_query, formulario)

        # Añade el patient_id al formulario para asociarlo con la tabla history.
        formulario['patient_id'] = patient_id

        # Consulta SQL para insertar un nuevo registro en la tabla history.
        history_query = """
            INSERT INTO history (
                reason_consult, medication, personal_history, familiar_history, personal_area, 
                social_area, familiar_area, occupational_area, user_id, patient_id
            ) VALUES (
                %(reason_consult)s, %(medication)s, %(personal_history)s, %(familiar_history)s, %(personal_area)s, 
                %(social_area)s, %(familiar_area)s, %(occupational_area)s, %(user_id)s, %(patient_id)s
            )
            """
        # Ejecuta la consulta para insertar los datos del historial.
        connectToMySQL('lifeblue_db').query_db(history_query, formulario)

        # Devuelve el ID del paciente registrado.
        flash('El paciente fue registrado exitosamente')
        return patient_id
    
    
    #Método para validar la información ingresada en el formulario paciente.
    @staticmethod
    def validate_patient(formulario):
        es_valido = True

        # Valida que el nombre tenga al menos 2 caracteres.
        if len(formulario['first_name']) < 2:
            flash('El nombre debe tener al menos 2 caracteres', 'reg_first_name')
            es_valido = False

        # Valida que el apellido tenga al menos 2 caracteres.
        if len(formulario['last_name']) < 2:
            flash('El apellido debe tener al menos 2 caracteres', 'reg_last_name')
            es_valido = False

        if formulario['docu_type'] == 'none':
            flash('Debes seleccionar un tipo de documento', 'reg_docu_type')
            es_valido = False

        # Valida que el número de documento no esté vacío y sea numérico.
        if not formulario['docu_number'].isdigit():
            flash('Número de documento inválido, vuelve a intentarlo', 'reg_number')
            es_valido = False

        # Valida que la fecha de nacimiento no esté vacía y tenga un formato válido.
        if len(formulario['birthdate']) < 1:
            flash('Debes ingresar la fecha de nacimiento del paciente', 'reg_birthdate')
            es_valido = False

        # Valida que el lugar de nacimiento no esté vacío.
        if len(formulario['birth_place']) < 1:
            flash('Debes ingresar el lugar de nacimiento del paciente', 'reg_birth_place')
            es_valido = False

        # Valida que el estado civil sea uno de los valores permitidos.
        if formulario['civil_status'] not in ['soltero', 'casado', 'divorciado', 'viudo']:
            flash('Debes ingresar el estado civil del paciente', 'reg_civil_status')
            es_valido = False

        # Valida que la EPS no esté vacía.
        if len(formulario['eps']) < 1:
            flash('Debes ingresar la EPS del paciente', 'reg_eps')
            es_valido = False

        # Valida que la ocupación no esté vacía.
        if len(formulario['occupation']) < 1:
            flash('Debes indicar cual es la ocupación del paciente', 'reg_occupation')
            es_valido = False

        # Valida que la residencia no esté vacía.
        if len(formulario['residence']) < 1:
            flash('Debes indicar el municipio o ciudad de residencia del paciente', 'reg_residence')
            es_valido = False

        # Valida que el contacto de emergencia no esté vacío.
        if len(formulario['emergency_contact']) < 1:
            flash('Debes registrar una persona para contacto en caso de emergencia', 'reg_emergency_contact')
            es_valido = False

        # Valida que el número de emergencia no esté vacío y sea numérico.
        if not formulario['emergency_number'].isdigit() or len(formulario['emergency_number']) < 7:
            flash('Número de télefono no válido, debe contener al menos 7 dígitos', 'reg_emergency_number')
            es_valido = False

        # Valida que la relación con el contacto de emergencia no esté vacía.
        if len(formulario['emergency_relationship']) < 1:
            flash('Debes indicar el parentesco con el paciente', 'reg_emergency_relationship')
            es_valido = False

        # Verifica que el email tenga un formato correcto utilizando la expresión regular.
        if not EMAIL_REGEX.match(formulario['email']):
            flash('El correo electrónico ingresado no es válido, vuelve a intentarlo', 'reg_email')
            es_valido = False

                # Valida que el teléfono no esté vacío y sea numérico.
        if not formulario['phone'].isdigit() or len(formulario['phone']) < 7:
            flash('Número de teléfono inválido, debe contener mínimo 7 dígitos', 'reg_phone')
            es_valido = False

        # Valida que la dirección no esté vacía y tenga al menos 5 caracteres.
        if len(formulario['address']) < 5:
            flash('Debes ingresar la dirección de residencia del paciente', 'reg_address')
            es_valido = False

        return es_valido
    

    #Método para mostrar una lista de los pacientes registrados.
    @classmethod
    def get_all(cls):
        query = """SELECT patient.id AS patient_id, patient.*, person.*
                FROM patient
                JOIN person ON person.id = patient.person_id;
                """

        results = connectToMySQL('lifeblue_db').query_db(query)

        patients = []

        for patient in results:
            patients.append(cls(patient))

        return patients
    
    #Método para mostrar un paciente registrado en la base de datos a partir de su ID.
    @classmethod
    def patient_by_id(cls, formulario):
        query = """
                SELECT person.*, patient.*, history.*, history.created_at
                FROM patient
                JOIN person ON person.id = patient.person_id
                LEFT JOIN history ON history.patient_id = patient.id
                WHERE patient.id = %(id)s;
                """
        
        print(f"Ejecutando consulta: {query} con formulario: {formulario}")
        
        result = connectToMySQL('lifeblue_db').query_db(query, formulario)

        # Imprime el resultado para verificar si se encontraron datos
        print(f"Resultado de la consulta: {result}")

        if result:
            # Separa el paciente de sus historias
            patient_data = result[0]
            histories = result  # Todos los registros de la historia

            patient_instance = cls(patient_data)  # Crea la instancia del paciente
            return patient_instance, histories  # Devuelve el paciente y sus historias
        else:
            return None, []
        
    @classmethod
    def update_patient(cls, formulario):
        # Consulta SQL para actualizar la tabla person y patient
        query = """
                UPDATE patient
                JOIN person ON patient.person_id = person.id
                SET 
                    person.first_name = %(first_name)s, 
                    person.last_name = %(last_name)s, 
                    person.docu_type = %(docu_type)s, 
                    person.docu_number = %(docu_number)s, 
                    person.phone = %(phone)s, 
                    person.email = %(email)s, 
                    person.address = %(address)s,
                    patient.residence = %(residence)s, 
                    patient.emergency_contact = %(emergency_contact)s, 
                    patient.emergency_number = %(emergency_number)s, 
                    patient.emergency_relationship = %(emergency_relationship)s,
                    patient.birthdate = %(birthdate)s, 
                    patient.birth_place = %(birth_place)s, 
                    patient.civil_status = %(civil_status)s, 
                    patient.occupation = %(occupation)s,
                    patient.eps = %(eps)s   
                WHERE patient.id = %(id)s  -- Asegúrate de usar el id correcto
                """
        
        # Ejecuta la consulta para editar los datos en la tabla person y patient
        results = connectToMySQL('lifeblue_db').query_db(query, formulario)

        # Mensaje de éxito
        flash('Los datos del paciente han sido actualizados exitosamente')

        return results








    # Método para eliminar un paciente
    @classmethod
    def delete_patient(cls, formulario):
        # Consulta SQL para eliminar el historial asociado al paciente
        history_query = """
            DELETE FROM history WHERE patient_id = %(patient_id)s
        """
        connectToMySQL('lifeblue_db').query_db(history_query, formulario)

        # Consulta SQL para eliminar el registro del paciente
        patient_query = """
            DELETE FROM patient WHERE id = %(patient_id)s
        """
        connectToMySQL('lifeblue_db').query_db(patient_query, formulario)

        # Consulta SQL para eliminar la persona asociada
        person_query = """
            DELETE FROM person WHERE id = (SELECT person_id FROM patient WHERE id = %(patient_id)s)
        """
        connectToMySQL('lifeblue_db').query_db(person_query, formulario)

        # Mensaje de éxito
        flash('El paciente fue eliminado exitosamente')

