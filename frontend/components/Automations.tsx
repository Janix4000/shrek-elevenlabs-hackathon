import React, { useState } from 'react';
import { Clock, Phone, Zap, Plus, Settings, TrendingUp, Bell, MessageSquare, Mail, Shield, Target, Globe, Brain } from 'lucide-react';
import AutomationFlowConfig, { AutomationConfig } from './AutomationFlowConfig';

interface Automation {
  id: string;
  name: string;
  description: string;
  keyMessage: string;
  icon: React.ReactNode;
  isActive: boolean;
  triggersCount: number;
  successRate: number;
  color: string;
}

const MOCK_AUTOMATIONS: Automation[] = [
  {
    id: 'auto-1',
    name: 'Subscription Cancellation',
    description: 'Auto-resolve disputes for customers claiming unauthorized renewal',
    keyMessage: 'Instant refunds for subscription disputes',
    icon: <Zap size={32} />,
    isActive: true,
    triggersCount: 2847,
    successRate: 84,
    color: 'blue',
  },
  {
    id: 'auto-2',
    name: 'Product Not Received',
    description: 'Handle missing shipments with carrier tracking verification',
    keyMessage: 'Fast resolution for delivery issues',
    icon: <Zap size={32} />,
    isActive: true,
    triggersCount: 1923,
    successRate: 93,
    color: 'red',
  },
  {
    id: 'auto-3',
    name: 'Taste Dissatisfaction',
    description: 'Offer flavor exchange or refund for first-time buyers',
    keyMessage: 'Turn flavor complaints into retention wins',
    icon: <Zap size={32} />,
    isActive: true,
    triggersCount: 4521,
    successRate: 76,
    color: 'purple',
  },
  {
    id: 'auto-4',
    name: 'High-Value Orders',
    description: 'Priority outreach for bulk orders over $200',
    keyMessage: 'VIP treatment for premium customers',
    icon: <Zap size={32} />,
    isActive: true,
    triggersCount: 3102,
    successRate: 88,
    color: 'orange',
  },
];

const Automations: React.FC = () => {
  const [configureAutomation, setConfigureAutomation] = useState<Automation | null>(null);

  const getColorClasses = (color: string) => {
    const colors = {
      blue: { bg: 'bg-blue-50', icon: 'text-blue-600' },
      red: { bg: 'bg-red-50', icon: 'text-red-600' },
      purple: { bg: 'bg-purple-50', icon: 'text-purple-600' },
      orange: { bg: 'bg-orange-50', icon: 'text-orange-600' },
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="animate-fade-in space-y-6 pb-12">

      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Intelligent Automation</h1>
          <p className="text-slate-500 text-sm mt-1">AI-powered workflows that work 24/7 to win disputes and prevent chargebacks</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 shadow-sm">
          <Plus size={16} /> Create New Automation
        </button>
      </div>

      {/* Automation List */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Automation</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Triggers</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Success Rate</th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {MOCK_AUTOMATIONS.map((automation) => {
              const colors = getColorClasses(automation.color);
              return (
                <tr
                  key={automation.id}
                  onClick={() => setConfigureAutomation(automation)}
                  className="hover:bg-slate-50 cursor-pointer transition-colors group"
                >
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-4">
                      <div className={`${colors.bg} w-12 h-12 rounded-xl flex items-center justify-center ${colors.icon}`}>
                        {automation.icon}
                      </div>
                      <div className="flex-1">
                        <div className="text-lg font-bold text-slate-900 mb-1">{automation.keyMessage}</div>
                        <div className="text-sm text-slate-600">{automation.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-2 text-emerald-600">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                      <span className="text-sm font-semibold">Active</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <span className="text-lg font-bold text-slate-900">{automation.triggersCount.toLocaleString()}</span>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-3">
                      <div className="w-24 h-2.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          style={{ width: `${automation.successRate}%` }}
                          className="h-full bg-blue-600"
                        ></div>
                      </div>
                      <span className="text-lg font-bold text-slate-900 w-12">{automation.successRate}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setConfigureAutomation(automation);
                      }}
                      className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Settings size={14} />
                      Configure
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Automation Configuration Modal */}
      {configureAutomation && (
        <AutomationFlowConfig
          automationName={configureAutomation.name}
          onClose={() => setConfigureAutomation(null)}
          onSave={(config: AutomationConfig) => {
            console.log('Saved automation configuration:', config);
            setConfigureAutomation(null);
          }}
        />
      )}
    </div>
  );
};

export default Automations;
