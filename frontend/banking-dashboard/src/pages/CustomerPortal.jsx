import React, { useState } from 'react';
import { TransactionView } from '../components/TransactionView';
import { api } from '../services/api';

export const CustomerPortal = () => {
  // Agent Registration State
  const [regName, setRegName] = useState('Payment Agent Alpha');
  const [regRole, setRegRole] = useState('supervisor');
  const [regBudget, setRegBudget] = useState('10000');
  const [regMsg, setRegMsg] = useState(null);

  // Agent Payment Request State
  const [agentName, setAgentName] = useState('Supervisor Agent');
  const [amount, setAmount] = useState('450.00');
  const [recipient, setRecipient] = useState('Vendor Tech Supplies');
  const [description, setDescription] = useState('Monthly server hosting fee payment');
  const [payResult, setPayResult] = useState(null);
  const [loadingPay, setLoadingPay] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await api.registerAgent(regName, regRole, parseFloat(regBudget) || 0);
      setRegMsg(res);
    } catch (e) {
      setRegMsg({ status: 'ERROR', message: 'Agent registration failed' });
    }
  };

  const handlePaymentRequest = async (e) => {
    e.preventDefault();
    setLoadingPay(true);
    try {
      const res = await api.processAgentPayment(agentName, parseFloat(amount) || 0.0, recipient, description);
      setPayResult(res);
    } catch (err) {
      setPayResult({
        payment_status: 'DENIED',
        risk_score: 0.99,
        is_fraud: true,
        agent_name: agentName,
        governance_explanation: 'Payment request rejected by platform gateway'
      });
    } finally {
      setLoadingPay(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top B2B Agent Platform Header Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl shadow-lg">
          <span className="text-slate-400 text-sm font-medium">Platform Mode</span>
          <h2 className="text-2xl font-bold text-indigo-400 mt-2">B2B Agent Gateway</h2>
          <p className="text-xs text-slate-400 mt-2">AI Agent Registration & Payment Authorization</p>
        </div>

        <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl shadow-lg">
          <span className="text-slate-400 text-sm font-medium">Risk Analysis Engine</span>
          <h2 className="text-2xl font-bold text-slate-100 mt-2">XGBoost + RAG</h2>
          <p className="text-xs text-emerald-400 mt-2 font-semibold">● 2-Stage MCP Verification Active</p>
        </div>

        <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl shadow-lg">
          <span className="text-slate-400 text-sm font-medium">Governance Policy</span>
          <h2 className="text-2xl font-bold text-emerald-400 mt-2">OPA Rego Rules</h2>
          <p className="text-xs text-slate-400 mt-2">Zero-Trust Spending & Permission Caps</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Register External AI Agent Form */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-slate-100 mb-2">1. Register External AI Agent</h3>
          <p className="text-sm text-slate-400 mb-4">Register a new AI Agent on our Governance Platform to issue cryptographic API credentials.</p>

          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Agent Name / ID</label>
              <input
                type="text"
                value={regName}
                onChange={(e) => setRegName(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Agent Role (RBAC/ABAC)</label>
              <select
                value={regRole}
                onChange={(e) => setRegRole(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                <option value="supervisor">Supervisor (Full Access)</option>
                <option value="fraud_evaluator">Fraud Evaluator</option>
                <option value="loan_underwriter">Loan Underwriter</option>
                <option value="refund_processor">Refund Processor</option>
                <option value="support_assistant">Support Assistant</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Daily Budget Limit</label>
              <input
                type="number"
                min="0.01"
                max="1000000"
                step="0.01"
                value={regBudget}
                onChange={(e) => setRegBudget(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 rounded-lg text-sm transition"
            >
              Register AI Agent
            </button>
          </form>

          {regMsg && (
            <div className="mt-4 p-3 rounded bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-xs">
              <strong>{regMsg.message}</strong> (ID: {regMsg.agent_id})
              {regMsg.api_key && (
                <div className="mt-2 break-all">
                  <strong>API key (store securely):</strong> {regMsg.api_key}
                </div>
              )}
            </div>
          )}
        </div>

        {/* 2. Submit Agent Payment Request Form */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-slate-100 mb-2">2. Submit Agent Payment Request</h3>
          <p className="text-sm text-slate-400 mb-4">AI Agents request payment authorization. Request undergoes ML risk analysis & OPA Rego policy verification.</p>

          <form onSubmit={handlePaymentRequest} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Requesting Agent</label>
                <input
                  type="text"
                  value={agentName}
                  onChange={(e) => setAgentName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Payment Amount ($)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Payment Recipient</label>
              <input
                type="text"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Payment Description / Purpose</label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <button
              type="submit"
              disabled={loadingPay}
              className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2 rounded-lg text-sm transition disabled:opacity-50"
            >
              {loadingPay ? 'Analyzing ML Risk & Governance Rules...' : 'Submit Payment Request'}
            </button>
          </form>
        </div>
      </div>

      {/* Payment Decision Output */}
      {payResult && (
        <div className={`p-6 rounded-xl border shadow-lg ${
          payResult.payment_status === 'APPROVED'
            ? 'bg-emerald-950/40 border-emerald-600 text-emerald-200'
            : 'bg-rose-950/40 border-rose-600 text-rose-200'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="font-bold text-lg">Agent Payment Authorization Result:</span>
            <span className={`px-3 py-1 rounded-full text-xs font-black uppercase ${
              payResult.payment_status === 'APPROVED' ? 'bg-emerald-500 text-slate-950' : 'bg-rose-500 text-white'
            }`}>
              {payResult.payment_status}
            </span>
          </div>

          <p className="text-sm mb-3"><strong>Governance Explanation:</strong> {payResult.governance_explanation}</p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-slate-900/80 p-3 rounded-lg text-slate-300">
            <div><span>Requesting Agent:</span> <strong className="block text-slate-100">{payResult.agent_name}</strong></div>
            <div><span>XGBoost Fraud Risk:</span> <strong className="block text-slate-100">{(payResult.risk_score * 100).toFixed(1)}%</strong></div>
            <div><span>Is Fraud Flagged:</span> <strong className="block text-slate-100">{payResult.is_fraud ? 'YES' : 'NO'}</strong></div>
            <div><span>MCP Transaction ID:</span> <strong className="block text-slate-100">{payResult.mcp_transaction_id || 'N/A'}</strong></div>
          </div>
        </div>
      )}

      {/* Executed Agent Payments History */}
      <TransactionView />
    </div>
  );
};
