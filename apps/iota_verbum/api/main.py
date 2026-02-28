# api/main.py

from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.axiom_lambda_demo import router as axiom_lambda_router


app = FastAPI(title="Iota Verbum – Axiom Λ Demo")


# CORS – for local React demo and future hosted frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # add your real demo domain here later, e.g.
        # "https://demo.iotaverbum.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Attach the Axiom Λ / Desert Rule demo router
app.include_router(axiom_lambda_router)


# Simple healthcheck so you can test the app is running
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "axiom-lambda-demo"}
@app.get("/demo/jumo", response_class=HTMLResponse)
async def jumo_demo() -> str:
    # Simple HTML + JS page that calls /axiom-lambda/assess
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Jumo – Axiom Lambda Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; background: #f9fafb; }
    h1 { margin-bottom: 0.25rem; }
    .card { background: white; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .row { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .label { font-size: 0.85rem; color: #4b5563; margin-bottom: 0.25rem; }
    select, button { padding: 0.5rem 0.75rem; border-radius: 0.5rem; border: 1px solid #d1d5db; font-size: 0.9rem; }
    button { background: #2563eb; color: white; border-color: #2563eb; cursor: pointer; }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    pre { background: #111827; color: #e5e7eb; padding: 0.75rem; border-radius: 0.5rem; font-size: 0.8rem; overflow-x: auto; }
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
    .badge-ok { background: #dcfce7; color: #166534; }
    .badge-warn { background: #fef3c7; color: #92400e; }
    .badge-bad { background: #fee2e2; color: #991b1b; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Jumo + Axiom Λ Governance Demo</h1>
    <p style="color:#4b5563; font-size:0.9rem;">
      Simple UI to send stress-test scenarios to the Axiom Λ endpoint
      at <code>/axiom-lambda/assess</code>.
    </p>
  </div>

  <div class="card">
    <div class="row">
      <div style="flex: 1;">
        <div class="label">Scenario</div>
        <select id="scenarioSelect">
          <option value="honest_borrower">Honest Struggling Borrower</option>
          <option value="deceptive_borrower">Deceptive High-Income Borrower</option>
          <option value="predatory_expansion">Predatory Lending Expansion (6 months)</option>
          <option value="algorithmic_redlining">Algorithmic Redlining (1 year)</option>
          <option value="profit_absolutism">Profit Absolutism (5 years)</option>
        </select>
      </div>
      <div style="display:flex; align-items:flex-end;">
        <button id="runBtn">Run Stress Test</button>
      </div>
    </div>

    <div id="statusLine" style="font-size:0.85rem; color:#6b7280; margin-top:0.25rem;">
      Ready.
    </div>
  </div>

  <div class="card">
    <h2 style="font-size:1.1rem; margin-bottom:0.5rem;">Governance Assessment</h2>
    <div id="summary" style="margin-bottom:0.75rem; font-size:0.9rem;"></div>
    <pre id="rawJson">{}</pre>
  </div>

  <script>
    const runBtn = document.getElementById("runBtn");
    const scenarioSelect = document.getElementById("scenarioSelect");
    const rawJson = document.getElementById("rawJson");
    const summary = document.getElementById("summary");
    const statusLine = document.getElementById("statusLine");

    function badge(text, level) {
      const cls =
        level === "ok" ? "badge badge-ok" :
        level === "warn" ? "badge badge-warn" :
        "badge badge-bad";
      return `<span class="${cls}">${text}</span>`;
    }

    runBtn.addEventListener("click", async () => {
      const scenarioId = scenarioSelect.value;
      runBtn.disabled = true;
      statusLine.textContent = "Running stress test...";

      try {
        const res = await fetch("/axiom-lambda/assess", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            scenario_id: scenarioId,
            meta: { source: "jumo_demo_page" }
          }),
        });

        if (!res.ok) {
          statusLine.textContent = "Error from server: " + res.status;
          summary.innerHTML = "";
          rawJson.textContent = "{}";
          runBtn.disabled = false;
          return;
        }

        const data = await res.json();
        rawJson.textContent = JSON.stringify(data, null, 2);

        // Neutral governance summary
        const status = data.status || "UNKNOWN";
        const violation = data.justice_eval && data.justice_eval.violation;
        const vType = data.justice_eval && data.justice_eval.type;
        const rec = data.recommendation || "No explicit recommendation.";

        let level = "ok";
        if (violation) level = "bad";

        summary.innerHTML = `
          <div style="margin-bottom:0.35rem;">
            ${badge(status, level)}
          </div>
          <div style="margin-bottom:0.25rem;">
            <strong>Case profile:</strong> ${data.case_profile || "unspecified"}
          </div>
          <div style="margin-bottom:0.25rem;">
            <strong>Governance finding:</strong>
            ${violation ? "Violation detected (" + (vType || "unspecified") + ")."
                        : "No governance violation detected."}
          </div>
          <div>
            <strong>System recommendation:</strong> ${rec}
          </div>
        `;

        statusLine.textContent = "Completed.";
      } catch (err) {
        console.error(err);
        statusLine.textContent = "Error calling Axiom Λ endpoint. See console.";
        summary.innerHTML = "";
        rawJson.textContent = "{}";
      } finally {
        runBtn.disabled = false;
      }
    });
  </script>
</body>
</html>
    """

