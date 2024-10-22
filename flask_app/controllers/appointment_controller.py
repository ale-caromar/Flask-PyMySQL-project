#Importa la aplicación Flask definida en el archivo __init__.py.
from flask_app import app

#Importa funciones de Flask para renderizar plantillas, redirigir, mostrar mensajes, manejar solicitudes y sesiones.
from flask import render_template, redirect, request, session, url_for
#Importa el modelo User desde el archivo users.py.
from flask_app.models.users import User
#Importa el modelo de Patients desde el archivo patients.py
from flask_app.models.patients import Patient
#Importa el modelo de Appointment desde el archivo appointment.py
from flask_app.models.appointment import Appointment

# Renderiza el formulario de agendar cita
@app.route('/schedule')
def schedule():
    # Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Obtiene el user_id de la sesión
    user_id = session['user_id']

    # Prepara el formulario con el user_id
    formulario = {
        'id': user_id
    }

    # Obtiene el usuario por ID
    user = User.get_by_id(formulario)
    print("User data:", user)  # Debugging
    
    # Obtiene todos los pacientes del usuario usando el user_id
    patients = Patient.get_all(user_id)

    # Renderiza la plantilla con los datos del usuario y los pacientes
    return render_template('appointment.html', user=user, patients=patients)


#Ruta para agendar una cita
@app.route('/new_appointment', methods=['POST'])
def new_appointment():
    # Crea un diccionario que contiene todos los campos del formulario
    formulario = {
        "date": request.form['date'],
        "hour": request.form['hour'],
        "place": request.form['place'],
        "state": 'Confirmada',  # Estado predeterminado para la cita
        "patient_id": request.form['patient_id']  # Obtiene el ID del paciente del formulario
    }

    # Obtiene el ID del usuario que está en sesión.
    user_id = session['user_id']
    
    # Agregar la cita a la base de datos
    Appointment.schedule_appointment(formulario, user_id)
    
    #Redirije a la plantilla donde se ven todas las citas agendadas
    return redirect('/view_appointments')


#Ruta para ver las citas agendadas
@app.route('/view_appointments')
def view_appointments():
# Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect('/')

    # Obtener el user_id de la sesión
    user_id = session['user_id']

    # Prepara el formulario con el user_id
    formulario = {
        'id': user_id
    }

    # Obtener el usuario por ID
    user = User.get_by_id(formulario)
    
    # Obtener todos los pacientes del usuario usando el user_id
    patient = Patient.get_all(user_id)
    print("Patients data:", patient)  # Debugging
    
     # Llama al método que obtiene todas las citas del usuario basado en su user_id
    appointments = Appointment.get_appointments(session['user_id'])

     # Renderiza el template 'view_appointments.html', pasando las citas, el usuario y los pacientes a la vista
    return render_template('view_appointments.html', appointments=appointments, user=user, patient=patient)


#Ruta para cancelar una cita
@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment():
    # Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect('/')
    
    # Obtener el user_id de la sesión
    user_id = session['user_id']

    # Obtener el appointment_id desde el formulario
    appointment_id = request.form.get('appointment_id')

    # Cancelar la cita con el método del modelo
    Appointment.cancel_appointment(appointment_id, user_id)

    appointments = Appointment.get_appointments(session['user_id'])

    # Obtener todos los pacientes del usuario usando el user_id
    patient = Patient.get_all(user_id)

    # Renderiza el template 'view_appointments.html', pasando las citas actualizadas (sin la cancelada),
    # el user_id del usuario logueado y la lista de pacientes. Así, la vista puede reflejar los cambios.
    return render_template('view_appointments.html', appointments=appointments, user_id=user_id, patient=patient)

#Ruta para marcar una cita como realizada
@app.route('/completed_appointment', methods=['POST'])
def completed_appointment():
    # Verifica si el usuario ha iniciado sesión
    if 'user_id' not in session:
        return redirect('/')
    
    # Obtener el user_id de la sesión
    user_id = session['user_id']

    # Obtener el appointment_id desde el formulario
    appointment_id = request.form.get('appointment_id')

    # Cancelar la cita con el método del modelo
    Appointment.completed_appointment(appointment_id, user_id)

    appointments = Appointment.get_appointments(session['user_id'])

    # Obtener todos los pacientes del usuario usando el user_id
    patient = Patient.get_all(user_id)
 
    # Renderiza el template 'view_appointments.html', pasando las citas actualizadas (con la cita marcada como realizada),
    # el user_id del usuario logueado y la lista de pacientes. Así, la vista puede reflejar los cambios.
    return render_template('view_appointments.html', appointments=appointments, user_id=user_id, patient=patient)


#Ruta que renderiza el formulario para reprogramar una cita
@app.route('/reschedule_route/<int:appointment_id>')
def reschedule_route(appointment_id):
    # Obtén la cita por su ID
    appointment = Appointment.appointment_by_id(appointment_id)

    # Verifica si se encontró la cita
    if appointment:
        # Crea un diccionario con el ID del paciente
        form_patient = {
            "id": appointment.patient_id  # Asegúrate de que patient_id exista en Appointment
        }
        
        # Llama al método patient_by_id pasando el diccionario
        patient, histories = Patient.patient_by_id(form_patient)

        # Renderiza el formulario de reagendar
        return render_template('reschedule.html', appointment=appointment, patient=patient, histories=histories)
    else:
        # Manejo del caso en que no se encontró la cita
        return "Cita no encontrada", 404


#Ruta con el método post para enviar los datos de una cita reprogramada a la DB
@app.route('/reschedule', methods=['POST'])
def reschedule():
    # Obtén el user_id de la sesión
    user_id = session.get('user_id')

    if not user_id:
        # Si no hay usuario en sesión, redirige a la página de inicio de sesión
        return redirect(url_for('login'))

    # Preparar los datos del formulario para guardar la cita
    formulario = {
        "appointment_id": request.form['appointment_id'],
        "date": request.form['date'],
        "hour": request.form['hour'],
        "place": request.form['place'],
        "user_id": user_id  # Se obtiene el user_id desde la sesión
    }

    # Llama a la función reschedule, pasando los datos del formulario.
    Appointment.reschedule(formulario) 

    # Redirige a la ruta que muestra las citas agendadas
    return redirect(url_for('view_appointments'))
