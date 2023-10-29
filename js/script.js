
  document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("registration-form").addEventListener("submit", function (event) {
      event.preventDefault();
      enviar();
    });

    function enviar() {
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

      if (nombre && apellido && direccion && numero && codigoPostal && telefono && email && confirmarEmail && contrasena && confirmarContrasena) {
        if (contrasena === confirmarContrasena && email === confirmarEmail) {
          alert("¡El registro fue exitoso! A la brevedad nos pondremos en contacto.");
          // limpia elformulario
          document.getElementById("nombre").value = "";
          document.getElementById("apellido").value = "";
          document.getElementById("direccion").value = "";
          document.getElementById("numero").value = "";
          document.getElementById("codigo-postal").value = "";
          document.getElementById("telefono").value = "";
          document.getElementById("email").value = "";
          document.getElementById("confirmar-email").value = "";
          document.getElementById("contrasena").value = "";
          document.getElementById("confirmar-contrasena").value = "";
          document.getElementById("textarea").value = "";
        } else {
          alert("Las contraseñas o los emails no coinciden.");
        }
      } else {
        alert("Por favor, complete todos los campos obligatorios.");
      }
    }
  });


  const buttons = document.querySelectorAll('.leer-mas');

  // Agrega un controlador de eventos a cada botón
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Obtiene el identificador del contenido adicional a mostrar/ocultar
      const targetId = button.getAttribute('data-target');
      const contenidoAdicional = document.getElementById(targetId);

      // Alterna la visibilidad del contenido adicional al hacer clic en el botón
      if (contenidoAdicional.style.display === 'none' || contenidoAdicional.style.display === '') {
        contenidoAdicional.style.display = 'block';
        button.textContent = 'Leer Menos';
      } else {
        contenidoAdicional.style.display = 'none';
        button.textContent = 'Leer Más';
      }
    });
  });



 
  

















 






