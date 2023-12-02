from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
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
    direccion = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    localidad = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    contrasena = db.Column(db.String(255), nullable=False)
    consulta = db.Column(db.Text)

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
    direccion = StringField('Dirección', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    localidad = StringField('Localidad', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    consulta = TextAreaField('Consulta')

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
            direccion=data['direccion'],
            numero=data['numero'],
            localidad=data['localidad'],
            telefono=data['telefono'],
            email=data['email'],
            contrasena=data['contrasena'],
            consulta=data['consulta']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        # enviar por telegram
        try:
            bot = Bot(token=telegram_bot_token)
            chat_id = "" 
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
            'direccion': usuario.direccion,
            'numero': usuario.numero,
            'localidad': usuario.localidad,
            'telefono': usuario.telefono,
            'email': usuario.email,
            'contrasena': usuario.contrasena,
            'consulta': usuario.consulta,
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
        usuario.direccion = request.form['direccion']
        usuario.numero = request.form['numero']
        usuario.localidad = request.form['localidad']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['email']
        usuario.contrasena = request.form['contrasena']
        usuario.consulta = request.form['consulta']
        
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
    return render_template('formulario.html')

@app.route('/especialidades')
def especialidades():
    return render_template('especialidades.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html')

if __name__ == '__main__':
    app.run(debug=True)
