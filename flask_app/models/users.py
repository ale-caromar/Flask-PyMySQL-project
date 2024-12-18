# Importa la conexión con la base de datos desde la configuración.
from flask_app.config.mysqlconnection import connectToMySQL

#Importa la clase Person
from flask_app.models.persons import Person

# Importa el módulo de expresiones regulares para validaciones.
import re
# Expresión regular para validar el formato del correo electrónico.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Importa la función flash para mostrar mensajes de error o confirmación en el formulario.
from flask import flash


# Define la clase User que hereda de Person.
class User(Person):
    # Atributo de clase: la profesión por defecto de los usuarios es "Psicólogo".
    profession = "Psicólogo/a"

    # Constructor de la clase User. Inicializa los atributos de Person y agrega los de User.
    def __init__(self, data):
        # Inicializa los atributos de la clase padre Person.
        super().__init__(data)
        # Inicializa los atributos específicos de User.
        self.id = data['id']
        self.university = data['university']
        self.professional_card = data['professional_card']
        self.professional_reg = data['professional_reg']
        self.other_degrees = data['other_degrees']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Método de clase para guardar un nuevo usuario en la base de datos.
    @classmethod
    def save_user(cls, formulario):
        
        # Consulta para insertar los datos en la tabla person.
        person_query = """
            INSERT INTO person (first_name, last_name, docu_type, docu_number, email, phone, address) 
            VALUES (%(first_name)s, %(last_name)s, %(docu_type)s, %(docu_number)s, %(email)s, %(phone)s, %(address)s)
        """

        # Ejecuta la query para insertar los datos en la tabla person
        person_id = connectToMySQL('lifeblue_db').query_db(person_query, formulario)

        # Añadir el person_id obtenido al formulario para poder asociarlo con la tabla user
        formulario['person_id'] = person_id

        # Consulta SQL para insertar un nuevo registro en la tabla user.
        user_query = """
            INSERT INTO user (person_id, university, professional_card, professional_reg, other_degrees, password) 
            VALUES (%(person_id)s, %(university)s, %(professional_card)s, %(professional_reg)s, %(other_degrees)s, %(password)s)
        """

        # Ejecuta la query para insertar los datos del usuario en la tabla user.
        user_id = connectToMySQL('lifeblue_db').query_db(user_query, formulario)

        # Retorna el user_id (ID del usuario recién insertado)
        return user_id

    
    # Método estático para validar los datos ingresados en el formulario de registro.
    @staticmethod
    def validate_user(formulario):
        es_valido = True

        # Verifica que el email tenga un formato correcto utilizando la expresión regular.
        if not EMAIL_REGEX.match(formulario['email']):
            flash('El correo electrónico ingresado no es válido', 'reg_email')
            es_valido = False

        # Verifica si el correo ya existe en la base de datos.
        query = "SELECT * FROM person WHERE email = %(email)s"
        results = connectToMySQL('lifeblue_db').query_db(query, formulario)
        if len(results) >= 1:
            flash('Este correo ya ha sido registrado', 'reg_email')
            es_valido = False
        
        # Valida que la contraseña tenga al menos 6 caracteres.
        if len(formulario['password']) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'reg_password')
            es_valido = False
        
        # Verifica que las contraseñas coincidan.
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden', 'reg_password')
            es_valido = False

        #Valida que el nombre tenga al menos 2 caracteres.
        if len(formulario['first_name']) < 2 :
            flash('El nombre debe de tener al menos 2 caracteres', 'reg_first')
            es_valido = False
        
        #Valida que el apellido tenga al menos 2 caracteres
        if len(formulario['last_name']) < 2:
            flash('El apellido debe de tener al menos 2 caracteres', 'reg_last')
            es_valido = False

         # Valida que se haya seleccionado un tipo de documento válido
        if formulario['docu_type'] not in ['cc', 'ce', 'pp', 'ti']:
            flash('Ingrese su tipo de documento de identidad', 'reg_docutype')
            es_valido = False

        # Valida que el número de documento no esté vacío y sea numérico.
        if not formulario['docu_number'].isdigit() or len(formulario['docu_number']) < 4:
            flash('El número de documento es inválido, debe contener mínimo 4 dígitos', 'reg_number')
            es_valido = False

        # Valida que el teléfono no esté vacío y sea numérico.
        if not formulario['phone'].isdigit() or len(formulario['phone']) < 7:
            flash('Número de teléfono inválido, debe contener mínimo 7 dígitos', 'reg_phone')
            es_valido = False

        # Valida que la dirección no esté vacía y tenga al menos 5 caracteres.
        if len(formulario['address']) < 5:
            flash('Ingresa una dirección', 'reg_address')
            es_valido = False

        # Valida que la universidad tenga al menos 3 caracteres
        if len(formulario['university']) < 3:
            flash('El nombre de la universidad debe contener mínimo 3 caracteres', 'reg_university')
            es_valido = False

        # Valida que la tarjeta profesional tenga al menos 4 caracteres.
        if len(formulario['professional_card']) < 4:
            flash('El número de tarjeta profesional debe contener mínimo 4 caracteres', 'reg_card')
            es_valido = False

        # Valida que el número de registro profesional tenga al menos 4 caracteres.
        if len(formulario['professional_reg']) < 4:
            flash('El número de registro profesional debe contener mínimo 4 caracteres', 'reg_reg')
            es_valido = False    
        
        return es_valido
    

    # Método de clase para verificar si el email existe en la base de datos al iniciar sesión.
    @classmethod
    def verify_email(cls, formulario):
        # Esta consulta realiza un JOIN entre las tablas person y user para encontrar el correo electrónico ingresado
        query = "SELECT person.*, user.* FROM person INNER JOIN user ON person.id = user.person_id WHERE person.email = %(email)s;"
        
        query = """
                SELECT
                    u.id,
                    p.id AS person_id,
                    p.first_name,
                    p.last_name,
                    p.email,
                    p.docu_type,
                    p.docu_number,
                    p.phone,
                    p.address,
                    u.university,
                    u.professional_card,
                    u.professional_reg,
                    u.other_degrees,
                    u.password,
                    u.created_at,
                    u.updated_at 
                FROM person p
                JOIN user u ON p.id = u.person_id
                WHERE p.email = %(email)s;
            """
        
        # Ejecuta la consulta utilizando el formulario proporcionado
        result = connectToMySQL('lifeblue_db').query_db(query, formulario)
        print(result)  # Esto te ayudará a verificar si 'docu_type' está presente

        # Si no se encuentra el correo electrónico, se retorna False.
        if len(result) < 1:
            return False
        else: # Si el correo electrónico existe, se crea una instancia de User con los datos obtenidos de la consulta.
            user = cls(result[0])
            return user
        

    # Método de clase para obtener un usuario por su ID
    @classmethod
    def get_by_id(cls, formulario):
        # Esta consulta realiza un JOIN para obtener la información del usuario y la persona relacionada
        query = """SELECT 
                    p.id AS person_id,  
                    p.first_name, 
                    p.last_name, 
                    p.docu_type, 
                    p.docu_number, 
                    p.phone, 
                    p.address,
                    p.email, 
                    u.*
                FROM 
                    person p 
                JOIN 
                    user u ON p.id = u.person_id 
                WHERE 
                    u.id = %(id)s;
                """
        result = connectToMySQL('lifeblue_db').query_db(query, formulario)

         # Si se encuentra el usuario, se retorna una instancia de User
        if result:
            return cls(result[0])
        else:
            return None


    # Método de clase para actualizar un usuario en la base de datos
    @classmethod
    def update_user(cls, user_id, formulario):
        # Esta consulta actualiza tanto los datos de la persona como del usuario en las tablas person y user
        query = """
            UPDATE person
            JOIN user ON person.id = user.person_id
            SET 
                person.first_name = %(first_name)s,
                person.last_name = %(last_name)s,
                person.email = %(email)s,
                person.phone = %(phone)s,
                person.address = %(address)s,
                user.university = %(university)s,
                user.professional_card = %(professional_card)s,
                user.professional_reg = %(professional_reg)s,
                user.other_degrees = %(other_degrees)s
            WHERE user.id = %(id)s;  
        """
        
        # Añadir el user_id al formulario para su uso en la consulta
        formulario["id"] = user_id
        
        # Ejecuta la query para actualizar los datos en las tablas person y user
        result = connectToMySQL('lifeblue_db').query_db(query, formulario)
        return result
    

    # Método de clase para eliminar un perfil de usuario
    @classmethod
    def delete_profile(cls, formulario):
        # Primero elimina los registros relacionados en la tabla `history`.
        history_query = """
            DELETE FROM history 
            WHERE user_id = %(user_id)s;  
        """
        connectToMySQL('lifeblue_db').query_db(history_query, formulario)

        # Luego elimina los registros relacionados en la tabla `patient`.
        patient_query = """
            DELETE FROM patient
            WHERE user_id = %(user_id)s;  
        """
        connectToMySQL('lifeblue_db').query_db(patient_query, formulario)

        # Después elimina el registro en la tabla `user`.
        user_query = "DELETE FROM user WHERE id = %(user_id)s;"  # Asegúrate de usar el ID de usuario
        connectToMySQL('lifeblue_db').query_db(user_query, formulario)

        # Retorna True para indicar que la operación fue exitosa
        return True