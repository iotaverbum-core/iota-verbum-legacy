/*
 * AlertSystem sends notifications when drift metrics exceed thresholds.
 * It supports Slack and email alerts. To enable Slack notifications,
 * provide a valid Slack token and channel ID via environment variables.
 * To enable email, configure SMTP credentials. Cooldowns prevent spam.
 */

const { WebClient } = require('@slack/web-api');
const nodemailer = require('nodemailer');

class AlertSystem {
  constructor(config = {}) {
    const slackToken = process.env.SLACK_TOKEN || config.slackToken;
    const channel = process.env.ALERT_CHANNEL_ID || config.channel;
    this.slackClient = slackToken ? new WebClient(slackToken) : null;
    this.channel = channel;
    // Configure nodemailer if SMTP creds supplied
    const smtpHost = process.env.SMTP_HOST || (config.emailConfig && config.emailConfig.host);
    const smtpUser = process.env.SMTP_USER || (config.emailConfig && config.emailConfig.auth && config.emailConfig.auth.user);
    const smtpPass = process.env.SMTP_PASS || (config.emailConfig && config.emailConfig.auth && config.emailConfig.auth.pass);
    const smtpPort = process.env.SMTP_PORT || (config.emailConfig && config.emailConfig.port);
    if (smtpHost && smtpUser && smtpPass) {
      this.emailTransport = nodemailer.createTransport({
        host: smtpHost,
        port: smtpPort || 587,
        secure: false,
        auth: { user: smtpUser, pass: smtpPass }
      });
    } else {
      this.emailTransport = null;
    }
    this.cooldowns = new Map();
    this.thresholds = config.thresholds || {
      highRisk: 0.7,
      mediumRisk: 0.45,
      fleetHighRiskPercent: 0.15
    };
  }

  isOnCooldown(key, durationMs) {
    const last = this.cooldowns.get(key);
    if (!last) return false;
    return Date.now() - last < durationMs;
  }

  setCooldown(key) {
    this.cooldowns.set(key, Date.now());
  }

  async checkAndAlert(conversationId, userId, drift) {
    if (drift.riskScore >= this.thresholds.highRisk) {
      await this.sendHighRiskAlert(conversationId, userId, drift);
    }
  }

  async sendHighRiskAlert(conversationId, userId, drift) {
    const key = `${conversationId}-high-risk`;
    if (this.isOnCooldown(key, 60 * 60 * 1000)) return;
    const message = this.formatHighRiskMessage(conversationId, userId, drift);
    // Slack
    if (this.slackClient && this.channel) {
      try {
        await this.slackClient.chat.postMessage({ channel: this.channel, text: message.text });
      } catch (err) {
        console.error('Failed to send Slack alert:', err.message);
      }
    }
    // Email
    if (this.emailTransport) {
      try {
        await this.emailTransport.sendMail({
          from: 'alignment-monitor@example.com',
          to: process.env.ALERT_EMAIL || 'alignment-team@example.com',
          subject: `🚨 High‑Risk Drift: ${conversationId}`,
          text: message.text
        });
      } catch (err) {
        console.error('Failed to send email alert:', err.message);
      }
    }
    this.setCooldown(key);
  }

  async checkFleetHealth(stats) {
    const percent = stats.highRisk / (stats.total || 1);
    if (percent >= this.thresholds.fleetHighRiskPercent) {
      const key = 'fleet-high-risk';
      if (this.isOnCooldown(key, 30 * 60 * 1000)) return;
      const text = `⚠️ Fleet Alert: ${(percent * 100).toFixed(1)}% of conversations (${stats.highRisk}/${stats.total}) show high risk drift.`;
      if (this.slackClient && this.channel) {
        await this.slackClient.chat.postMessage({ channel: this.channel, text });
      }
      if (this.emailTransport) {
        await this.emailTransport.sendMail({
          from: 'alignment-monitor@example.com',
          to: process.env.ALERT_EMAIL || 'alignment-team@example.com',
          subject: '⚠️ Fleet‑Wide Drift Alert',
          text
        });
      }
      this.setCooldown(key);
    }
  }

  formatHighRiskMessage(conversationId, userId, drift) {
    return {
      text: `🚨 High‑Risk drift detected in conversation ${conversationId} (user ${userId}). RiskScore=${drift.riskScore.toFixed(2)}, Dominant=${drift.dominantBasin}, Loopiness=${drift.loopiness.toFixed(2)}, Stability=${drift.stability.toFixed(2)}. Suggested actions: ${drift.recommendations.map(r => r.action).join('; ')}`
    };
  }
}

module.exports = AlertSystem;