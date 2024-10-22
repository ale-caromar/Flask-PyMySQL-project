# Importa la aplicación Flask definida en el archivo __init__.py.
from flask_app import app

# Importa funciones de Flask para renderizar plantillas, redirigir, mostrar mensajes, manejar solicitudes y sesiones.
from flask import render_template, redirect, request, session

# Importa el modelo User desde el archivo users.py.
from flask_app.models.users import User

# Importa el modelo de Patients desde el archivo patients.py.
from flask_app.models.patients import Patient

# Importa el modelo de Histories desde el archivo histories.py.
from flask_app.models.histories import History

# Renderiza la pantalla para registrar evolución de un paciente.
@app.route('/add_route/<int:patient_id>')
def add_route(patient_id):
    # Verifica si el usuario ha iniciado sesión; de lo contrario, redirige a la página de inicio.
    if 'user_id' not in session:
        return redirect('/')

    # Prepara un diccionario con el ID del usuario para obtener sus datos.
    formulario = {
        'id': session['user_id']
    }
    
    # Obtiene los datos del usuario mediante su ID.
    user = User.get_by_id(formulario)
    print("User data:", user)  # Imprime los datos del usuario para depuración.
    
    # Prepara un diccionario con el ID del paciente para obtener sus datos.
    form_patient = {"id": patient_id}
    
    # Obtiene el paciente y su historial utilizando el ID del paciente.
    patient, histories = Patient.patient_by_id(form_patient)  # Obteniendo el paciente y las historias.
    print("Patient data:", patient)  # Imprime los datos del paciente para depuración.
    print("Histories data:", histories)  # Imprime los datos del historial para depuración.

    # Renderiza la plantilla 'add_history.html', pasando los datos del usuario y del paciente.
    return render_template('add_history.html', user=user, patient=patient)

#Envía los datos del formulario a traves de método POST
@app.route('/add_entry/<int:patient_id>', methods=['POST'])
def add_entry(patient_id):
    # Obtiene el ID del usuario del formulario, eliminando espacios en blanco.
    user_id = request.form.get('user_id', '').strip()

    # Verificación y creación del diccionario para insertar en la base de datos.
    formulario = {
        "patient_id": patient_id,
        "reason_consult": request.form['reason_consult'],
        "medication": request.form['medication'],
        "personal_history": request.form['personal_history'],
        "familiar_history": request.form['familiar_history'],
        "personal_area": request.form['personal_area'],
        "social_area": request.form['social_area'],
        "familiar_area": request.form['familiar_area'],
        "occupational_area": request.form['occupational_area'],
        "user_id": user_id
    }

    # Llamada a la función que guarda la entrada en la base de datos.
    History.add_entry(formulario)

    return redirect(f'/show_patient/{patient_id}')  # Ajustado para redirigir al paciente específico
