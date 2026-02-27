# Iota Verbum Demo Application

This repository contains a proof‑of‑concept implementation of the Iota Verbum stack.  It shows how to integrate the alignment middleware, drift detection, A/B testing, simple attestation tooling and governance hooks into a single Node.js service.

> **Note**: This is a demonstration.  A production deployment of Iota Verbum should replace the simple heuristics here with the full λ‑corpus, modal reasoning engine and canonical constitution described in the Phase 6 specification.

## Structure

- `server.js` – Express server exposing chat, configuration and experiment endpoints.
- `alignment-middleware.js` – Orchestrates OpenAI chat, drift monitoring and function calling.
- `alignment-core.js` – Core classes and heuristics for vectorising responses and computing drift metrics.
- `alert-system.js` – Sends Slack/email alerts when drift is high.
- `ab-testing.js` – Simple A/B testing framework for interventions.
- `batch-attestation.js` – Toy batch attestation utility for auditing multiple files.
- `train_scoring_model.py` – Python script to train a machine‑learning model for the scoring heuristics.
- `.env.example` – Sample environment variables.  Copy to `.env` and fill in your credentials.

## Prerequisites

1. [Node.js](https://nodejs.org/) (v18 or newer) and npm installed on your machine.
2. An [OpenAI API key](https://platform.openai.com/) for GPT‑5.1 or similar model.
3. (Optional) Slack token and SMTP credentials for alerting.
4. (Optional) Python 3.9+ with `pip` to train the ML models.

## Installation

1. **Clone or copy this repository** to your local machine.
2. Navigate into the app directory:

   ```bash
   cd iotaverbum_app
   ```
3. **Install dependencies**:

   ```bash
   npm install
   ```
   > If you see network‑related errors during `npm install`, verify your network settings or use a mirror registry.  The `@slack/web-api` package is optional; omit it from `package.json` if you do not require Slack alerts.

4. **Configure environment variables**:

   Copy `.env.example` to `.env` and edit the values:

   ```bash
   cp .env.example .env
   nano .env # or your editor of choice
   ```

   Set `OPENAI_API_KEY` to your OpenAI key, fill in Slack and SMTP credentials if you wish to receive drift alerts, and adjust `PORT` if needed.

## Running the Server

Start the server with:

```bash
npm start
```

The server will run on `http://localhost:3000` by default.  You can test the chat endpoint with a tool like `curl` or [Postman](https://www.postman.com/):

```bash
curl -X POST http://localhost:3000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"userId":"user1","conversationId":"conv1","messages":[{"role":"user","content":"Tell me about John 17"}]}'
```

The response JSON contains the assistant’s reply and metadata about drift and interventions.

## Customising Basins

The moral “basins” define the gravitational forces for drift detection.  To update them at runtime, call the `/api/alignment/config` endpoint:

```bash
curl -X POST http://localhost:3000/api/alignment/config \
  -H 'Content-Type: application/json' \
  -d '{"basins":[{"name":"Helpfulness","dimensions":["clarity","completeness"],"strength":3.0}, ...],"interventionsEnabled":true}'
```

## Running Batch Attestations

The `run_attestation` function can be invoked by the model to audit multiple text files.  You can also run it manually in Node:

```bash
node -e "require('./batch-attestation').run(['path/to/file1.txt','path/to/file2.txt']).then(console.log)"
```

## A/B Experiments

You can create an experiment via POST to `/api/experiments`:

```bash
curl -X POST http://localhost:3000/api/experiments \
  -H 'Content-Type: application/json' \
  -d '{"id":"exp1","name":"Intervention Efficacy","hypothesis":"Interventions reduce drift","controlBasinConfig":null,"treatmentBasinConfig":null,"sampleSize":500}'
```

Then supply `experimentId":"exp1"` in chat requests to assign users automatically.  Results are available at `/api/experiments/exp1/results`.

## Training Scoring Models

If you wish to replace the heuristic scoring with a machine‑learning model, prepare a CSV with a column of free‑text responses (`text`) and labelled scores for each dimension (`clarity`, `completeness`, etc.).

Install the required Python packages:

```bash
pip install pandas numpy scikit-learn transformers sentence-transformers joblib
```

Then run:

```bash
python train_scoring_model.py --data my_dataset.csv --text-col text --out my_model
```

This produces `my_model.json` and `my_model.models.pkl`.  You would then modify `alignment-core.js` to load and use these models instead of the heuristic functions.

## Extending the Demo

This demo lays the groundwork for integrating a full modal engine, canonical constitution and attestation logic.  To extend it:

1. Replace the heuristics in `alignment-core.js` with your trained models.
2. Integrate the λ‑doc corpus and modal reasoning engine to compute identities, enactments and effects for real witnesses.
3. Implement the canonical constitution API (Phase 6) and connect it to the drift monitor.
4. Build a front‑end dashboard using React or your framework of choice.  The provided components (AlignmentMonitor, BasinTuningUI, ExperimentResults) in earlier phases can be adapted.

## Contributing

Feedback and contributions are welcome.  This project began as an exploration of computational theology and AI governance; your ideas can help refine the vision.