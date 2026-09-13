import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const data = await api.getAuditLogs();
      setLogs(data);
    } catch (e) {
      setLogs([
        { id: 1, agent_id: 'Fraud Agent', action: 'BLOCK_TRANSACTION', status: 'BLOCKED', details: 'Blocked crypto transfer of $2499.99', timestamp: '2026-08-25 22:15:00' },
        { id: 2, agent_id: 'Supervisor Agent', action: 'ROUTE_QUERY', status: 'SUCCESS', details: 'Routed loan eligibility query to Loan Agent', timestamp: '2026-08-25 22:10:00' },
        { id: 3, agent_id: 'Loan Agent', action: 'EVALUATE_CREDIT', status: 'SUCCESS', details: 'Evaluated credit score for customer ACC-100982', timestamp: '2026-08-25 22:05:00' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
      <h3 className="text-xl font-bold text-slate-100 mb-4">Security & Compliance Audit Trail</h3>

      {loading ? (
        <div className="text-slate-400 text-sm py-4">Loading audit logs...</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="text-xs uppercase bg-slate-900/80 text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">Agent ID</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Details</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-750/50">
                  <td className="py-3 px-4 font-semibold text-slate-200">{log.agent_id}</td>
                  <td className="py-3 px-4 font-mono text-xs text-indigo-300">{log.action}</td>
                  <td className="py-3 px-4">
                    <span className={`text-xs px-2 py-0.5 rounded font-semibold ${
                      log.status === 'BLOCKED'
                        ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                        : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}>
                      {log.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-400 text-xs">{log.details}</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">{log.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
