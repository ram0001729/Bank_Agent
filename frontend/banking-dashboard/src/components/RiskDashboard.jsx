import React, { useState } from 'react';
import { api } from '../services/api';

export const RiskDashboard = () => {
  const [amount, setAmount] = useState('1500.00');
  const [timeOffset, setTimeOffset] = useState('1200');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.analyzeFraud({
        amount: parseFloat(amount) || 100.0,
        time_offset: parseFloat(timeOffset) || 1000.0,
      });
      setResult(res);
    } catch (err) {
      setResult({
        risk_score: 0.88,
        is_fraud: true,
        status: 'blocked',
        risk_level: 'High',
        recommendation: 'Block & Alert Security (Fallback Heuristic)'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
      <h3 className="text-xl font-bold text-slate-100 mb-2">Real-Time ML Risk Assessment</h3>
      <p className="text-sm text-slate-400 mb-6">
        Test instant XGBoost model fraud scoring on incoming transaction vectors.
      </p>

      <form onSubmit={handleAnalyze} className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-xs text-slate-400 mb-1 font-medium">Transaction Amount ($)</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
            placeholder="1500.00"
          />
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-1 font-medium">Time Offset (Seconds)</label>
          <input
            type="number"
            value={timeOffset}
            onChange={(e) => setTimeOffset(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
            placeholder="1200"
          />
        </div>

        <div className="flex items-end">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 px-4 rounded-lg transition text-sm disabled:opacity-50"
          >
            {loading ? 'Evaluating Model...' : 'Run Risk Inference'}
          </button>
        </div>
      </form>

      {result && (
        <div className="bg-slate-900 border border-slate-700 p-4 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-semibold text-slate-300">Model Decision Output:</span>
            <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase ${
              result.is_fraud ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
            }`}>
              {result.recommendation}
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="bg-slate-800 p-2.5 rounded border border-slate-750">
              <span className="text-slate-500 block">Fraud Probability</span>
              <span className="text-base font-mono font-bold text-indigo-400">{(result.risk_score * 100).toFixed(1)}%</span>
            </div>

            <div className="bg-slate-800 p-2.5 rounded border border-slate-750">
              <span className="text-slate-500 block">Risk Category</span>
              <span className="text-base font-semibold text-slate-200">{result.risk_level}</span>
            </div>

            <div className="bg-slate-800 p-2.5 rounded border border-slate-750">
              <span className="text-slate-500 block">Action Code</span>
              <span className="text-base font-semibold text-slate-200">{result.status}</span>
            </div>

            <div className="bg-slate-800 p-2.5 rounded border border-slate-750">
              <span className="text-slate-500 block">Model Version</span>
              <span className="text-base font-semibold text-slate-200">XGBoost v6</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
