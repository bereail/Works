const cuerpoTabla = document.getElementById("cuerpo-tabla");
const mensajeVacio = document.getElementById("mensaje-vacio");
const buscador = document.getElementById("buscador");
const contadorResultados = document.getElementById("contador-resultados");
const toast = document.getElementById("toast");
const textoToast = document.getElementById("texto-toast");

const ETIQUETAS_CLASE_ESTADO = {
  Nuevo: "estado-nuevo",
  Contactado: "estado-contactado",
  Convertido: "estado-convertido",
  Descartado: "estado-descartado",
};

let leads = [];
let idsConocidos = new Set();
let primeraCarga = true;

async function cargarLeads() {
  const respuesta = await fetch("/api/leads");
  const datos = await respuesta.json();

  const idsNuevos = datos
    .map((lead) => lead.id)
    .filter((id) => !idsConocidos.has(id));

  leads = datos;
  idsConocidos = new Set(datos.map((lead) => lead.id));

  renderizarKpis();
  renderizarTabla(idsNuevos);
  primeraCarga = false;
}

function renderizarKpis() {
  const conteos = { Nuevo: 0, Contactado: 0, Convertido: 0, Descartado: 0 };
  leads.forEach((lead) => {
    if (conteos[lead.estado] !== undefined) conteos[lead.estado] += 1;
  });

  document.getElementById("kpi-total").textContent = leads.length;
  document.getElementById("kpi-nuevo").textContent = conteos.Nuevo;
  document.getElementById("kpi-contactado").textContent = conteos.Contactado;
  document.getElementById("kpi-convertido").textContent = conteos.Convertido;
  document.getElementById("kpi-descartado").textContent = conteos.Descartado;
}

function filtrarLeads() {
  const termino = buscador.value.trim().toLowerCase();
  if (!termino) return leads;

  return leads.filter(
    (lead) =>
      lead.nombre.toLowerCase().includes(termino) ||
      lead.email.toLowerCase().includes(termino)
  );
}

function renderizarTabla(idsNuevos = []) {
  const filtrados = filtrarLeads();

  contadorResultados.textContent = `${filtrados.length} de ${leads.length} lead(s)`;
  mensajeVacio.style.display = filtrados.length === 0 ? "block" : "none";

  cuerpoTabla.innerHTML = "";

  filtrados.forEach((lead) => {
    const fila = document.createElement("tr");
    if (!primeraCarga && idsNuevos.includes(lead.id)) {
      fila.classList.add("fila-nueva");
    }

    fila.innerHTML = `
      <td>
        <div class="nombre-lead">${escaparHtml(lead.nombre)}</div>
        <div class="email-lead">${escaparHtml(lead.email)}</div>
      </td>
      <td>${escaparHtml(lead.telefono || "—")}</td>
      <td><span class="chip-origen">${escaparHtml(lead.origen)}</span></td>
      <td>${lead.fecha_creacion}</td>
      <td></td>
    `;

    const celdaEstado = fila.querySelector("td:last-child");
    celdaEstado.appendChild(crearSelectorEstado(lead));

    cuerpoTabla.appendChild(fila);
  });
}

function crearSelectorEstado(lead) {
  const select = document.createElement("select");
  select.className = `selector-estado ${ETIQUETAS_CLASE_ESTADO[lead.estado]}`;

  ESTADOS.forEach((estado) => {
    const opcion = document.createElement("option");
    opcion.value = estado;
    opcion.textContent = estado;
    opcion.selected = estado === lead.estado;
    select.appendChild(opcion);
  });

  select.addEventListener("change", async () => {
    const nuevoEstado = select.value;
    select.disabled = true;
    select.classList.add("select-guardando");

    try {
      const respuesta = await fetch(`/api/leads/${lead.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado: nuevoEstado }),
      });

      if (!respuesta.ok) throw new Error("No se pudo actualizar el estado.");

      const actualizado = await respuesta.json();
      const indice = leads.findIndex((l) => l.id === actualizado.id);
      if (indice !== -1) leads[indice] = actualizado;

      select.className = `selector-estado ${ETIQUETAS_CLASE_ESTADO[nuevoEstado]}`;
      renderizarKpis();
      mostrarToast(`${lead.nombre} ahora está en estado "${nuevoEstado}"`);
    } catch (error) {
      select.value = lead.estado;
      mostrarToast("Ocurrió un error al actualizar el estado.");
    } finally {
      select.disabled = false;
      select.classList.remove("select-guardando");
    }
  });

  return select;
}

function mostrarToast(mensaje) {
  textoToast.textContent = mensaje;
  toast.classList.add("visible");
  window.clearTimeout(mostrarToast._temporizador);
  mostrarToast._temporizador = window.setTimeout(() => {
    toast.classList.remove("visible");
  }, 2600);
}

function escaparHtml(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

buscador.addEventListener("input", () => renderizarTabla());

cargarLeads();
setInterval(cargarLeads, 5000);
