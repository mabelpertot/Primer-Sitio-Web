from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    datos_formulario = {
        'id': request.form['id'],
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'dni': request.form['dni'],
        'email': request.form['email'],
        'telefono': request.form['telefono'],
    }

    # Aquí puedes realizar acciones con los datos recibidos, como guardarlos en una base de datos, etc.
    print(datos_formulario)

    return 'Datos recibidos correctamente.'

if __name__ == '__main__':
    app.run(debug=True)
