from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
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
    telefono = db.Column(db.String(15), nullable=False)
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
    telefono = StringField('Teléfono', validators=[DataRequired()])
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
            fecha_nacimiento=datetime.strptime('01/01/1990', '%d/%m/%Y'),
            telefono=data['telefono'],
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
                f"   - 📞 Teléfono: {data['telefono']}\n"
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
def registrar():
    if request.method == 'GET':
        usuario = Usuario.query.all()
        return render_template('loggedin.html', usuario=usuario)
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
            return redirect(url_for('loggedin'))
        
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            fecha_nacimiento=datetime.strptime('01/01/1990', '%d/%m/%Y'),
            telefono=data['telefono'],
            email=data['email'],
            contrasena=data['contrasena'],
        )
        db.session.add(nuevo_usuario)
        db.session.commit()



@app.route('/ver_usuario_dni/<string:dni>', methods=['GET'])
def ver_usuario_dni(dni):

    usuario = Usuario.query.filter_by(dni=dni).first()

    if usuario:
        # Convierte la fecha de nacimiento a un formato de cadena específico
        fecha_nacimiento_str = usuario.fecha_nacimiento.strftime('%d/%m/%Y') if usuario.fecha_nacimiento else None
        
        usuario_data = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'dni': usuario.dni,
            'fecha_nacimiento': fecha_nacimiento_str,
            'telefono': usuario.telefono,
            'email': usuario.email,
            'contrasena': usuario.contrasena
        }
        
        print("Datos del usuario:", usuario_data)
        return jsonify(usuario_data)
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/modificar_usuario_dni/<string:dni>', methods=['POST'])
def modificar_usuario_dni(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()

    if usuario:
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.dni = request.form['dni']
        usuario.fecha_nacimiento = request.form['fecha_nacimiento']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['email']
        usuario.contrasena = request.form['contrasena']

        db.session.commit()

        return jsonify({'mensaje': 'Cambios guardados correctamente'})
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 40

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
        # Get the entered username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Check the credentials against the database
        user = Usuario.query.filter_by(email=username, contrasena=password).first()

        if user:
            # If the user is found, set the user as logged in
            session['user_id'] = user.id
            return redirect(url_for('loggedin'))
        else:
            # If the credentials are invalid, show an error message
            error_message = 'Usuario o contraseña invalida. Por favor intente nuevamente.'
            return render_template('login.html', error_message=error_message)

    # If it's a GET request, render the login form
    return render_template('login.html')

# Define a route for the loggedin page
@app.route('/loggedin')
def loggedin():
    # Check if the user is logged in
    user_id = session.get('user_id')

    if user_id:
        # If logged in, fetch user data and render the loggedin page
        user = Usuario.query.get(user_id)
        usuarios = Usuario.query.all()
        return render_template('loggedin.html', user=user, usuarios=usuarios)
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/obtener_formulario_usuario', methods=['GET'])
def obtener_formulario_usuario():
    id_usuario = request.args.get('id')
    usuario = Usuario.query.get(id_usuario)
    return render_template('usuario_form.html', usuario=usuario)

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    id_usuario = request.form.get('id')
    usuario = Usuario.query.get(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado correctamente.'})

@app.route('/guardar_edicion_usuario', methods=['POST'])
def guardar_edicion_usuario():
    id_usuario = request.form.get('id')
    usuario = Usuario.query.get(id_usuario)
    # Actualizar los campos del usuario según los datos del formulario
    usuario.nombre = request.form['nombre']
    usuario.apellido = request.form['apellido']
    # Actualiza más campos según sea necesario
    db.session.commit()
    return jsonify({'mensaje': 'Edición de usuario guardada correctamente.'})

if __name__ == '__main__':
    app.run(debug=True)
