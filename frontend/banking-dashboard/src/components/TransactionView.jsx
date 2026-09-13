import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export const TransactionView = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      const data = await api.getTransactions();
      setTransactions(data);
    } catch (e) {
      setTransactions([
        { id: 101, customer_id: 1, amount: 120.00, merchant: 'Amazon.com', category: 'Shopping', status: 'completed', is_fraud: false, risk_score: 0.02 },
        { id: 102, customer_id: 1, amount: 45.50, merchant: 'Starbucks', category: 'Dining', status: 'completed', is_fraud: false, risk_score: 0.01 },
        { id: 103, customer_id: 2, amount: 2499.99, merchant: 'Unknown Crypto Exch', category: 'Transfer', status: 'blocked', is_fraud: true, risk_score: 0.92 },
        { id: 104, customer_id: 3, amount: 850.00, merchant: 'Luxury Hotel', category: 'Travel', status: 'completed', is_fraud: false, risk_score: 0.15 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-slate-100">Recent Transactions</h3>
        <button
          onClick={loadTransactions}
          className="text-xs bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-lg text-slate-300 transition"
        >
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="text-slate-400 text-sm py-4">Loading transactions...</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="text-xs uppercase bg-slate-900/80 text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">TX ID</th>
                <th className="py-3 px-4">Merchant</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Amount</th>
                <th className="py-3 px-4">Risk Score</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-slate-750/50">
                  <td className="py-3 px-4 font-mono text-xs text-slate-400">#{tx.id}</td>
                  <td className="py-3 px-4 font-semibold text-slate-200">{tx.merchant}</td>
                  <td className="py-3 px-4 text-xs text-slate-400">{tx.category}</td>
                  <td className="py-3 px-4 font-mono text-slate-200">${tx.amount.toFixed(2)}</td>
                  <td className="py-3 px-4">
                    <span className={`font-mono text-xs font-bold ${
                      tx.risk_score > 0.7 ? 'text-rose-400' : tx.risk_score > 0.3 ? 'text-amber-400' : 'text-emerald-400'
                    }`}>
                      {(tx.risk_score * 100).toFixed(0)}%
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`text-xs px-2.5 py-0.5 rounded font-semibold uppercase ${
                      tx.is_fraud || tx.status === 'blocked'
                        ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                        : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}>
                      {tx.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
