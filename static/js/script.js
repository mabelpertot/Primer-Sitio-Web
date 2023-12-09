
function validarFormulario() {
  const nombre = document.getElementById("nombre").value;
  const apellido = document.getElementById("apellido").value;
  const dni = document.getElementById("dni").value;
  const fechaNacimiento = document.getElementById('fecha_nacimiento').value;
  const telefono = document.getElementById("telefono").value;
  const email = document.getElementById("email").value;

  if (!nombre || !apellido || !dni || !fechaNacimiento || !telefono || !email) {
    return { mensaje: "Por favor, complete todos los campos obligatorios." };
  }

  return null; // Validación exitosa
}

function editarUsuario(userId) {
  fetch(`/obtener_formulario_usuario/${userId}`, {
      method: 'POST', 
  })
      .then(response => {
          if (response.ok) {
              return response.json();
          } else {
              throw new Error('Usuario no encontrado');
          }
      })
      .then(data => {
          // Rellenar el formulario con la información obtenida
          document.getElementById('registration-form').elements['id'].value = data.id;
          document.getElementById('registration-form').elements['nombre'].value = data.nombre;
          document.getElementById('registration-form').elements['apellido'].value = data.apellido;
          document.getElementById('registration-form').elements['dni'].value = data.dni;
          document.getElementById('registration-form').elements['fecha'].value = data.fecha_nacimiento;
          document.getElementById('registration-form').elements['correo'].value = data.email;
          document.getElementById('registration-form').elements['contrasena'].value = data.contrasena;
          document.getElementById('registration-form').elements['admin'].checked = data.admin;

          // Cambiar el texto del botón de enviar para indicar que es una edición
          document.getElementById('enviarButton').innerText = 'Guardar Cambios';

          // Crear un elemento de mensaje y agregarlo al formulario
          const mensajeElement = document.createElement('div');
          mensajeElement.className = 'alert alert-success';
          mensajeElement.setAttribute('role', 'alert');
          mensajeElement.textContent = 'Usuario encontrado. Datos cargados en el formulario.';

          // Obtener el formulario y agregar el mensaje al principio
          const formulario = document.getElementById('registration-form');
          formulario.insertBefore(mensajeElement, formulario.firstChild);

          // Eliminar el mensaje después de unos segundos
          setTimeout(() => {
              formulario.removeChild(mensajeElement);
          }, 2000);
      })
      .catch(error => {
          console.error('Error:', error);
          // Crear un elemento de mensaje de error y agregarlo al formulario
          const mensajeErrorElement = document.createElement('div');
          mensajeErrorElement.className = 'alert alert-danger';
          mensajeErrorElement.setAttribute('role', 'alert');
          mensajeErrorElement.textContent = 'Error al encontrar el usuario.';

          // Obtener el formulario y agregar el mensaje de error al principio
          const formulario = document.getElementById('registration-form');
          formulario.insertBefore(mensajeErrorElement, formulario.firstChild);

          // Eliminar el mensaje después de unos segundos
          setTimeout(() => {
              formulario.removeChild(mensajeErrorElement);
          }, 2000);
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


const loginsec=document.querySelector('.login-section')
const loginlink=document.querySelector('.login-link')
const registerlink=document.querySelector('.register-link')
registerlink.addEventListener('click',()=>{
    loginsec.classList.add('active')
})
loginlink.addEventListener('click',()=>{
    loginsec.classList.remove('active')
})





 
  
