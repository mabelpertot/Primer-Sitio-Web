
function validarFormulario() {
  const nombre = document.getElementById("nombre").value;
  const apellido = document.getElementById("apellido").value;
  const dni = document.getElementById("dni").value;
  const fechaNacimiento = document.getElementById("fecha-nacimiento").value;
  const direccion = document.getElementById("direccion").value;
  const numero = document.getElementById("numero").value;
  const localidad = document.getElementById("localidad").value;
  const telefono = document.getElementById("telefono").value;
  const email = document.getElementById("email").value;
  const contrasena = document.getElementById("contrasena").value;
  const textarea = document.getElementById("textarea").value;

  if (!nombre || !apellido || !dni || !fechaNacimiento || !direccion  || !numero || !localidad || !telefono || !email || !contrasena || !textarea) {
    return { mensaje: "Por favor, complete todos los campos obligatorios." };
  }
  if (contrasena !== confirmarContrasena || email !== confirmarEmail) {
    return { mensaje: "Las contraseñas o los emails no coinciden." };
  }

  return null; // Validación exitosa
}

function verUsuario() {
  const dni = document.getElementById("dni").value.trim();

  if (dni.trim() === "") {
    alert("Por favor, ingrese un DNI válido.");
    return;
  }

  fetch(`/ver_usuario_dni/${dni}`, {
    method: 'GET',
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Usuario no encontrado (${response.status})`);
      }
      return response.json();
    })
    .then(data => {
      cargarDatosEnFormulario(data); // Nueva línea para cargar los datos en el formulario
      alert("Usuario encontrado. Datos pre-cargados en el formulario.");
    })
    .catch(error => {
      console.error("Error al obtener detalles del usuario:", error);
      alert("Error al obtener detalles del usuario. Usuario no encontrado o se produjo un error.");    
    });
}

function cargarDatosEnFormulario(data) {
  // Actualiza los valores de los campos del formulario con los datos del usuario
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const element = document.getElementById(key);
      if (element) {
        element.value = data[key];
      } else {
        console.warn(`Elemento con id ${key} no encontrado en el formulario.`);
      }
    }
  }
}

function editarUsuario() {
  const dni = document.getElementById("dni").value.trim();

  if (dni === "") {
    alert("Por favor, ingrese un DNI válido.");
    return;
  }

  fetch(`/modificar_usuario_dni/${dni}`, {
    method: 'POST',
    body: new FormData(document.getElementById("registration-form")),
  })
    .then(response => response.json())
    .then(data => {
      alert(data.mensaje);

    })
    .catch(error => {
      console.error("Error al modificar el usuario:", error);
      alert("Error al modificar el usuario. Verifica los datos e intenta nuevamente.");
    });
}

function actualizarFormularioConDatos(data) {
  // Actualiza los valores de los campos del formulario con los datos del usuario
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const element = document.getElementById(key);
      if (element) {
        element.value = data[key];
      }
    }
  }
}

function eliminarUsuario() {
  const dni = document.getElementById("dni").value.trim();

  if (dni === "") {
    alert("Por favor, ingrese un DNI válido.");
    return;
  }

  fetch(`/eliminar_usuario_dni/${dni}`, {
    method: 'DELETE',
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error al eliminar el usuario (${response.status})`);
      }
      return response.json();
    })
    .then(data => {
      alert(data.mensaje);
    })
    .catch(error => {
      console.error("Error al eliminar el usuario:", error);
      alert("Error al eliminar el usuario. Verifica los datos e intenta nuevamente.");
    })
    .finally(() => {
      // Reiniciar el formulario a su estado inicial
      document.getElementById("registration-form").reset();
    });
}

function guardarCambios() {
  const dni = document.getElementById("dni").value.trim();

  if (dni === "") {
    alert("Por favor, ingrese un DNI válido.");
    return;
  }

  fetch(`/modificar_usuario_dni/${dni}`, {
    method: 'POST',
    body: new FormData(document.getElementById("registration-form")),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error al modificar el usuario (${response.status})`);
      }
      return response.json();
    })
    .then(data => {
      alert(data.mensaje);
    })
    .catch(error => {
      console.error("Error al modificar el usuario:", error);
      alert("Error al modificar el usuario. Verifica los datos e intenta nuevamente.");
    })
    .finally(() => {
      // Reiniciar el formulario a su estado inicial
      document.getElementById("registration-form").reset();
    });
}





 
  

















 






