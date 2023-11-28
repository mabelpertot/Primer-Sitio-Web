from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms import HiddenField
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pruebacaccomision@gmail.com'
app.config['MAIL_PASSWORD'] = 'pruebacomision'
app.config['MAIL_DEFAULT_SENDER'] = 'pruebacaccomision@gmail.com'

mail = Mail(app)

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
    fecha_nacimiento = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    localidad = db.Column(db.String(255), nullable=False)
    codigo_postal = db.Column(db.String(15), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmar_email = db.Column(db.String(255), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    confirmar_contrasena = db.Column(db.String(255), nullable=False)
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
    codigo_postal = StringField('Código Postal', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirmar_email = StringField('Confirmar Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    consulta = TextAreaField('Consulta')

def enviar_correo(destinatario, asunto, cuerpo):
    try:
        message = Message(asunto, sender=app.config['pruebacaccomision@gmail.com'], recipients=[destinatario])
        message.body = cuerpo
        mail.send(message)
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")

# Rutas y funciones Flask
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        return render_template('formulario.html', usuarios=usuarios)
    elif request.method == 'POST':
        data = request.form.to_dict()
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            fecha_nacimiento=data['fecha_nacimiento'],
            direccion=data['direccion'],
            numero=data['numero'],
            localidad=data['localidad'],
            codigo_postal=data['codigo_postal'],
            telefono=data['telefono'],
            email=data['email'],
            confirmar_email=data['confirmar_email'],
            contrasena=data['contrasena'],
            confirmar_contrasena=data['confirmar_contrasena'],
            consulta=data['consulta']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Nos pondremos en contacto a la brevedad.', 'success')

        # Enviar correo electrónico
        enviar_correo(data['email'], 'Registro exitoso', 'Gracias por registrarte en nuestro sitio.')

        return redirect(url_for('formulario'))

    return jsonify({'mensaje': 'Registro exitoso. Nos pondremos en contacto pronto.'})

@app.route('/ver_usuario_dni/<string:dni>', methods=['GET'])
def ver_usuario_dni(dni):

    usuario = Usuario.query.filter_by(dni=dni).first()

    if usuario:
        usuario_data = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'dni': usuario.dni,
            'fecha_nacimiento': usuario.fecha_nacimiento,
            'direccion': usuario.direccion,
            'numero': usuario.numero,
            'localidad': usuario.localidad,
            'codigo_postal': usuario.codigo_postal,
            'telefono': usuario.telefono,
            'email': usuario.email,
            'confirmar_email': usuario.confirmar_email,
            'contrasena': usuario.contrasena,
            'confirmar_contrasena': usuario.confirmar_contrasena,
            'consulta': usuario.consulta,
        }
        print("Datos del usuario:", usuario_data)
        return jsonify(usuario_data)
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Ruta para editar un usuario (actualiza el registro en la base de datos)
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
        usuario.codigo_postal = request.form['codigo_postal']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['email']
        usuario.confirmar_email = request.form['confirmar_email']
        usuario.contrasena = request.form['contrasena']
        usuario.confirmar_contrasena = request.form['confirmar_contrasena']
        
        db.session.commit()

        return jsonify({'mensaje': 'Cambios guardados correctamente'})
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 40

# Ruta para eliminar un usuario
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
