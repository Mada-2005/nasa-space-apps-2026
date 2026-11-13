// Lane B: the demo app. Only talks to the API in contracts/api.md.
// Ignores unknown fields so lane A can add fields safely.

const COLORS = { high: "#ff5a5f", medium: "#ffb84d", low: "#4dd4a0" };
const plotLayout = {
  paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
  font: { color: "#e8ecf8", size: 11 }, margin: { l: 40, r: 10, t: 24, b: 30 },
};

const map = L.map("map", { worldCopyJump: true }).setView([26.8, 30.8], 5);
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution: "&copy; OpenStreetMap, &copy; CARTO",
}).addTo(map);
const layer = L.layerGroup().addTo(map);

async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url} -> ${r.status}`);
  return r.json();
}

function showDetail(item) {
  document.getElementById("detail").innerHTML = `
    <h2>${item.location.name ?? item.id}</h2>
    <p>Score <b>${item.score.toFixed(2)}</b> (${item.label}) at ${item.time}</p>
    <p class="muted">${item.location.lat.toFixed(3)}, ${item.location.lon.toFixed(3)}</p>`;

  if (item.series?.length) {
    Plotly.newPlot("series", [{
      x: item.series.map(p => p.t), y: item.series.map(p => p.v),
      type: "scatter", mode: "lines+markers", line: { color: "#5ab0ff" },
    }], { ...plotLayout, title: "Over time" }, { displayModeBar: false });
  } else { document.getElementById("series").innerHTML = ""; }

  if (item.explanation?.length) {
    const ex = [...item.explanation].sort((a, b) => Math.abs(a.contribution) - Math.abs(b.contribution));
    Plotly.newPlot("why", [{
      y: ex.map(e => e.feature), x: ex.map(e => e.contribution), type: "bar", orientation: "h",
      marker: { color: ex.map(e => (e.contribution >= 0 ? "#ff5a5f" : "#4dd4a0")) },
    }], { ...plotLayout, title: "Why this score" }, { displayModeBar: false });
  } else { document.getElementById("why").innerHTML = ""; }
}

async function render(minScore = 0) {
  const b = await getJSON(`/api/predictions?min_score=${minScore}`);
  layer.clearLayers();
  for (const it of b.items) {
    L.circleMarker([it.location.lat, it.location.lon], {
      radius: 5 + 10 * it.score, color: COLORS[it.label] ?? "#5ab0ff", weight: 1, fillOpacity: 0.7,
    }).on("click", () => showDetail(it)).addTo(layer);
  }
  document.getElementById("footer").textContent =
    `${b.items.length} items | model ${b.model.name} v${b.model.version} | ` +
    Object.entries(b.model.metrics).map(([k, v]) => `${k}=${v.toFixed(3)}`).join("  ");
}

async function init() {
  const h = await getJSON("/health");
  const meta = await getJSON("/api/meta");
  document.getElementById("title").textContent = meta.challenge;
  document.getElementById("badges").innerHTML =
    (h.mock ? '<span class="badge mock">MOCK DATA</span>' : "") +
    `<span class="badge">contract v${meta.version}</span>`;
  const slider = document.getElementById("min");
  slider.addEventListener("change", () => render(+slider.value));
  slider.addEventListener("input", () => (document.getElementById("minval").textContent = (+slider.value).toFixed(2)));
  await render(0);
}

init().catch(e => { document.getElementById("detail").innerHTML = `<p>Error: ${e.message}</p>`; });
