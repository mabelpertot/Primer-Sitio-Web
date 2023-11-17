
document.getElementById("registration-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const resultadoValidacion = validarFormulario();

  if (resultadoValidacion) {
    alert(resultadoValidacion.mensaje);
  } else {
    alert("¡El registro fue exitoso! A la brevedad nos pondremos en contacto.");
    // Limpia el formulario
    document.getElementById("registration-form").reset();
  }
});

document.getElementById("eliminarButton").addEventListener("click", function() {
  var idUsuario = 123; // Reemplaza esto con el ID del usuario que deseas eliminar
  fetch("/eliminar/" + idUsuario, {
      method: "DELETE",
  })
  .then(response => response.json())
  .then(data => {
      console.log(data.message); // Imprime el mensaje del servidor
      // Puedes realizar otras acciones después de eliminar el usuario
  })
  .catch(error => {
      console.error("Error al eliminar usuario:", error);
  });
});



function validarFormulario() {
  const nombre = document.getElementById("nombre").value;
  const apellido = document.getElementById("apellido").value;
  const direccion = document.getElementById("direccion").value;
  const numero = document.getElementById("numero").value;
  const codigoPostal = document.getElementById("codigo-postal").value;
  const telefono = document.getElementById("telefono").value;
  const email = document.getElementById("email").value;
  const confirmarEmail = document.getElementById("confirmar-email").value;
  const contrasena = document.getElementById("contrasena").value;
  const confirmarContrasena = document.getElementById("confirmar-contrasena").value;
  textarea = document.getElementById("textarea").value;


  if (!nombre || !apellido || !direccion || !dni || !numero || !codigoPostal || !telefono || !email || !confirmarEmail || !contrasena || !confirmarContrasena) {
    return { mensaje: "Por favor, complete todos los campos obligatorios." };
  }
  if (contrasena !== confirmarContrasena || email !== confirmarEmail) {
    return { mensaje: "Las contraseñas o los emails no coinciden." };
  }

  return null; // Validación exitosa
}





 
  

















 






