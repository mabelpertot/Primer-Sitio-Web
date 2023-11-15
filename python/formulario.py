import mysql.connector
import tkinter as tk
from tkinter import ttk

class FormularioUsuarios:
    def __init__(self, base):
        # Inicializar la ventana de la aplicación
        self.base = base
        self.tree = None

        # Conectar a la base de datos
        self.conexion = mysql.connector.connect(
                user='root',
                password='root',
                host='127.0.0.1',
                database='usuariosdb',
                port='3306'
        )

        # Crear un cursor para ejecutar consultas SQL
        self.cursor = self.conexion.cursor()

        # Crear la tabla si no existe
        self.crear_tabla()

    def crear_tabla(self):
        # Ejecutar la creación de la tabla en la base de datos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                apellido VARCHAR(255),
                dni VARCHAR(15),
                email VARCHAR(255),
                telefono VARCHAR(15)
            )
        """)
        
        # Confirmar la transacción
        self.conexion.commit()

    def formulario(self):
        try:
            # Crear la interfaz de usuario
            groupBox = ttk.LabelFrame(self.base, text="Datos del Usuario", padding=(5, 5))
            groupBox.grid(row=0, column=0, padx=10, pady=10)

            labels = ["ID:", "Nombres:", "Apellidos:", "DNI:", "Correo:", "Teléfono:"]
            for i, label_text in enumerate(labels):
                ttk.Label(groupBox, text=label_text).grid(row=i, column=0, sticky=tk.E)

            # Entradas para ingresar datos
            self.texBoxId = ttk.Entry(groupBox)
            self.texBoxId.grid(row=0, column=1)
            self.texBoxNombre = ttk.Entry(groupBox)
            self.texBoxNombre.grid(row=1, column=1)
            self.texBoxApellido = ttk.Entry(groupBox)
            self.texBoxApellido.grid(row=2, column=1)
            self.texBoxDni = ttk.Entry(groupBox)
            self.texBoxDni.grid(row=3, column=1)
            self.texBoxEmail = ttk.Entry(groupBox)
            self.texBoxEmail.grid(row=4, column=1)
            self.texBoxTelefono = ttk.Entry(groupBox)
            self.texBoxTelefono.grid(row=5, column=1)

            # Botones para acciones
            ttk.Button(groupBox, text="Guardar", command=self.enviar_datos).grid(row=6, column=0, padx=5)
            ttk.Button(groupBox, text="Modificar", command=self.modificar_datos).grid(row=6, column=1, padx=5)
            ttk.Button(groupBox, text="Eliminar", command=self.eliminar_datos).grid(row=6, column=2, padx=5)

            self.base.mainloop()

        except ValueError as error:
            print("Error al mostrar la interfaz, error:{}".format(error))

    def enviar_datos(self):
        # Obtener datos del formulario
        datos = {
            'nombre': self.texBoxNombre.get(),
            'apellido': self.texBoxApellido.get(),
            'dni': self.texBoxDni.get(),
            'email': self.texBoxEmail.get(),
            'telefono': self.texBoxTelefono.get(),
        }

        # Insertar datos en la base de datos
        self.cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, dni, email, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (datos['nombre'], datos['apellido'], datos['dni'], datos['email'], datos['telefono']))

        # Confirmar la transacción
        self.conexion.commit()

        print("Datos enviados correctamente.")

    def modificar_datos(self):
        try:
        # Obtener datos del formulario
            id_usuario = self.texBoxId.get()
            nuevo_nombre = self.texBoxNombre.get()
            nuevo_apellido = self.texBoxApellido.get()
            nuevo_dni = self.texBoxDni.get()
            nuevo_email = self.texBoxEmail.get()
            nuevo_telefono = self.texBoxTelefono.get()

            # Verificar que se haya seleccionado un usuario
            if not id_usuario:
                print("Error: Selecciona un usuario para modificar.")
                return

            # Actualizar datos en la base de datos
            self.cursor.execute("""
                UPDATE usuarios
                SET nombre=%s, apellido=%s, dni=%s, email=%s, telefono=%s
                WHERE id=%s
            """, (nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_email, nuevo_telefono, id_usuario))

            # Confirmar la transacción
            self.conexion.commit()

            print("Datos modificados correctamente.")

        except Exception as error:
            print(f"Error al modificar los datos: {error}")

    def eliminar_datos(self):
        try:
            # Obtener el ID del usuario a eliminar
            id_usuario = self.texBoxId.get()

            # Verificar que se haya seleccionado un usuario
            if not id_usuario:
                print("Error: Selecciona un usuario para eliminar.")
                return

            # Eliminar datos en la base de datos
            self.cursor.execute("""
                DELETE FROM usuarios
                WHERE id=%s
            """, (id_usuario,))

            # Confirmar la transacción
            self.conexion.commit()

            print("Usuario eliminado correctamente.")

        except Exception as error:
            print(f"Error al eliminar el usuario: {error}")


if __name__ == "__main__":
    # Inicializar la aplicación
    root = tk.Tk()
    form = FormularioUsuarios(root)
    form.formulario()

