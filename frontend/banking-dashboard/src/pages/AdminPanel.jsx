import React, { useState, useEffect } from 'react';
import { AgentMonitor } from '../components/AgentMonitor';
import { AuditLogs } from '../components/AuditLogs';
import { api } from '../services/api';

export const AdminPanel = () => {
  const [isStopped, setIsStopped] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const res = await api.getEmergencyStopStatus();
      setIsStopped(res.is_stopped);
    } catch (e) {}
  };

  const handleToggle = async () => {
    setLoading(true);
    try {
      if (isStopped) {
        await api.resetEmergencyStop();
        setIsStopped(false);
      } else {
        await api.triggerEmergencyStop();
        setIsStopped(true);
      }
    } catch (e) {
      alert('Error updating Emergency Stop status');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">System Administration & Governance Panel</h2>
          <p className="text-sm text-slate-400">Monitor multi-agent execution telemetry, security policies, and compliance logs.</p>
        </div>
        <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold px-4 py-1.5 rounded-lg text-sm">
          System Admin
        </span>
      </div>

      {/* Emergency Control Circuit Breaker Box */}
      <div className={`p-6 rounded-xl border shadow-lg flex items-center justify-between ${
        isStopped ? 'bg-rose-950/40 border-rose-600' : 'bg-slate-800 border-slate-700'
      }`}>
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className={`h-3 w-3 rounded-full ${isStopped ? 'bg-rose-500 animate-ping' : 'bg-emerald-500'}`}></span>
            <h3 className="text-lg font-bold text-slate-100">Governance OS Circuit Breaker (Emergency Stop)</h3>
          </div>
          <p className="text-xs text-slate-400">
            {isStopped
              ? 'ALL AGENT WORKFLOWS SUSPENDED. Requests return EMERGENCY_STOP_ACTIVE until reset.'
              : 'All agents operational. Pressing Emergency Stop will instantly freeze all multi-agent tool executions.'}
          </p>
        </div>

        <button
          onClick={handleToggle}
          disabled={loading}
          className={`px-5 py-2.5 rounded-xl font-black text-xs uppercase tracking-wider transition border shadow-lg ${
            isStopped
              ? 'bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-500'
              : 'bg-rose-600 hover:bg-rose-500 text-white border-rose-500'
          }`}
        >
          {isStopped ? 'Restore Agent Operations' : '🛑 TRIGGER EMERGENCY STOP'}
        </button>
      </div>

      <AgentMonitor />
      <AuditLogs />
    </div>
  );
};
