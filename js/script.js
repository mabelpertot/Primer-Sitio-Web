function toggleInfo(id) {
   info = document.getElementById(id);
  if (info.style.display === "none" || info.style.display === "") {
    info.style.display = "block"; // Mostrar la información adicional
  } else {
    info.style.display = "none"; // Ocultar la información adicional
  }
}

    // Mostrar u ocultar la información adicional al hacer clic en el botón.
    function toggleInfo(infoId) {
       info = document.getElementById(infoId);
      if (info.style.display === "none") {
        info.style.display = "block";
      } else {
        info.style.display = "none";
      }
    }

// Función para limpiar el formulario y ocultar el mensaje
  document.addEventListener("DOMContentLoaded", function () {
    // Referencias a los elementos del botón y la caja
     moreInfoButton = document.getElementById("more-info-button");
     moreInfoBox = document.getElementById("more-info-box");

    // Evento de clic al botón para alternar la visibilidad de la caja
    moreInfoButton.addEventListener("click", function () {
      if (moreInfoBox.style.display === "none" || moreInfoBox.style.display === "") {
        moreInfoBox.style.display = "block";
      } else {
        moreInfoBox.style.display = "none";
      }
    });
  });

  function enviar() {
     nombre = document.getElementById("name").value;
     fecha_nacimiento = document.getElementById("fecha_nacimiento").value;
     dni = document.getElementById("dni").value;
     phone = document.getElementById("phone").value;
     email = document.getElementById("email").value;
     message = document.getElementById("message").value;
     contrasena = document.getElementById("contrasena").value;
     confirmarContrasena = document.getElementById("confirmar-contrasena").value;
     
    
    if (nombre && fecha_nacimiento && dni && phone && email && message && contrasena && confirmarContrasena) {
      if (contrasena === confirmarContrasena) {

        



        alert("¡Su mensaje fue recibido correctamente! A la brevedad nos pondremos en contacto.");
      
      // Limpiar el formulario
      document.getElementById("name").value = "";
      document.getElementById("fecha_nacimiento").value = "";
      document.getElementById("dni").value = "";
      document.getElementById("phone").value = "";
      document.getElementById("email").value = "";
      document.getElementById("contrasena").value = "";
      document.getElementById("confirmar-contrasena").value = "";
      document.getElementById("message").value = "";
    } else {
      alert("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.");
    }
  }else {
    alert("Por favor, complete todos los campos obligatorios.");
  }
}


 






