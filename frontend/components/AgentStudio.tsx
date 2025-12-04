import React, { useState } from 'react';
import { Bot, Plus, Settings, Phone, TrendingUp, Clock, Sparkles } from 'lucide-react';
import AgentFlowConfig, { ElevenLabsAgentConfig } from './AgentFlowConfig';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Badge } from './ui/badge';

interface Agent {
  id: string;
  name: string;
  title: string;
  description: string;
  voiceId: string;
  isActive: boolean;
  callsHandled: number;
  successRate: number;
  avgCallDuration: string;
  lastUsed: string;
  color: string;
  gradient: string;
}

const MOCK_AGENTS: Agent[] = [
  {
    id: 'agent-1',
    name: 'Subscription Support',
    title: 'Subscription & Recurring Issues',
    description: 'Handles cancellation requests and recurring billing disputes',
    voiceId: 'eleven_flash_v2_5_sarah',
    isActive: true,
    callsHandled: 8347,
    successRate: 84,
    avgCallDuration: '6m 42s',
    lastUsed: '12 minutes ago',
    color: 'blue',
    gradient: 'from-blue-500 to-indigo-600',
  },
  {
    id: 'agent-2',
    name: 'Fraud Detection',
    title: 'Fraudulent Claim Handler',
    description: 'Identifies and handles suspicious chargebacks and fraud patterns',
    voiceId: 'eleven_flash_v2_5_marcus',
    isActive: true,
    callsHandled: 6923,
    successRate: 91,
    avgCallDuration: '4m 18s',
    lastUsed: '8 minutes ago',
    color: 'purple',
    gradient: 'from-purple-500 to-pink-600',
  },
  {
    id: 'agent-3',
    name: 'Delivery Issues',
    title: 'Shipping & Delivery Disputes',
    description: 'Resolves non-delivery and package theft claims quickly',
    voiceId: 'eleven_flash_v2_5_alex',
    isActive: true,
    callsHandled: 12521,
    successRate: 79,
    avgCallDuration: '3m 08s',
    lastUsed: '3 minutes ago',
    color: 'emerald',
    gradient: 'from-emerald-500 to-teal-600',
  },
  {
    id: 'agent-4',
    name: 'Product Quality',
    title: 'Quality & Defect Claims',
    description: 'Handles product defect, taste, and quality-related disputes',
    voiceId: 'eleven_flash_v2_5_jordan',
    isActive: true,
    callsHandled: 4647,
    successRate: 93,
    avgCallDuration: '7m 24s',
    lastUsed: '18 minutes ago',
    color: 'orange',
    gradient: 'from-orange-500 to-red-600',
  },
];

const AgentStudio: React.FC = () => {
  const [configureAgent, setConfigureAgent] = useState<Agent | null>(null);

  const getColorClasses = (color: string) => {
    const colors = {
      blue: { bg: 'bg-blue-50', icon: 'text-blue-600' },
      purple: { bg: 'bg-purple-50', icon: 'text-purple-600' },
      emerald: { bg: 'bg-emerald-50', icon: 'text-emerald-600' },
      orange: { bg: 'bg-orange-50', icon: 'text-orange-600' },
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="animate-fade-in space-y-6 pb-12">

      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Voice Agent Library</h1>
          <p className="text-muted-foreground text-sm mt-1">ElevenLabs-powered voice agents for real-time dispute resolution</p>
        </div>
        <Button className="flex items-center gap-2">
          <Plus size={16} /> Create New Agent
        </Button>
      </div>

      {/* Agent List */}
      <Card>
        <table className="w-full text-left border-collapse">
          <thead className="bg-muted border-b border-border">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider">Agent</th>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider">Calls</th>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider">Win Rate</th>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider">Avg Duration</th>
              <th className="px-6 py-4 text-xs font-bold text-muted-foreground uppercase tracking-wider"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {MOCK_AGENTS.map((agent) => {
              const colors = getColorClasses(agent.color);
              return (
                <tr
                  key={agent.id}
                  onClick={() => setConfigureAgent(agent)}
                  className="hover:bg-muted/50 cursor-pointer transition-colors group"
                >
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-4">
                      <div className={`${colors.bg} w-12 h-12 rounded-xl flex items-center justify-center ${colors.icon}`}>
                        <Bot size={24} />
                      </div>
                      <div className="flex-1">
                        <div className="text-lg font-bold text-foreground mb-1">{agent.name}</div>
                        <div className="text-sm text-muted-foreground">{agent.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <Badge variant="default" className="gap-2">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                      <span>Live</span>
                    </Badge>
                  </td>
                  <td className="px-6 py-5">
                    <span className="text-lg font-bold text-foreground">{agent.callsHandled.toLocaleString()}</span>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-3">
                      <div className="w-24 h-2.5 bg-muted rounded-full overflow-hidden">
                        <div
                          style={{ width: `${agent.successRate}%` }}
                          className="h-full bg-blue-600"
                        ></div>
                      </div>
                      <span className="text-lg font-bold text-foreground w-12">{agent.successRate}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    <span className="text-lg font-bold text-foreground">{agent.avgCallDuration}</span>
                  </td>
                  <td className="px-6 py-5">
                    <Button
                      onClick={(e) => {
                        e.stopPropagation();
                        setConfigureAgent(agent);
                      }}
                      size="sm"
                      className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Settings size={14} />
                      Configure
                    </Button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Card>

      {/* Agent Configuration Modal */}
      {configureAgent && (
        <AgentFlowConfig
          agentName={configureAgent.name}
          onClose={() => setConfigureAgent(null)}
          onSave={(config: ElevenLabsAgentConfig) => {
            console.log('Saved configuration:', config);
            setConfigureAgent(null);
          }}
        />
      )}
    </div>
  );
};

export default AgentStudio;
