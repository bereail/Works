const chat = document.getElementById("chat");
const formulario = document.getElementById("formulario-envio");
const entradaMensaje = document.getElementById("entrada-mensaje");
const subtitulo = document.getElementById("subtitulo");

function obtenerTelefonoSimulado() {
  const guardado = localStorage.getItem("telefono_simulado");
  if (guardado) {
    return guardado;
  }
  const numero = `+54 9 11 ${Math.floor(1000 + Math.random() * 8999)}-${Math.floor(
    1000 + Math.random() * 8999
  )}`;
  localStorage.setItem("telefono_simulado", numero);
  return numero;
}

const telefono = obtenerTelefonoSimulado();

function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function formatearTexto(texto) {
  return escaparHtml(texto)
    .replace(/\*(.+?)\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

function agregarBurbuja(texto, hora, esEntrante) {
  const fila = document.createElement("div");
  fila.className = `fila-burbuja ${esEntrante ? "entrante" : "saliente"}`;

  const burbuja = document.createElement("div");
  burbuja.className = "burbuja";
  burbuja.innerHTML = `${formatearTexto(texto)}<span class="hora">${hora}</span>`;

  fila.appendChild(burbuja);
  chat.appendChild(fila);
  desplazarAbajo();
}

function desplazarAbajo() {
  chat.scrollTop = chat.scrollHeight;
}

function mostrarEscribiendo() {
  const fila = document.createElement("div");
  fila.className = "fila-burbuja saliente";
  fila.id = "indicador-escribiendo";

  const burbuja = document.createElement("div");
  burbuja.className = "burbuja burbuja-escribiendo";
  burbuja.innerHTML = '<span class="punto"></span><span class="punto"></span><span class="punto"></span>';

  fila.appendChild(burbuja);
  chat.appendChild(fila);
  desplazarAbajo();
}

function ocultarEscribiendo() {
  const indicador = document.getElementById("indicador-escribiendo");
  if (indicador) {
    indicador.remove();
  }
}

function horaActual() {
  const ahora = new Date();
  return ahora.toTimeString().slice(0, 5);
}

async function mostrarRespuestasBot(respuestas) {
  subtitulo.textContent = "escribiendo…";
  mostrarEscribiendo();

  await esperar(700);
  ocultarEscribiendo();

  for (let indice = 0; indice < respuestas.length; indice += 1) {
    agregarBurbuja(respuestas[indice].texto, respuestas[indice].hora, false);
    if (indice < respuestas.length - 1) {
      mostrarEscribiendo();
      await esperar(550);
      ocultarEscribiendo();
    }
  }

  subtitulo.textContent = "en línea";
}

function esperar(milisegundos) {
  return new Promise((resolver) => setTimeout(resolver, milisegundos));
}

async function enviarMensaje(texto) {
  agregarBurbuja(texto, horaActual(), true);

  const respuesta = await fetch("/mensaje", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ telefono, texto }),
  });
  const respuestasBot = await respuesta.json();
  await mostrarRespuestasBot(respuestasBot);
}

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();
  const texto = entradaMensaje.value.trim();
  if (!texto) {
    return;
  }
  entradaMensaje.value = "";
  enviarMensaje(texto);
});

async function iniciarChat() {
  const historial = await (await fetch(`/historial/${encodeURIComponent(telefono)}`)).json();

  if (historial.length === 0) {
    const saludo = await (await fetch(`/saludo/${encodeURIComponent(telefono)}`)).json();
    await mostrarRespuestasBot(saludo);
    return;
  }

  historial.forEach((mensaje) => {
    agregarBurbuja(mensaje.texto, mensaje.hora, mensaje.es_entrante);
  });
}

iniciarChat();
