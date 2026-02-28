from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/console", tags=["console"])

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>iota verbum – Reviewer Console</title>
  <style>
    :root {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color-scheme: light dark;
    }
    body {
      margin: 0;
      padding: 0;
      background: #0f172a;
      color: #e5e7eb;
    }
    header {
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #1f2937;
      background: radial-gradient(circle at top left, #1d4ed8 0, #0f172a 55%);
    }
    header h1 {
      margin: 0;
      font-size: 1.4rem;
    }
    header p {
      margin: 0.25rem 0 0;
      font-size: 0.85rem;
      color: #cbd5f5;
    }
    main {
      padding: 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1rem;
    }
    .card {
      background: #020617;
      border-radius: 0.75rem;
      border: 1px solid #1f2937;
      padding: 1rem 1.1rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    }
    .card h2 {
      font-size: 1rem;
      margin: 0 0 0.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    h3 {
      font-size: 0.8rem;
      margin: 0.4rem 0 0.2rem;
      color: #9ca3af;
    }
    .chip {
      font-size: 0.7rem;
      padding: 0.15rem 0.45rem;
      border-radius: 999px;
      border: 1px solid #4b5563;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: #9ca3af;
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.8rem;
      padding: 0.15rem 0.55rem;
      border-radius: 999px;
      background: #111827;
    }
    .dot {
      width: 0.55rem;
      height: 0.55rem;
      border-radius: 999px;
      background: #6b7280;
    }
    .dot.ok { background: #22c55e; }
    .dot.warn { background: #eab308; }
    .dot.fail { background: #ef4444; }
    .meta {
      font-size: 0.78rem;
      color: #9ca3af;
      margin-bottom: 0.35rem;
    }
    .meta span + span::before {
      content: "•";
      margin: 0 0.4rem;
      color: #4b5563;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.78rem;
      margin-top: 0.35rem;
    }
    th, td {
      padding: 0.3rem 0.35rem;
      border-bottom: 1px solid #111827;
      text-align: left;
    }
    th {
      font-weight: 500;
      color: #9ca3af;
    }
    tbody tr:last-child td {
      border-bottom: none;
    }
    .tag {
      font-size: 0.7rem;
      padding: 0.1rem 0.4rem;
      border-radius: 999px;
      background: #111827;
      color: #9ca3af;
      border: 1px solid #1f2937;
    }
    .small {
      font-size: 0.75rem;
      color: #9ca3af;
      margin-top: 0.4rem;
    }
    #global-error {
      padding: 0.75rem 1.5rem;
      font-size: 0.8rem;
      background: #451a1a;
      color: #fecaca;
      border-bottom: 1px solid #7f1d1d;
      display: none;
    }
    a {
      color: #93c5fd;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <header>
    <h1>iota verbum – reviewer console</h1>
    <p>Signed, small, and honest. Every endpoint accountable to the Word.</p>
  </header>

  <div id="global-error"></div>

  <main>
    <section class="card" id="card-health">
      <h2>
        Health
        <span class="chip">/check</span>
      </h2>
      <div class="meta">
        <span id="health-signature"></span>
        <span id="health-timestamp"></span>
      </div>
      <div class="status-pill" id="health-pill">
        <span class="dot" id="health-dot"></span>
        <span id="health-status-label">Loading…</span>
      </div>
      <div class="small" id="health-details"></div>
    </section>

    <section class="card" id="card-report">
      <h2>
        Latest report
        <span class="chip">/report/latest</span>
      </h2>
      <div class="meta">
        <span id="report-filename"></span>
        <span id="report-timestamp"></span>
      </div>
      <table>
        <tbody>
          <tr>
            <th>Modal OK</th>
            <td id="report-modal-ok">–</td>
          </tr>
          <tr>
            <th>Score</th>
            <td id="report-score">–</td>
          </tr>
        </tbody>
      </table>
      <div class="small">
        Source: <span id="report-source">engine_report_v1 (parsed from results/)</span>
      </div>
    </section>

    <section class="card" id="card-phases">
      <h2>
        Build roadmap
        <span class="chip">/phases/status</span>
      </h2>
      <div class="meta">
        <span id="phases-timestamp"></span>
        <span id="phases-signature"></span>
      </div>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Phase</th>
            <th>Track</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody id="phases-body"></tbody>
      </table>
      <div class="small">
        Core phases should trend green; expansion phases may remain partial.
      </div>
    </section>

    <section class="card" id="card-theology">
      <h2>
        Theology map (demo)
        <span class="chip">/hinges, /iv-maps, /arcs/canonical, /iv/pairs</span>
      </h2>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>ID</th>
            <th>Summary</th>
          </tr>
        </thead>
        <tbody id="theology-body"></tbody>
      </table>
      <div class="small">
        Lightweight glance at hinge texts, canonical arcs, IV maps, and IV pairs.
        Full atlas UI belongs to a later phase.
      </div>
    </section>

    <section class="card" id="card-languages">
      <h2>
        Languages
        <span class="chip">/languages</span>
      </h2>
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
          </tr>
        </thead>
        <tbody id="languages-body"></tbody>
      </table>
      <div class="small">
        Variant summaries and density are served from repository-backed data.
      </div>
    </section>

    <section class="card" id="card-variants">
      <h2>
        Variant lab
        <span class="chip">/languages/variants, /languages/variants/density, /variants/provenance</span>
      </h2>

      <h3>By language</h3>
      <table>
        <thead>
          <tr>
            <th>Lang</th>
            <th>Variants</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody id="variants-lang-body"></tbody>
      </table>

      <h3>By book (density)</h3>
      <table>
        <thead>
          <tr>
            <th>Unit / Book</th>
            <th>Density</th>
          </tr>
        </thead>
        <tbody id="variants-density-body"></tbody>
      </table>

      <div class="small" id="variants-provenance">
        Provenance: loading…
      </div>
    </section>
  </main>

  <script>
    async function fetchJson(path) {
      const res = await fetch(path);
      if (!res.ok) {
        throw new Error(path + " → HTTP " + res.status);
      }
      return await res.json();
    }

    function setDot(id, state) {
      const dot = document.getElementById(id);
      if (!dot) return;
      dot.classList.remove("ok", "warn", "fail");
      if (state) {
        dot.classList.add(state);
      }
    }

    function safeText(id, value) {
      const el = document.getElementById(id);
      if (!el) return;
      el.textContent = value ?? "";
    }

    async function loadConsole() {
      try {
        const [
          check,
          latest,
          phases,
          hinges,
          ivMaps,
          arcs,
          languages,
          ivPairs,
          langVariants,
          density,
          provenance
        ] = await Promise.all([
          fetchJson("/check"),
          fetchJson("/report/latest").catch(() => null),
          fetchJson("/phases/status"),
          fetchJson("/hinges"),
          fetchJson("/iv-maps"),
          fetchJson("/arcs/canonical"),
          fetchJson("/languages"),
          fetchJson("/iv/pairs").catch(() => null),
          fetchJson("/languages/variants").catch(() => null),
          fetchJson("/languages/variants/density").catch(() => null),
          fetchJson("/variants/provenance").catch(() => null)
        ]);

        // Health
        const ok = check && check.status === "ok";
        safeText("health-signature", check.signature || "");
        safeText("health-timestamp", check.timestamp || "");
        setDot("health-dot", ok ? "ok" : "fail");
        safeText("health-status-label", ok ? "Healthy" : "Check failed");
        safeText(
          "health-details",
          "Lexicon loaded: " + (!!check.lexicon_loaded) +
            " • Annotations loaded: " + (!!check.annotations_loaded)
        );

        // Report
        if (latest && latest.latest) {
          safeText("report-filename", latest.latest.filename || "");
          safeText("report-timestamp", latest.latest.timestamp || "");
          safeText("report-modal-ok", String(latest.latest.modal_ok));
          safeText("report-score", String(latest.latest.score));
        } else {
          safeText("report-filename", "No reports found");
          safeText("report-modal-ok", "–");
          safeText("report-score", "–");
        }

        // Phases
        safeText("phases-timestamp", phases.timestamp || "");
        safeText("phases-signature", phases.signature || "");
        const tbody = document.getElementById("phases-body");
        tbody.innerHTML = "";
        (phases.phases || []).forEach((p) => {
          const tr = document.createElement("tr");
          const statusTag = document.createElement("span");
          statusTag.className = "tag";
          statusTag.textContent = p.status || "unknown";
          tr.innerHTML = `
            <td>${p.phase}</td>
            <td>${p.name}</td>
            <td>${p.track}</td>
            <td></td>
          `;
          tr.children[3].appendChild(statusTag);
          tbody.appendChild(tr);
        });

        // Theology map (summary)
        const theologyBody = document.getElementById("theology-body");
        theologyBody.innerHTML = "";

        // Hinges
        (hinges || []).slice(0, 5).forEach((h) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td><span class="tag">hinge</span></td>
            <td>${h.id || h.hinge_id || ""}</td>
            <td>${h.label || h.ref || ""}</td>
          `;
          theologyBody.appendChild(tr);
        });

        // Canonical arcs
        const arcsData = arcs && arcs.edges ? arcs : null;
        if (arcsData && Array.isArray(arcsData.edges)) {
          arcsData.edges.slice(0, 5).forEach((e) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td><span class="tag">arc</span></td>
              <td>${e.from} → ${e.to}</td>
              <td>${e.type || ""}</td>
            `;
            theologyBody.appendChild(tr);
          });
        }

        // IV maps (engine data)
        if (Array.isArray(ivMaps)) {
          ivMaps.slice(0, 5).forEach((m) => {
            const fromId = m.source_id || m.from || "";
            const toId = m.target_id || m.to || "";
            const summary = m.theme || m.note || "";
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td><span class="tag">iv-map</span></td>
              <td>${fromId} → ${toId}</td>
              <td>${summary}</td>
            `;
            theologyBody.appendChild(tr);
          });
        }

        // IV pairs (demo aggregate)
        if (ivPairs && Array.isArray(ivPairs.pairs)) {
          ivPairs.pairs.slice(0, 5).forEach((p) => {
            const fromId = p.from || "";
            const toId = p.to || "";
            const summary = p.theme || p.note || "";
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td><span class="tag">iv-pair demo</span></td>
              <td>${fromId} → ${toId}</td>
              <td>${summary}</td>
            `;
            theologyBody.appendChild(tr);
          });
        }

        // Languages
        const langsBody = document.getElementById("languages-body");
        langsBody.innerHTML = "";
        (languages || []).forEach((lang) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${lang.code || ""}</td>
            <td>${lang.name || ""}</td>
          `;
          langsBody.appendChild(tr);
        });

        // Variant lab – by language
        const vLangBody = document.getElementById("variants-lang-body");
        vLangBody.innerHTML = "";
        if (Array.isArray(langVariants)) {
          langVariants.forEach((v) => {
            const langCode = v.language || v.code || v.lang_code || "";
            const count = v.variant_count || v.count || 0;
            const note = v.note || "";
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>${langCode}</td>
              <td>${count}</td>
              <td>${note}</td>
            `;
            vLangBody.appendChild(tr);
          });
        }

        // Variant lab – density
        const densityBody = document.getElementById("variants-density-body");
        densityBody.innerHTML = "";
        if (density && typeof density === "object") {
          Object.entries(density).forEach(([unit, val]) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>${unit}</td>
              <td>${val}</td>
            `;
            densityBody.appendChild(tr);
          });
        }

        // Provenance note
        if (provenance) {
          const examples =
            provenance.examples ||
            provenance.sample ||
            provenance.records ||
            [];
          const count = Array.isArray(examples) ? examples.length : 0;
          const note =
            (provenance.note || provenance.message || "Provenance summary available") +
            " • examples: " +
            count;
          safeText("variants-provenance", note);
        } else {
          safeText(
            "variants-provenance",
            "Provenance endpoint unavailable right now (no witness samples loaded)."
          );
        }

      } catch (err) {
        console.error(err);
        const box = document.getElementById("global-error");
        box.style.display = "block";
        box.textContent = "Error loading console: " + err.message;
        setDot("health-dot", "fail");
        safeText("health-status-label", "Console load error");
      }
    }

    document.addEventListener("DOMContentLoaded", loadConsole);
  </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def reviewer_console():
    """
    Minimal reviewer console for Step B.

    Provides a human-readable snapshot of:
      - /check
      - /report/latest
      - /phases/status
      - /hinges
      - /iv-maps
      - /arcs/canonical
      - /iv/pairs
      - /languages
      - /languages/variants
      - /languages/variants/density
      - /variants/provenance
    """
    return HTML
