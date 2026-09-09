const formulario = document.getElementById("form-contacto");
const botonEnviar = document.getElementById("boton-enviar");
const mensajeError = document.getElementById("mensaje-error");
const tarjetaFormulario = document.getElementById("tarjeta-formulario");
const confirmacion = document.getElementById("confirmacion");
const textoConfirmacion = document.getElementById("texto-confirmacion");
const botonNuevaConsulta = document.getElementById("boton-nueva-consulta");

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mensajeError.textContent = "";

  const datos = Object.fromEntries(new FormData(formulario).entries());

  if (!datos.nombre.trim() || !datos.email.trim()) {
    mensajeError.textContent = "Completá al menos tu nombre y email para continuar.";
    return;
  }

  botonEnviar.disabled = true;
  botonEnviar.classList.add("cargando");

  try {
    const respuesta = await fetch("/api/leads", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    const resultado = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(resultado.error || "No pudimos registrar tu consulta.");
    }

    textoConfirmacion.textContent =
      `Un especialista de Nimbus va a contactarte a ${resultado.email} a la brevedad.`;
    confirmacion.classList.add("visible");
  } catch (error) {
    mensajeError.textContent = error.message;
  } finally {
    botonEnviar.disabled = false;
    botonEnviar.classList.remove("cargando");
  }
});

botonNuevaConsulta.addEventListener("click", () => {
  confirmacion.classList.remove("visible");
  formulario.reset();
  window.setTimeout(() => document.getElementById("nombre").focus(), 260);
});
