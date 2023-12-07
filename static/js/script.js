
function validarFormulario() {
  const nombre = document.getElementById("nombre").value;
  const apellido = document.getElementById("apellido").value;
  const dni = document.getElementById("dni").value;
  const fechaNacimiento = document.getElementById("fecha-nacimiento").value;
  const telefono = document.getElementById("telefono").value;
  const email = document.getElementById("email").value;

  if (!nombre || !apellido || !dni || !fechaNacimiento || !telefono || !email) {
    return { mensaje: "Por favor, complete todos los campos obligatorios." };
  }

  return null; // Validación exitosa
}


function ver(dni) {
  fetch(`/ver_usuario_dni/${dni}`, {
    method: 'GET',
  })
    .then(response => {
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Usuario no encontrado.');
        } else {
          throw new Error(`Error del servidor (${response.status}).`);
        }
      }
      return response.json();
    })
    .then(data => {
      // Llama a funciones para mostrar los datos en tu interfaz de usuario
      mostrarDatosEnPagina(data);
      alert("Usuario encontrado. Datos mostrados.");
    })
    .catch(error => {
      console.error("Error al obtener detalles del usuario:", error);
      alert(error.message || "Error al obtener detalles del usuario. Usuario no encontrado o se produjo un error.");
    });
}

function mostrarDatosEnPagina(data) {
  const datosDiv = document.getElementById("formularioUsuario");

  // Crear una cadena HTML con los datos del usuario
  const html = `
    <h3>Datos del Usuario</h3>
    <p><strong>ID:</strong> ${data.id}</p>
    <p><strong>Nombre:</strong> ${data.nombre}</p>
    <p><strong>Apellido:</strong> ${data.apellido}</p>
    <p><strong>DNI:</strong> ${data.dni}</p>
    <p><strong>Email:</strong> ${data.email}</p>
    <p><strong>Teléfono:</strong> ${data.telefono}</p>
  `;
  // Actualizar el contenido del div
  datosDiv.innerHTML = html;
  console.log(data);
}

function editar(dni) {
  fetch(`/ver_usuario_dni/${dni}`, {
    method: 'GET',
  })
    .then(response => {
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Usuario no encontrado.');
        } else {
          throw new Error(`Error del servidor (${response.status}).`);
        }
      }
      return response.json();
    })
    .then(data => {
      cargarDatosEnPagina(data);
      habilitarEdicion(data); // Pasar data como parámetro
    })
    .catch(error => {
      console.error("Error al obtener detalles del usuario:", error);
      alert(error.message || "Error al obtener detalles del usuario. Usuario no encontrado o se produjo un error.");
    });
}

function cargarDatosEnPagina(data) {
  const datosDiv = document.getElementById("formularioUsuario");

  // Crear una cadena HTML con los datos del usuario
  const html = `
    <h3>Datos del Usuario</h3>
    <p><strong>ID:</strong> ${data.id}</p>
    <p><strong>Nombre:</strong> ${data.nombre}</p>
    <p><strong>Apellido:</strong> ${data.apellido}</p>
    <p><strong>DNI:</strong> ${data.dni}</p>
    <p><strong>Email:</strong> ${data.email}</p>
    <p><strong>Teléfono:</strong> ${data.telefono}</p>
  `;

  // Actualizar el contenido del div
  datosDiv.innerHTML = html;
}


function eliminar(dni) {
  const confirmar = confirm("¿Estás seguro de que deseas eliminar este usuario?");
  if (!confirmar) {
    return;
  }

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
      alert(data.mensaje);
      eliminarUsuarioDePagina(dni);
    })
    .catch(error => {
      console.error("Error al eliminar el usuario:", error);
      alert("Error al eliminar el usuario. Verifica los datos e intenta nuevamente.");
    });
}

function eliminarUsuarioDePagina(dni) {
  // Encuentra la fila de la tabla con el ID igual al dni del usuario
  const filaUsuario = document.getElementById(`usuario_${dni}`);

  if (filaUsuario) {
    // Si se encuentra la fila, elimínala
    filaUsuario.remove();
    console.log(`Usuario con DNI ${dni} eliminado de la página`);
  } else {
    console.warn(`No se encontró la fila del usuario con DNI ${dni}`);
  }
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





 
  

















 






