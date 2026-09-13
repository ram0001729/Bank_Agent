import React, { useState, useEffect } from 'react';
import { CustomerPortal } from './pages/CustomerPortal';
import { EmployeePortal } from './pages/EmployeePortal';
import { AdminPanel } from './pages/AdminPanel';
import { api } from './services/api';

export default function App() {
  const [activePortal, setActivePortal] = useState('customer');
  const [isStopped, setIsStopped] = useState(false);
  const [loadingStop, setLoadingStop] = useState(false);

  useEffect(() => {
    checkStopStatus();
  }, []);

  const checkStopStatus = async () => {
    try {
      const res = await api.getEmergencyStopStatus();
      setIsStopped(res.is_stopped);
    } catch (e) {
      console.warn('Could not check emergency stop status');
    }
  };

  const handleToggleEmergencyStop = async () => {
    setLoadingStop(true);
    try {
      if (isStopped) {
        const res = await api.resetEmergencyStop();
        setIsStopped(false);
      } else {
        const res = await api.triggerEmergencyStop();
        setIsStopped(true);
      }
    } catch (e) {
      alert('Failed to toggle Emergency Stop');
    } finally {
      setLoadingStop(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Emergency Stop Alert Banner if Stopped */}
      {isStopped && (
        <div className="bg-rose-600 text-white px-6 py-2.5 text-center font-bold text-sm flex items-center justify-center gap-3 animate-pulse border-b border-rose-700">
          <span>🛑 CIRCUIT BREAKER TRIGGERED: ALL AGENT EXECUTIONS ARE CURRENTLY SUSPENDED BY EMERGENCY STOP!</span>
          <button
            onClick={handleToggleEmergencyStop}
            className="bg-white text-rose-700 px-3 py-1 rounded text-xs uppercase font-extrabold hover:bg-slate-100 transition shadow"
          >
            Reset Emergency Stop
          </button>
        </div>
      )}

      {/* Top Header Navigation */}
      <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-600 p-2 rounded-lg font-black text-xl text-white">AG</div>
            <div>
              <h1 className="font-bold text-slate-100 text-lg leading-tight">AI Banking Agent Platform</h1>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* RED EMERGENCY STOP BUTTON */}
            <button
              onClick={handleToggleEmergencyStop}
              disabled={loadingStop}
              className={`emergency-stop-button flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition shadow-lg border ${
                isStopped
                  ? 'bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-500 animate-bounce'
                  : 'bg-rose-300 hover:bg-rose-400 text-rose-950 border-rose-400 hover:shadow-rose-400/20'
              }`}
            >
              <span className="h-2.5 w-2.5 rounded-full bg-white animate-ping"></span>
              {isStopped ? 'Reset Emergency Stop' : '🛑 EMERGENCY STOP'}
            </button>

            {/* Portal Switcher Buttons */}
            <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-sm font-semibold">
              <button
                onClick={() => setActivePortal('customer')}
                className={`px-4 py-1.5 rounded-lg transition ${
                  activePortal === 'customer'
                    ? 'bg-indigo-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Agent Payment Gateway
              </button>

              <button
                onClick={() => setActivePortal('employee')}
                className={`px-4 py-1.5 rounded-lg transition ${
                  activePortal === 'employee'
                    ? 'bg-indigo-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Risk Analysis & XGBoost
              </button>

              <button
                onClick={() => setActivePortal('admin')}
                className={`px-4 py-1.5 rounded-lg transition ${
                  activePortal === 'admin'
                    ? 'bg-indigo-600 text-white shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Governance OS Admin
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activePortal === 'customer' && <CustomerPortal />}
        {activePortal === 'employee' && <EmployeePortal />}
        {activePortal === 'admin' && <AdminPanel />}
      </main>

      {/* Footer Status Bar */}
      <footer className="border-t border-slate-800 bg-slate-900/60 py-4 text-center text-xs text-slate-500">
        <p>AI-Banking-Agent-Platform v1.0 • Connected to FastAPI Gateway (127.0.0.1:8000) • Governance OS Active</p>
      </footer>
    </div>
  );
}
