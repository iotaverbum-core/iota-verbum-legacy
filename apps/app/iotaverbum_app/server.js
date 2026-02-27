/*
 * Entrypoint for the Iota Verbum demo server. This Express app exposes
 * chat endpoints backed by the alignment middleware, configuration
 * management, experiment reporting and dashboard stats. To run:
 *   npm install
 *   cp .env.example .env # adjust values
 *   npm start
 */

require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const AlignmentMiddleware = require('./alignment-middleware');

const app = express();
app.use(cors());
app.use(bodyParser.json({ limit: '2mb' }));

const middleware = new AlignmentMiddleware({});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { userId, conversationId, messages, experimentId } = req.body;
    if (!userId || !conversationId || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'userId, conversationId and messages are required' });
    }
    const result = await middleware.handleRequest(userId, conversationId, messages, { experimentId });
    res.json(result);
  } catch (err) {
    console.error('Chat error:', err);
    res.status(500).json({ error: err.message });
  }
});

// Alignment config endpoint
app.post('/api/alignment/config', (req, res) => {
  const { basins, interventionsEnabled } = req.body;
  if (basins) {
    middleware.config.defaultBasins = basins;
  }
  if (interventionsEnabled !== undefined) {
    middleware.config.defaultInterventionsEnabled = interventionsEnabled;
  }
  res.json({ ok: true, basins: middleware.config.defaultBasins, interventionsEnabled: middleware.config.defaultInterventionsEnabled });
});

// Dashboard stats
app.get('/api/alignment/dashboard', (req, res) => {
  const stats = middleware.getFleetStats();
  res.json(stats);
});

// Experiment endpoints
const experiments = middleware.abTesting;
app.post('/api/experiments', (req, res) => {
  const config = req.body;
  if (!config || !config.id) {
    return res.status(400).json({ error: 'Experiment id is required' });
  }
  const exp = experiments.createExperiment(config);
  exp.status = 'running';
  exp.startDate = new Date().toISOString();
  res.json(exp);
});

app.get('/api/experiments/:id/results', (req, res) => {
  const expId = req.params.id;
  const results = experiments.getResults(expId);
  if (!results) {
    return res.status(404).json({ error: 'Experiment not found' });
  }
  res.json(results);
});

// Serve static files from public (if front‑end built here)
app.use(express.static('public'));

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Iota Verbum demo server listening on port ${PORT}`);
});