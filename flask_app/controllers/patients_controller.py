#Importa la aplicación Flask definida en el archivo __init__.py.
from flask_app import app

#Importa funciones de Flask para renderizar plantillas, redirigir, mostrar mensajes, manejar solicitudes y sesiones.
from flask import render_template, redirect, request, session, flash
#Importa el modelo User desde el archivo users.py.
from flask_app.models.users import User
#Importa el modelo de Patients desde el archivo patients.py
from flask_app.models.patients import Patient


# Renderiza el formulario de registro de usuario.
@app.route('/patient_register')
def patient_register():
    return render_template('patient_register.html')

@app.route('/open_history', methods=['POST'])
def open_history():
    # Valida los datos del formulario usando el método validate_patient del modelo Patient.
    if not Patient.validate_patient(request.form):
        return redirect('/patient_register')  # Redirige al formulario si la validación falla.

    # Preparar los datos del formulario para guardar el paciente.
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
        "emergency_relationship": request.form['emergency_relationship']
    }

    # Obtener el ID del usuario que está en sesión.
    user_id = session['user_id']

    # Aquí llamas a la función para guardar el paciente
    patient_id = Patient.save_patient(formulario, user_id)
    
    # Imprimir el ID del paciente registrado en la consola
    print(f'El ID del paciente registrado es: {patient_id}')

    return redirect('/all_patients')  # Redirige a la lista de pacientes


# Devuelve la lista de pacientes registrados por un usuario.
@app.route('/all_patients')
def all_patients():
    if 'user_id'not in session:
        return redirect('/')
    
    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    patients = Patient.get_all()

    return render_template('all_patients.html', user=user, patients=patients)
    

#
@app.route('/show_patient/<int:id>')
def show_patient(id):
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)  # Instancia del usuario que inició sesión

    # La instancia del paciente que queremos mostrar
    form_patient = {"id": id}

    patient, histories = Patient.patient_by_id(form_patient)

    # Imprime el ID para verificar que es correcto
    print(f"ID del paciente solicitado: {patient}")

    if patient:
        return render_template('show_patient.html', user=user, patient=patient, histories=histories)
    else:
        return "Paciente no encontrado", 404
    

# Ruta para mostrar el formulario de actualización del perfil del usuario.
@app.route('/edit_patient/<int:id>')
def edit_patient(id):
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    # La instancia del paciente que queremos mostrar
    form_patient = {"id": id}

    patient, histories = Patient.patient_by_id(form_patient)

    # Renderiza la plantilla update.html y pasa los datos del usuario.
    return render_template('update_patient.html', user=user, patient=patient, histories=histories)  # Pasa el usuario al template


#Elimina a un paciente y redirije a la lista de pacientes
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {'patient_id': id}  # Cambié 'id' por 'patient_id'
    Patient.delete_patient(formulario)

    return redirect('/all_patients')

@app.route('/update_patient', methods=['POST'])
def update_patient_route():

    # Preparar los datos del formulario para guardar el paciente.
    formulario = {
        "id": request.form['id'],  # Toma el ID del campo oculto
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

    # Imprimir para verificar el ID recibido
    print(f'Formulario recibido para actualización: {formulario}')

    # Aquí llamas a la función para actualizar el paciente
    Patient.update_patient(formulario)

    flash('Los datos del paciente han sido actualizados exitosamente')
    return redirect('/all_patients')  # Redirige a la lista de pacientes

