//static/core/js/v-recuprar-contrasena.js

var clave = document.getElementById("Email1");


const form = document.getElementById("form1");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", e =>{
    e.preventDefault();
    let mensajesMostrar = "";
    let entrar = false;
    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/
    mensaje.innerHTML = "";

    if (!regexEmail.test(Email1.value)) {
        mensajesMostrar += 'El correo electrónico ingresado no es válido. <br>'
        entrar = true
    }
    if (entrar) {
        mensaje.innerHTML = mensajesMostrar;
    } else {
        mensaje.innerHTML = "Se ha enviado un correo para recuperar su contraseña";
    }
})

document.getElementById('form-reset').addEventListener('submit', async e => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const res = await fetch('/api/password-reset/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });
  const data = await res.json();
  if (res.ok) {
    // muestra un alert o pinta un mensaje Bootstrap
    alert(data.detail);
  } else {
    alert(JSON.stringify(data));
  }
});

// static/core/js/v-recuperar-contrasena.js
(function () {
  'use strict';
  const form = document.getElementById('form1');
  if (!form) return;  // evita errores si no estás en la página de recuperar contraseña

  form.addEventListener('submit', function (event) {
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }
    form.classList.add('was-validated');
  }, false);
})();
