function obtenerColor(variable) {
  return getComputedStyle(document.documentElement).getPropertyValue(variable).trim();
}

function formatearMoneda(valor) {
  return "$ " + Math.round(valor).toLocaleString("es-AR");
}

function formatearCompacto(valor) {
  const numero = Number(valor);
  if (Math.abs(numero) >= 1_000_000) return "$ " + (numero / 1_000_000).toFixed(1).replace(".", ",") + "M";
  if (Math.abs(numero) >= 1_000) return "$ " + (numero / 1_000).toFixed(0) + "K";
  return "$ " + numero.toFixed(0);
}

/* ---------- Tema oscuro / claro ---------- */
function inicializarTema() {
  const boton = document.getElementById("boton-tema");
  const raiz = document.documentElement;
  const guardado = localStorage.getItem("tema-panel");
  if (guardado) raiz.setAttribute("data-theme", guardado);

  boton?.addEventListener("click", () => {
    const prefiereOscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const actual = raiz.getAttribute("data-theme") || (prefiereOscuro ? "dark" : "light");
    const siguiente = actual === "dark" ? "light" : "dark";
    raiz.setAttribute("data-theme", siguiente);
    localStorage.setItem("tema-panel", siguiente);
    setTimeout(() => { if (window.actualizarGraficosDeTema) window.actualizarGraficosDeTema(); }, 260);
  });
}

/* ---------- Tooltip externo compartido ---------- */
function crearTooltipExterno(contenedor) {
  const div = document.createElement("div");
  div.className = "tooltip-grafico";
  contenedor.style.position = "relative";
  contenedor.appendChild(div);
  return div;
}

function posicionarTooltip(tooltipEl, contexto, contenedor) {
  const tooltipModel = contexto.tooltip;
  if (tooltipModel.opacity === 0) {
    tooltipEl.style.opacity = "0";
    return;
  }
  const rectContenedor = contenedor.getBoundingClientRect();
  const rectCanvas = contexto.chart.canvas.getBoundingClientRect();
  const offsetX = rectCanvas.left - rectContenedor.left;
  const offsetY = rectCanvas.top - rectContenedor.top;

  tooltipEl.style.opacity = "1";
  tooltipEl.style.left = offsetX + tooltipModel.caretX + "px";
  tooltipEl.style.top = offsetY + tooltipModel.caretY + "px";
}

/* ---------- Gráfico de ventas en el tiempo ---------- */
function crearGraficoVentas(datos, agrupadoPorSemana) {
  const canvas = document.getElementById("grafico-ventas");
  if (!canvas) return null;
  const contenedor = canvas.closest(".panel__area-grafico");
  const tooltipEl = crearTooltipExterno(contenedor);
  const colorSerie = obtenerColor("--serie-1");
  const colorGrid = obtenerColor("--gridline");
  const colorMuted = obtenerColor("--text-muted");
  const colorSuperficie = obtenerColor("--surface-1");

  return new Chart(canvas.getContext("2d"), {
    type: "line",
    data: {
      labels: datos.map((d) => d.fecha),
      datasets: [
        {
          label: agrupadoPorSemana ? "Ventas semanales" : "Ventas diarias",
          data: datos.map((d) => d.total),
          borderColor: colorSerie,
          backgroundColor: colorSerie + "1A",
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: colorSerie,
          pointHoverBorderColor: colorSuperficie,
          pointHoverBorderWidth: 2,
          fill: true,
          tension: 0.35,
          cubicInterpolationMode: "monotone",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      animation: { duration: 500, easing: "easeOutQuart" },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: false,
          external: (contexto) => {
            const modelo = contexto.tooltip;
            if (modelo.opacity === 0) { tooltipEl.style.opacity = "0"; return; }
            const punto = modelo.dataPoints[0];
            tooltipEl.innerHTML = "";
            const titulo = document.createElement("div");
            titulo.className = "tooltip-grafico__titulo";
            titulo.textContent = punto.label;
            const fila = document.createElement("div");
            fila.className = "tooltip-grafico__fila";
            const linea = document.createElement("span");
            linea.className = "tooltip-grafico__linea";
            linea.style.background = colorSerie;
            const valor = document.createElement("span");
            valor.className = "tooltip-grafico__valor";
            valor.textContent = formatearMoneda(punto.parsed.y);
            fila.append(linea, valor);
            tooltipEl.append(titulo, fila);
            posicionarTooltip(tooltipEl, contexto, contenedor);
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: colorMuted, font: { size: 11 }, maxRotation: 0, autoSkip: true, autoSkipPadding: 16 },
          border: { color: colorGrid },
        },
        y: {
          beginAtZero: true,
          grid: { color: colorGrid },
          border: { display: false },
          ticks: { color: colorMuted, font: { size: 11 }, callback: (v) => formatearCompacto(v), maxTicksLimit: 5 },
        },
      },
    },
  });
}

