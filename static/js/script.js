function validarFormulario() {
    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const dni = document.getElementById("dni").value.trim();
    const fechaNacimiento = document.getElementById("fecha-nacimiento").value.trim();
    const telefono = document.getElementById("telefono").value.trim();
    const email = document.getElementById("email").value.trim();
    const editando = document.getElementById('registration-form').elements['editando'].value;

    if (!nombre || !apellido || !dni || !fechaNacimiento || !telefono || !email) {
        mostrarMensajeError("Por favor, complete todos los campos obligatorios.");
        return false; // Validación fallida
    }
     // Lógica de actualización si estás en modo de edición
    const url = editando === 'true' ? `/actualizar_usuario/${document.getElementById('edit-id').value}` : '/crear_usuario';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            nombre: nombre,
            apellido: apellido,
            dni: dni,
            fecha: fechaNacimiento,
            correo: email,
            contrasena: 'dummy', // Ajusta según sea necesario
            admin: document.getElementById('admin').checked,
        }),
    })

    .then(response => {
        if (!response.ok) {
            throw new Error(`Error al ${editando === 'true' ? 'actualizar' : 'crear'} el usuario (${response.status}).`);
        }
        return response.json();
    })

    .then(data => {
        // Resto del código para manejar la respuesta si es necesario
        console.log(data);
        mostrarMensajeExitoso(`Usuario ${editando === 'true' ? 'actualizado' : 'creado'} correctamente.`);
    })
    .catch(error => {
        console.error(`Error al ${editando === 'true' ? 'actualizar' : 'crear'} el usuario:`, error);
        // Resto del código para manejar el error si es necesario
    });

    return true; // Validación exitosa
}

function editarUsuario(idUsuario) {
    fetch(`/obtener_usuario/${idUsuario}`, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error al obtener el usuario (${response.status}).`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('registration-form').elements['id'].value = data.id;
        document.getElementById('registration-form').elements['nombre'].value = data.nombre;
        document.getElementById('registration-form').elements['apellido'].value = data.apellido;
        document.getElementById('registration-form').elements['dni'].value = data.dni;
        document.getElementById('registration-form').elements['fecha'].value = data.fecha_nacimiento;
        document.getElementById('registration-form').elements['email'].value = data.email;
        document.getElementById('registration-form').elements['contrasena'].value = data.contrasena;
        document.getElementById('registration-form').elements['admin'].checked = data.admin;

        document.getElementById('edit-id').value = data.id;
        document.getElementById('enviarButton').innerHTML = 'Guardar Cambios';
        document.getElementById('edit-form').style.display = 'block';
    })
    .catch(error => {
        console.error("Error al obtener el usuario:", error);
        // Manejar el error, mostrar un mensaje al usuario, etc.
    });
}


function eliminarUsuario(dni) {
  const confirmar = confirm("¿Estás seguro de que deseas eliminar este usuario?");
  if (!confirmar) {
      return;
  }

  const filaUsuario = document.getElementById(`usuario_${dni}`);

  fetch(`/eliminar_usuario_dni/${dni}`, {
      method: 'DELETE',
  })
      .then(response => {
          if (!response.ok) {
              throw new Error(`Error al eliminar el usuario (${response.status}).`);
          }
          return response.json();
      })
      .then(data => {
          // Crear un elemento de mensaje y agregarlo al formulario
          const mensajeElement = document.createElement('div');
          mensajeElement.className = 'alert alert-success';
          mensajeElement.setAttribute('role', 'alert');
          mensajeElement.textContent = data.mensaje;

          // Obtener el formulario y agregar el mensaje al principio
          const formulario = document.getElementById('registration-form');
          formulario.insertBefore(mensajeElement, formulario.firstChild);

          // Eliminar el mensaje después de unos segundos
          setTimeout(() => {
              formulario.removeChild(mensajeElement);
          }, 2000);

          // Eliminar la fila de la página solo después de que la operación de eliminación de la base de datos tenga éxito
          if (filaUsuario) {
              filaUsuario.remove();

              // Forzar una actualización del navegador
              window.location.reload(true);
          } else {
              console.error(`No se encontró la fila del usuario con DNI ${dni}.`);
          }
      })
      .catch(error => {
          console.error("Error al eliminar el usuario:", error);

          // Crear un elemento de mensaje de error y agregarlo al formulario
          const mensajeErrorElement = document.createElement('div');
          mensajeErrorElement.className = 'alert alert-danger';
          mensajeErrorElement.setAttribute('role', 'alert');
          mensajeErrorElement.textContent = "Error al eliminar el usuario. Verifica los datos e intenta nuevamente.";

          // Obtener el formulario y agregar el mensaje de error al principio
          const formulario = document.getElementById('registration-form');
          formulario.insertBefore(mensajeErrorElement, formulario.firstChild);

          // Eliminar el mensaje después de unos segundos
          setTimeout(() => {
              formulario.removeChild(mensajeErrorElement);
          }, 2000);
      });
}


document.addEventListener('DOMContentLoaded', function() {
    const loginsec = document.querySelector('.login-section');
    const loginlink = document.querySelector('.login-link');
    const registerlink = document.querySelector('.register-link');

    console.log(registerlink);  // Verifica si registerlink es null o un elemento

    registerlink.addEventListener('click', () => {
        loginsec.classList.add('active');
    });

    loginlink.addEventListener('click', () => {
        loginsec.classList.remove('active');
    });
});








 
  
