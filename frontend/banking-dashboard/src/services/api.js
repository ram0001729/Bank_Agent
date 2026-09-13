const BASE_URL = 'http://127.0.0.1:8000';

async function fetchJson(endpoint, options = {}) {
  try {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn(`API request failed for ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  getCustomers: () => fetchJson('/api/customers'),
  getTransactions: () => fetchJson('/api/transactions'),
  analyzeFraud: (data) =>
    fetchJson('/api/transactions/analyze-fraud', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  getAgentsStatus: () => fetchJson('/api/agents/status'),
  registerAgent: (agent_name, role, daily_budget_limit = 10000.0) =>
    fetchJson('/api/agents/register', {
      method: 'POST',
      body: JSON.stringify({ agent_name, role, daily_budget_limit }),
    }),
  processAgentPayment: (agent_name, amount, recipient, description) =>
    fetchJson('/api/agents/payment-request', {
      method: 'POST',
      body: JSON.stringify({ agent_name, amount, recipient, description }),
    }),
  chatWithAgent: (agent, message, amount = 0.0) =>
    fetchJson('/api/agents/chat', {
      method: 'POST',
      body: JSON.stringify({ agent, message, amount }),
    }),
  getAuditLogs: () => fetchJson('/api/agents/audit-logs'),
  getEmergencyStopStatus: () => fetchJson('/api/agents/emergency-stop/status'),
  triggerEmergencyStop: () =>
    fetchJson('/api/agents/emergency-stop/trigger', { method: 'POST' }),
  resetEmergencyStop: () =>
    fetchJson('/api/agents/emergency-stop/reset', { method: 'POST' }),
};
