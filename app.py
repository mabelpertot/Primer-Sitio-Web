from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from flask import flash
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms import HiddenField
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
from telegram import Bot

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# telegram token
telegram_bot_token = "6430948464:AAGJDAm8VmhnVZoZI6QBrjc7mGMbi_AmPn8"

# Configuración de Flask-Migrate y SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/registro_usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(15), nullable=False, unique=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    contrasena = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)

# Crear la tabla si no existe
with app.app_context():
    db.create_all()

# Definir el formulario utilizando Flask-WTF
class UsuarioForm(FlaskForm):
    id = HiddenField()
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    fecha_nacimiento = StringField('Fecha de Nacimiento', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])

# Rutas y funciones Flask
@app.route('/formulario', methods=['GET', 'POST'])
async def formulario():
    if request.method == 'GET':
        usuario = Usuario.query.all()
        return render_template('formulario.html', usuario=usuario)
    elif request.method == 'POST':
        data = request.form.to_dict()   
        
        # Verifica si se proporciona un DNI para la búsqueda
        dni_busqueda = data.get('dni-busqueda')
        if dni_busqueda:
            usuario = Usuario.query.filter_by(dni=dni_busqueda).first()
            if usuario:
                # Si se encuentra el usuario, muestra la información en el formulario
                return render_template('formulario.html', usuarios=[usuario])
            else:
                # Si no se encuentra el usuario, puedes manejarlo como desees (por ejemplo, mostrar un mensaje)
                return render_template('formulario.html', mensaje='Usuario no encontrado')
            
        # valida que el DNI del usuario no exista
        usuario_existente_dni = Usuario.query.filter_by(dni=data['dni']).first()
        if usuario_existente_dni:
            return redirect(url_for('formulario'))
        
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            fecha_nacimiento=datetime.strptime('01/01/2000', '%d/%m/%Y'),
            email=data['email'],
            contrasena=data['contrasena'],
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        # enviar por telegram
        try:
            bot = Bot(token=telegram_bot_token)
            chat_id = "5294223155" 
            message = (
                "📬 **Nueva Consulta** 📬\n\n"
                "👤 **Datos del Usuario**:\n"
                f"   - 🧑 Nombre: {data['nombre']}\n"
                f"   - 🧔 Apellido: {data['apellido']}\n"
                f"   - 🆔 DNI: {data['dni']}\n"
                f"   - 📧 Email: {data['email']}\n"
                "📝 **Consulta**:\n"
                f"{data['consulta']}"
            )
            await bot.send_message(chat_id, message)
            print('Mensaje de Telegram enviado')

        except Exception as e:
            print('Error al enviar el mensaje de Telegram:', str(e))
            return jsonify({'error': 'Error al enviar el mensaje a Telegram. Inténtalo de nuevo más tarde.'})
        
        return redirect(url_for('formulario'))

@app.route('/btnregistrar', methods=['GET', 'POST'])
def btnregistrar():
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        return render_template('loggedin.html', usuarios=usuarios)
    elif request.method == 'POST':
        data = request.form.to_dict()   
    
        # Verifica si se proporciona un DNI para la búsqueda
        dni_busqueda = data.get('dni-busqueda')
        if dni_busqueda:
            usuario = Usuario.query.filter_by(dni=dni_busqueda).first()
            if usuario:
                # Si se encuentra el usuario, muestra la información en el formulario
                return render_template('loggedin.html', usuarios=[usuario])
            else:
                # Si no se encuentra el usuario, puedes manejarlo como desees (por ejemplo, mostrar un mensaje)
                return render_template('loggedin.html', mensaje='Usuario no encontrado')
            
        # valida que el DNI del usuario no exista
        usuario_existente_dni = Usuario.query.filter_by(dni=data['dni']).first()
        if usuario_existente_dni:
            return redirect(url_for('btnregistrar'))
        
        # Convertir el valor del campo 'admin' a un booleano
        admin_value = data.get('admin', 'off') == 'on'
        
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            fecha_nacimiento=datetime.strptime(data['fecha'], '%Y-%m-%d'),
            email=data['correo'],
            contrasena=data['contrasena'],
            admin=admin_value,
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error: Ya existe un usuario con el mismo DNI', 'error')

        return redirect(url_for('btnregistrar'))


  # Ruta para obtener los datos de un usuario por su ID

# Ajustes en editar_usuario
@app.route('/editar_usuario/<int:id_usuario>', methods=['POST'])
def editar_usuario(id_usuario):
    print(f'ID del usuario a editar: {id_usuario}')
    usuario = Usuario.query.get(id_usuario)
    
    if usuario:
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.email = request.form['email']
        usuario.telefono = request.form['telefono']
        db.session.commit()
        return jsonify({'mensaje': 'Edición de usuario guardada correctamente.'})
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/obtener_formulario_usuario/<int:id_usuario>', methods=['GET'])
def obtener_formulario_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'email': usuario.email,
        'telefono': usuario.telefono
    })

@app.route('/guardar_cambios_usuario', methods=['POST'])
def guardar_cambios_usuario():
    id_usuario = request.form.get('id')
    usuario = Usuario.query.get(id_usuario)
    
    if usuario:
        # Actualiza los campos del usuario según los datos del formulario
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.email = request.form['email']
        usuario.telefono = request.form['telefono']

        db.session.commit()
        return jsonify({'mensaje': 'Edición de usuario guardada correctamente.'})
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404
@app.route('/eliminar_usuario_dni/<string:dni>', methods=['DELETE'])
def eliminar_usuario_dni(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()

    if usuario:
        db.session.delete(usuario)
        db.session.commit()

        return jsonify({'mensaje': 'Usuario eliminado correctamente.'})
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto')
def contacto():
    return render_template('loggedin.html')

@app.route('/especialidades')
def especialidades():
    return render_template('especialidades.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Usuario.query.filter_by(email=username, contrasena=password).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('loggedin'))
            # Redirigir según el rol del usuario
            # if user.admin:
            #     return redirect(url_for('loggedin'))
            # else:
            #     return redirect(url_for('pagina_no_admin'))
        else:
            # If the credentials are invalid, show an error message
            error_message = 'Usuario o contraseña invalida. Por favor intente nuevamente.'
            return render_template('login.html', error_message=error_message)

    # If it's a GET request, render the login form
    return render_template('login.html')

@app.route('/loggedin')
def loggedin():
    user_id = session.get('user_id')

    if user_id:
        user = Usuario.query.get(user_id)
        usuarios = Usuario.query.all()
        if user.admin == True:
            return render_template('loggedin.html', user=user, usuarios=usuarios)
        else:
            return render_template('pagina_no_admin.html', mensaje="Página para usuarios no administradores.")

    else:

        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Lógica de cerrar sesión
    session.clear()  # Limpia la sesión
    return redirect(url_for('index'))  # Ajusta la redirección según tu necesidad

if __name__ == '__main__':
    app.run(debug=True)
