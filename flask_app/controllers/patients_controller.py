# Importa la aplicación Flask definida en el archivo __init__.py.
from flask_app import app

# Importa funciones de Flask para renderizar plantillas, redirigir, mostrar mensajes, manejar solicitudes y sesiones.
from flask import render_template, redirect, request, session

# Importa el modelo User desde el archivo users.py.
from flask_app.models.users import User

# Importa el modelo de Patients desde el archivo patients.py.
from flask_app.models.patients import Patient


# Renderiza el formulario de registro de usuario.
@app.route('/patient_register')
def patient_register():
    # Verifica si hay un usuario en sesión. 
    # Esto asegura que solo los usuarios autenticados puedan acceder a la lista de pacientes.
    if 'user_id' not in session:
        return redirect('/')

    # Crea un diccionario 'formulario' que contiene el 'id' del usuario en sesión.
    formulario = {
        'id': session['user_id']
    }

    # Llama al método 'get_by_id' de la clase User para obtener la información del usuario autenticado.
    user = User.get_by_id(formulario)

    return render_template('patient_register.html', user=user)

# Ruta para abrir el historial de un paciente.
@app.route('/open_history', methods=['POST'])
def open_history():
    # Valida los datos del formulario usando el método validate_patient del modelo Patient.
    if not Patient.validate_patient(request.form):
        return redirect('/patient_register')  # Redirige al formulario si la validación falla.

    # Se crea un diccionario llamado formulario que contiene todos los campos que se extraen de request.form
    # request.form es un objeto de Flask que se utiliza para acceder a los datos enviados a través de un formulario HTML en una solicitud POST.
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "docu_type": request.form['docu_type'],
        "docu_number": request.form['docu_number'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "email": request.form['email'],
        "occupation": request.form['occupation'],
        "reason_consult": request.form['reason_consult'],
        "medication": request.form['medication'],
        "personal_history": request.form['personal_history'],
        "familiar_history": request.form['familiar_history'],
        "personal_area": request.form['personal_area'],
        "social_area": request.form['social_area'],
        "familiar_area": request.form['familiar_area'],
        "occupational_area": request.form['occupational_area'],
        "birthdate": request.form['birthdate'],
        "birth_place": request.form['birth_place'],
        "civil_status": request.form['civil_status'],
        "eps": request.form['eps'],
        "residence": request.form['residence'],
        "emergency_contact": request.form['emergency_contact'],
        "emergency_number": request.form['emergency_number'],
        "emergency_relationship": request.form['emergency_relationship'],
        "reason_consult": request.form['reason_consult'],
        "medication": request.form['medication'],
        "personal_history": request.form['personal_history'],
        "familiar_history": request.form['familiar_history'],
        "social_area": request.form['social_area'],
        "personal_area": request.form['personal_area'],
        "occupational_area": request.form['occupational_area'],
        "familiar_area": request.form['familiar_area']
    }

    # Obtener el ID del usuario que está en sesión.
    user_id = session['user_id']

    # Se llama al método save_patient del modelo Patient
    # Se pasa el diccionario formulario y el user_id. Se encarga de insertar los datos del paciente en la base de datos y devolver el ID del nuevo paciente registrado.
    patient_id = Patient.save_patient(formulario, user_id)
    
    # Se imprime en la consola el ID del paciente registrado para tener un registro en el servidor de la acción realizada.
    print(f'El ID del paciente registrado es: {patient_id}')

    return redirect('/all_patients')  # Redirige a la lista de pacientes


@app.route('/all_patients')
def all_patients():
    # Verifica si hay un usuario en sesión.
    if 'user_id' not in session:
        return redirect('/')

    # Obtiene directamente el ID del usuario en sesión.
    user_id = session['user_id']

    # Llama al método 'get_by_id' de la clase User para obtener la información del usuario autenticado.
    user = User.get_by_id(user_id)

    # Llama al método 'get_all' de la clase Patient para obtener la lista de todos los pacientes registrados.
    patients = Patient.get_all(user_id)

    # Renderiza la plantilla 'all_patients.html' pasando la información del usuario y la lista de sus pacientes.
    return render_template('all_patients.html', user=user, patients=patients)