/* ---------- Gráfico de ventas por categoría ---------- */
function crearGraficoCategorias(datos) {
  const canvas = document.getElementById("grafico-categorias");
  if (!canvas) return null;
  const contenedor = canvas.closest(".panel__area-grafico");
  const tooltipEl = crearTooltipExterno(contenedor);
  const colorGrid = obtenerColor("--gridline");
  const colorMuted = obtenerColor("--text-muted");
  const colorPrimario = obtenerColor("--text-primary");

  const colores = datos.map((d) => obtenerColor(window.mapaColoresCategoria[d.categoria] || "--serie-1"));

  return new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: datos.map((d) => d.categoria),
      datasets: [
        {
          data: datos.map((d) => d.total),
          backgroundColor: colores,
          hoverBackgroundColor: colores,
          borderRadius: 5,
          barThickness: 22,
          borderSkipped: false,
        },
      ],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500, easing: "easeOutQuart" },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: false,
          external: (contexto) => {
            const modelo = contexto.tooltip;
            if (modelo.opacity === 0) { tooltipEl.style.opacity = "0"; return; }
            const punto = modelo.dataPoints[0];
            tooltipEl.innerHTML = "";
            const titulo = document.createElement("div");
            titulo.className = "tooltip-grafico__titulo";
            titulo.textContent = punto.label;
            const fila = document.createElement("div");
            fila.className = "tooltip-grafico__fila";
            const linea = document.createElement("span");
            linea.className = "tooltip-grafico__linea";
            linea.style.background = colores[punto.dataIndex];
            const valor = document.createElement("span");
            valor.className = "tooltip-grafico__valor";
            valor.textContent = formatearMoneda(punto.parsed.x);
            fila.append(linea, valor);
            tooltipEl.append(titulo, fila);
            posicionarTooltip(tooltipEl, contexto, contenedor);
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: { color: colorGrid },
          border: { display: false },
          ticks: { color: colorMuted, font: { size: 11 }, callback: (v) => formatearCompacto(v), maxTicksLimit: 4 },
        },
        y: {
          grid: { display: false },
          border: { display: false },
          ticks: { color: colorPrimario, font: { size: 12.5, weight: "600" } },
        },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  inicializarTema();

  const datosEl = document.getElementById("datos-panel");
  if (!datosEl) return;
  const datos = JSON.parse(datosEl.textContent);

  window.mapaColoresCategoria = datos.coloresCategoria;

  let graficoVentas = crearGraficoVentas(datos.serieVentas, datos.agrupadoPorSemana);
  let graficoCategorias = crearGraficoCategorias(datos.serieCategorias);

  window.actualizarGraficosDeTema = () => {
    graficoVentas?.destroy();
    graficoCategorias?.destroy();
    graficoVentas = crearGraficoVentas(datos.serieVentas, datos.agrupadoPorSemana);
    graficoCategorias = crearGraficoCategorias(datos.serieCategorias);
  };
});
