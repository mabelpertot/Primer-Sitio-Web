import mysql.connector

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms import HiddenField
from flask import flash

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'usuariosdb',
    'port': '3306',
}

# Conexión a la base de datos
conexion = mysql.connector.connect(**db_config)
# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255),
        apellido VARCHAR(255),
        dni VARCHAR(15),
        direccion VARCHAR(255),
        numero VARCHAR(15),
        codigo_postal VARCHAR(15),
        telefono VARCHAR(15),
        email VARCHAR(255),
        confirmar_email VARCHAR(255),
        contrasena VARCHAR(255),
        confirmar_contrasena VARCHAR(255),
        consulta TEXT
    )
""")
conexion.commit()

# Definir el formulario utilizando Flask-WTF
class UsuarioForm(FlaskForm):
    id = HiddenField()  # Agrega un campo oculto para el ID
    nombre = StringField('Nombre', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    codigo_postal = StringField('Código Postal', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirmar_email = StringField('Confirmar Email', validators=[DataRequired(), Email()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contrasena = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    consulta = TextAreaField('Consulta')

# Rutas

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        # obtener la lista de usuarios desde la base de datos y pasarla al template
        cursor.execute("SELECT id, nombre, apellido FROM usuarios")
        usuarios = cursor.fetchall()
        # define 'usuario' as none for the initial render
        usuario = None
        return render_template('formulario.html', usuarios=usuarios, usuario=usuario)

    elif request.method == 'POST':
        form = UsuarioForm(request.form)
        if form.validate():
            try:
                if form.id.data:  # Si hay un ID en el formulario, entonces es una actualización
                    id_usuario = form.id.data
                    nuevo_nombre = form.nombre.data
                    nuevo_apellido = form.apellido.data
                    nuevo_dni = form.dni.data
                    nuevo_direccion = form.direccion.data
                    nuevo_numero = form.numero.data
                    nuevo_codigo_postal = form.codigo_postal.data
                    nuevo_telefono = form.telefono.data
                    nuevo_email = form.email.data
                    nuevo_confirmar_email = form.confirmar_email.data
                    nuevo_contrasena = form.contrasena.data
                    nuevo_confirmar_contrasena = form.confirmar_contrasena.data
                    nueva_consulta = form.consulta.data
                
                                    # Actualizar datos en la base de datos
                    cursor.execute("""
                        UPDATE usuarios
                        SET nombre=%s, apellido=%s, dni=%s, direccion=%s, numero=%s,
                        codigo_postal=%s, telefono=%s, email=%s, confirmar_email=%s,
                        contrasena=%s, confirmar_contrasena=%s, consulta=%s
                        WHERE id=%s
                    """, (
                        nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_direccion, nuevo_numero,
                        nuevo_codigo_postal, nuevo_telefono, nuevo_email, nuevo_confirmar_email,
                        nuevo_contrasena, nuevo_confirmar_contrasena, nueva_consulta, id_usuario
                    ))

                else:  # Si no hay un ID, entonces es una inserción
                    nuevo_nombre = form.nombre.data
                    nuevo_apellido = form.apellido.data
                    nuevo_dni = form.dni.data
                    nuevo_direccion = form.direccion.data
                    nuevo_numero = form.numero.data
                    nuevo_codigo_postal = form.codigo_postal.data
                    nuevo_telefono = form.telefono.data
                    nuevo_email = form.email.data
                    nuevo_confirmar_email = form.confirmar_email.data
                    nuevo_contrasena = form.contrasena.data
                    nuevo_confirmar_contrasena = form.confirmar_contrasena.data
                    nueva_consulta = form.consulta.data                
                
                # Insertar datos en la base de datos
                cursor.execute("""
                    INSERT INTO usuarios (nombre, apellido, dni, direccion, numero, codigo_postal, telefono, email, confirmar_email, contrasena, confirmar_contrasena, consulta)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_direccion, nuevo_numero,
                    nuevo_codigo_postal, nuevo_telefono, nuevo_email, nuevo_confirmar_email,
                    nuevo_contrasena, nuevo_confirmar_contrasena, nueva_consulta
                ))

                conexion.commit()
                flash('Registro exitoso. Nos pondremos en contacto pronto.', 'success')
                return redirect(url_for('formulario'))

            except Exception as e:
                return 'Error: {}'.format(e)
        else:
            return render_template('formulario.html', form=form)
                
                
@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/templates/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/templates/contacto')
def contacto():
    return render_template('formulario.html')

@app.route('/templates/especialidades')
def especialidades():
    return render_template('especialidades.html')

@app.route('/templates/equipo')
def equipo():
    return render_template('equipo.html')

@app.route('/modificar/<int:id_usuario>', methods=['GET', 'POST'])
def modificar(id_usuario):
    if request.method == 'GET':
        # Obtener los datos del usuario a modificar
        cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id_usuario,))
        usuario = cursor.fetchone()
        return render_template('formulario.html', usuario=usuario)

    elif request.method == 'POST':
        try:
            # Obtener datos del formulario
            nuevo_nombre = request.form['nombre']
            nuevo_apellido = request.form['apellido']
            nuevo_dni = request.form['dni']
            nuevo_direccion = request.form['direccion']
            nuevo_numero = request.form['numero']
            nuevo_codigo_postal = request.form['codigo_postal']
            nuevo_telefono = request.form['telefono']
            nuevo_email = request.form['email']
            nuevo_confirmar_email = request.form['confirmar_email']
            nuevo_contrasena = request.form['contrasena']
            nuevo_confirmar_contrasena = request.form['confirmar_contrasena']
            nueva_consulta = request.form['consulta']
        
             # Actualizar datos en la base de datos
            cursor.execute("""
                UPDATE usuarios
                SET nombre=%s, apellido=%s, dni=%s, direccion=%s, numero=%s,
                codigo_postal=%s, telefono=%s, email=%s, confirmar_email=%s,
                contrasena=%s, confirmar_contrasena=%s, consulta=%s
                WHERE id=%s
            """, (
                nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_direccion, nuevo_numero,
                nuevo_codigo_postal, nuevo_telefono, nuevo_email, nuevo_confirmar_email,
                nuevo_contrasena, nuevo_confirmar_contrasena, nueva_consulta, id_usuario
            ))
            
            # Confirmar la transacción
            conexion.commit()

            # Get the updated user data
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id_usuario,))
            usuario = cursor.fetchone()

            return redirect(url_for('formulario'))

        except Exception as e:
            return f"Error al modificar datos: {e}"
        
@app.route('/eliminar/<int:id_usuario>', methods=['DELETE'])
def eliminar(id_usuario):
    try:
        # Eliminar usuario de la base de datos
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
        conexion.commit()
        return jsonify({"message": "Usuario eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar usuario: {e}"}), 500

        

if __name__ == '__main__':
    app.run(debug=True)
