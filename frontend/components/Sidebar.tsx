import React from 'react';
import { LayoutDashboard, ShieldAlert, BarChart3, Bot, Settings, LogOut } from 'lucide-react';
import { ViewState } from '../types';

interface SidebarProps {
  currentView: ViewState;
  onChangeView: (view: ViewState) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentView, onChangeView }) => {
  const menuItems: { id: ViewState; label: string; icon: React.ReactNode }[] = [
    { id: 'overview', label: 'Overview', icon: <LayoutDashboard size={20} /> },
    { id: 'disputes', label: 'Disputes', icon: <ShieldAlert size={20} /> },
    { id: 'evaluations', label: 'Evaluations', icon: <BarChart3 size={20} /> },
    { id: 'agent-studio', label: 'Agent Studio', icon: <Bot size={20} /> },
  ];

  return (
    <div className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen border-r border-slate-800 sticky top-0">
      <div className="p-6 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-8 h-8 bg-brand-500 rounded-lg flex items-center justify-center">
            <ShieldAlert className="text-white" size={20} />
        </div>
        <span className="text-white font-bold text-lg tracking-tight">ChargeGuard</span>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onChangeView(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
              currentView === item.id
                ? 'bg-brand-900/50 text-brand-500 border border-brand-900'
                : 'hover:bg-slate-800 hover:text-white'
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-slate-400 hover:text-white transition-colors">
          <Settings size={18} />
          <span>Settings</span>
        </button>
        <button className="w-full flex items-center space-x-3 px-4 py-2 text-sm text-slate-400 hover:text-white transition-colors mt-1">
          <LogOut size={18} />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;