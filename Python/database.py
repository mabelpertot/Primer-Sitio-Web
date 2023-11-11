import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to create a user table in the database
def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "nombre TEXT, apellido TEXT, dni TEXT, direccion TEXT, numero TEXT, "
              "codigo_postal TEXT, telefono TEXT, email TEXT, contrasena TEXT, comentario TEXT)")
    conn.commit()
    conn.close()

# Function to save a user in the database
def save_user(data):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (nombre, apellido, dni, direccion, numero, codigo_postal, "
              "telefono, email, contrasena, comentario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (data['nombre'], data['apellido'], data['DNI'], data['direccion'], data['numero'],
               data['codigo-postal'], data['telefono'], data['email'], data['contrasena'], data['textarea']))
    conn.commit()
    conn.close()

# Function to show users
def show_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users_list = c.fetchall()
    conn.close()
    return users_list

@app.route('/', methods=['GET', 'POST'])
def registration_form():
    create_users_table()

    if request.method == 'POST':
        user_data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'DNI': request.form['DNI'],
            'direccion': request.form['direccion'],
            'numero': request.form['numero'],
            'codigo-postal': request.form['codigo-postal'],
            'telefono': request.form['telefono'],
            'email': request.form['email'],
            'contrasena': request.form['contrasena'],
            'textarea': request.form['textarea']
        }
        save_user(user_data)

    users = show_users()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
