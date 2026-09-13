import React from 'react';
import { RiskDashboard } from '../components/RiskDashboard';
import { TransactionView } from '../components/TransactionView';

export const EmployeePortal = () => {
  return (
    <div className="space-y-6">
      <div className="bg-slate-800 border border-slate-700 p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Bank Operations & Risk Officer Portal</h2>
          <p className="text-sm text-slate-400">Review flagged suspicious activities, model predictions, and customer risk levels.</p>
        </div>
        <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold px-4 py-1.5 rounded-lg text-sm">
          Risk Officer Mode
        </span>
      </div>

      <RiskDashboard />
      <TransactionView />
    </div>
  );
};
