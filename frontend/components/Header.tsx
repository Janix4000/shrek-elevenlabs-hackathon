import React from 'react';
import { ViewState } from '../types';

interface HeaderProps {
  currentView: ViewState;
  onChangeView: (view: ViewState) => void;
}

const Header: React.FC<HeaderProps> = ({ currentView, onChangeView }) => {
  const navItems: { id: ViewState; label: string }[] = [
    { id: 'overview', label: 'Dashboard' },
    { id: 'disputes', label: 'Disputes' },
    { id: 'agent-studio', label: 'Agent Studio' },
    { id: 'automations', label: 'Automations' },
    { id: 'integrations', label: 'Integrations' },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-[2000px] mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo & Nav */}
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center">
               <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                 <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
               </svg>
            </div>
            <span className="font-bold text-slate-900 text-lg tracking-tight">ChargeGuard</span>
            <span className="text-slate-300 text-sm">|</span>
            <svg width="60" height="32" viewBox="0 0 60 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <text x="0" y="24" fontFamily="Arial, sans-serif" fontSize="24" fontWeight="bold" fill="#000000">Huel</text>
            </svg>
          </div>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onChangeView(item.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  currentView === item.id
                    ? 'text-slate-900 bg-slate-100'
                    : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <button className="w-8 h-8 bg-slate-900 rounded-full flex items-center justify-center hover:bg-slate-800 transition-colors">
            <span className="text-white font-bold text-sm">H</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;