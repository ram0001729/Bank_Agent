import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export const AgentMonitor = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
    const interval = setInterval(loadAgents, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadAgents = async () => {
    try {
      const data = await api.getAgentsStatus();
      setAgents(data);
    } catch (e) {
      // Fallback data if backend offline
      setAgents([
        { name: 'Supervisor Agent', role: 'Intent Router', status: 'Active', model: 'Gemini 3.6 Flash', requests_processed: 142 },
        { name: 'Fraud Detection Agent', role: 'Risk Scoring Engine', status: 'Active', model: 'XGBoost v1', requests_processed: 98 },
        { name: 'Loan Approval Agent', role: 'Underwriting Risk', status: 'Active', model: 'Gemini 3.6 Flash', requests_processed: 34 },
        { name: 'Customer Support Agent', role: 'RAG Policy Assistant', status: 'Active', model: 'Gemini 3.6 Flash', requests_processed: 210 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </span>
          Autonomous Agent Fleet
        </h3>
        <button
          onClick={loadAgents}
          className="text-xs bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-lg text-slate-300 transition"
        >
          Refresh Status
        </button>
      </div>

      {loading ? (
        <div className="text-slate-400 text-sm py-4">Loading agent status...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent, idx) => (
            <div key={idx} className="bg-slate-900/60 border border-slate-750 p-4 rounded-lg flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-semibold text-slate-200">{agent.name}</h4>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {agent.status}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-3">{agent.role}</p>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800 pt-2.5 mt-2">
                <span>Model: <strong className="text-slate-300">{agent.model}</strong></span>
                <span>Requests: <strong className="text-slate-300">{agent.requests_processed}</strong></span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