# Ruta para mostrar la información de un paciente específico.
@app.route('/show_patient/<int:id>')
def show_patient(id):
    # Verifica si hay un usuario en sesión.
    if 'user_id' not in session:
        return redirect('/')
    
    # Crea un diccionario que contiene el ID del usuario en sesión.
    formulario = {
        'id': session['user_id']
    }

    # Obtiene los datos del usuario autenticado usando el ID de la sesión.
    user = User.get_by_id(formulario)
    
    # Prepara un diccionario con el ID del paciente para buscarlo.
    form_patient = {"id": id}
    
    # Llama al método para obtener la información del paciente y su historial.
    patient, histories = Patient.patient_by_id(form_patient)

    # Verifica si el paciente fue encontrado.
    if not patient:
        return "Paciente no encontrado", 404

    # Renderiza la plantilla 'show_patient.html' pasando la información del usuario, paciente y su historial.
    return render_template('show_patient.html', user=user, patient=patient, histories=histories)


# Define una ruta para editar la información de un paciente, con parametro patient_id que captura el ID del paciente.
@app.route('/edit_patient/<int:patient_id>')
def edit_patient(patient_id):
    # Verifica si hay un usuario autenticado en la sesión.
    if 'user_id' not in session:
        return redirect('/')  # Si no hay un usuario autenticado, redirige a la página de inicio.

    # Crea un diccionario que contiene el ID del usuario actualmente en sesión.
    formulario = {
        'id': session['user_id']
    }

    # Obtiene los datos del usuario autenticado usando el ID de la sesión.
    user = User.get_by_id(formulario)

    # Prepara un diccionario con el ID del paciente para buscarlo.
    form_patient = {"id": patient_id}  # Prepara un diccionario con el ID del paciente para buscarlo.
    
    # Llama al método para obtener la información del paciente y su historial.
    patient, histories = Patient.patient_by_id(form_patient)

    # Renderiza la plantilla para editar los datos del paciente, pasando la información del usuario, el paciente y su historial.
    return render_template('update_patient.html', user=user, patient=patient, histories=histories)


# Elimina a un paciente y redirige a la lista de pacientes.
@app.route('/delete_patient/<int:id>')  # Define una ruta para eliminar un paciente utilizando su ID.
def delete_patient(id):
    # Verifica si hay un usuario autenticado en la sesión.
    if 'user_id' not in session:
        return redirect('/')  # Si no hay un usuario autenticado, redirige a la página de inicio.

    # Prepara un diccionario con el ID del paciente a eliminar, usando 'patient_id' como clave.
    formulario = {'patient_id': id}  # Prepara un diccionario con el ID del paciente a eliminar, usando patient_id como clave.
    
    # Llama al método delete_patient del modelo Patient para eliminar al paciente.
    Patient.delete_patient(formulario) 

    # Redirige a la ruta que muestra la lista de todos los pacientes después de realizar la eliminación.
    return redirect('/all_patients')


# Define una ruta para actualizar los datos del paciente, a través de solicitud POST.
@app.route('/update_patient', methods=['POST'])
def update_patient_route():
    # Preparar los datos del formulario para guardar el paciente.
    formulario = {
        "id": request.form['id'],  # Toma el ID del paciente del campo oculto del formulario.
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "docu_type": request.form['docu_type'],
        "docu_number": request.form['docu_number'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "email": request.form['email'],
        "occupation": request.form['occupation'],
        "birthdate": request.form['birthdate'],
        "birth_place": request.form['birth_place'],
        "civil_status": request.form['civil_status'],
        "eps": request.form['eps'],
        "residence": request.form['residence'],
        "emergency_contact": request.form['emergency_contact'],
        "emergency_number": request.form['emergency_number'],
        "emergency_relationship": request.form['emergency_relationship']
    }

    # Imprimir para verificar el ID recibido (Sirve para depurar).
    print(f'Formulario recibido para actualización: {formulario}')  # Muestra en la consola el formulario recibido para la actualización.

    # Llama al método update_patient en el modelo Patient para actualizar los datos del paciente en la base de datos.
    Patient.update_patient(formulario)

    # Redirige a la lista de pacientes después de la actualización.
     # Redirige a la plantilla de mostrar paciente después de la actualización.
    return redirect(f'/show_patient/{formulario["id"]}')  # Redirige a la ruta show_patient con el ID del paciente actualizado.
