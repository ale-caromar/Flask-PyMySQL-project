#Importa la aplicación Flask definida en el archivo __init__.py.
from flask_app import app

#Importa funciones de Flask para renderizar plantillas, redirigir, mostrar mensajes, manejar solicitudes y sesiones.
from flask import render_template, redirect, flash, request, session

#Importa el modelo User desde el archivo users.py.
from flask_app.models.users import User

# Importar y configurar Bcrypt para manejar la encriptación de contraseñas.
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


# Ruta raíz, renderiza la plantilla 'index.html'.
@app.route('/')
def index():
    return render_template('index.html')


# Renderiza el formulario de registro de usuario.
@app.route('/register_route')
def register_route():
    return render_template('register.html')


# Maneja el registro de usuarios: recibe datos del formulario, los valida y los procesa.
@app.route('/register', methods=['POST'])
def register():
    # Valida los datos del formulario usando el método validate_user del modelo User.
    if not User.validate_user(request.form):
        return redirect('/register_route')  # Redirige al formulario si la validación falla.
    
    # Encripta la contraseña ingresada por el usuario
    pwd = bcrypt.generate_password_hash(request.form['password'])

    # Prepara los datos del formulario para guardar el usuario.
    formulario = {
        "email": request.form['email'],
        "password": pwd,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "docu_type": request.form['docu_type'],
        "docu_number": request.form['docu_number'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "university": request.form["university"],
        "professional_card": request.form["professional_card"],
        "professional_reg": request.form["professional_reg"],
        "other_degrees": request.form["other_degrees"]
    }

    # Guarda el usuario en la base de datos y obtiene el ID de ese nuevo usuario
    id = User.save_user(formulario)

    # Almacena el ID del usuario en la sesión
    session['user_id'] = id

    # Redirige al dashboard después del registro exitoso.
    return redirect('/dashboard')  


# Ruta para iniciar sesión, recibe datos del formulario y los valida.
@app.route('/login', methods=['POST'])
def login():
    # Verifica el email del usuario en la base de datos, usando el método verify_email del modelo user.
    user = User.verify_email(request.form)

    # Si el correo no está registrado, muestra un mensaje de error y redirige a la página de inicio.
    if not user:
        flash('El correo electrónico no se encuentra registrado', 'log_email')
        return redirect('/')

    # Verifica la contraseña del usuario encriptada.
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Contraseña incorrecta, ingresala nuevamente', 'log_password')
        return redirect('/')

    # Almacena el ID del usuario en la sesión.
    session['user_id'] = user.id # Aquí se guarda el ID de la tabla user

    # Imprime el ID del usuario almacenado en la sesión para depuración.
    print(f"ID de usuario almacenado en la sesión: {session['user_id']}")

    # Redirige al dashboard después de un inicio de sesión exitoso.
    return redirect('/dashboard')


# Ruta para mostrar el dashboard.
@app.route('/dashboard')
def dashboard():
    # Verifica si el usuario está en sesión, si no, redirige a la página de inicio.
    if 'user_id' not in session:
        return redirect('/')

    # Prepara el formulario para obtener los detalles del usuario.
    formulario = {
        'id': session['user_id']
    }

    # Obtiene la información del usuario desde la base de datos a partir del ID.
    user = User.get_by_id(formulario)

    # Renderiza la plantilla dashboard.html y pasa los datos del usuario.
    return render_template('dashboard.html', user=user)


# Ruta para mostrar el perfil del usuario en sesión.
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    # Renderiza la plantilla 'profile.html' pasando los datos del usuario.
    return render_template('profile.html', user=user)


# Ruta para mostrar el formulario de actualización del perfil del usuario.
@app.route('/update_route')
def update_route():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    # Renderiza la plantilla update.html y pasa los datos del usuario.
    return render_template('update.html', user=user)  # Pasa el usuario al template
    
    
# Ruta para actualizar el perfil del usuario, recibe datos del formulario y los guarda
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/')

    # Prepara los datos del formulario para actualizar el perfil del usuario.
    formulario = {
        "id": request.form['id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "university": request.form['university'],
        "professional_card": request.form['professional_card'],
        "professional_reg": request.form['professional_reg'],
        "other_degrees": request.form['other_degrees']
    }

    # Actualiza la información del usuario en la base de datos a traves del método update_user
    User.update_user(formulario)
    
    # Muestra un mensaje de éxito y redirige al perfil del usuario.
    flash('Perfil actualizado exitosamente', 'profile_update')
    return redirect('profile')


# Ruta para eliminar el perfil del usuario en sesión.
@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        'person_id': session['user_id']  # Usamos el id de `person` almacenado en la sesión
    }
    
     # Elimina el perfil del usuario en la base de datos usando el metodo delete_profile
    User.delete_profile(formulario)
    
    session.clear()  #Se limpia la sesión tras eliminar el perfil
    
    return redirect('/') #Redirige a la página principal


#Ruta para cerrar la sesión del usuario.
@app.route('/logout')
def logout():
    session.clear() # Limpia la sesión y redirige a la página de inicio.
    return redirect('/') #Redirige a la página principal.



