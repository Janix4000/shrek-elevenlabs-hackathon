import React, { useState, useCallback } from 'react';
import { createPortal } from 'react-dom';
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { X, Save, Play, Plus, Settings, Phone, MessageSquare, Zap, FileText } from 'lucide-react';

interface AgentFlowConfigProps {
  agentName: string;
  onClose: () => void;
  onSave: (config: ElevenLabsAgentConfig) => void;
}

// ElevenLabs Agent Configuration based on their SDK
export interface ElevenLabsAgentConfig {
  // Agent Identity
  name: string;

  // Voice Configuration
  voice_id: string;
  voice_settings?: {
    stability: number; // 0.0 to 1.0
    similarity_boost: number; // 0.0 to 1.0
    style?: number; // 0.0 to 1.0
    use_speaker_boost?: boolean;
  };

  // Language & Model
  language?: string; // e.g., "en", "es", "fr"
  model_id?: string; // e.g., "eleven_turbo_v2", "eleven_multilingual_v2"

  // Conversation Settings
  first_message?: string;
  prompt?: {
    system_prompt: string;
    temperature?: number; // 0.0 to 1.0
    max_tokens?: number;
  };

  // Tools & Functions
  tools?: Array<{
    type: string; // "function" | "webhook"
    name: string;
    description: string;
    parameters?: any;
    webhook_url?: string;
  }>;

  // Conversation Flow
  max_duration_seconds?: number;
  interruption_threshold?: number; // 0.0 to 1.0
  keywords?: string[];

  // Privacy & Compliance
  opt_out_message?: string;
  opt_out_phrase?: string;

  // Webhook Events
  webhook_events?: {
    on_call_start?: string;
    on_call_end?: string;
    on_transfer?: string;
  };
}

const initialNodes: Node[] = [
  {
    id: 'start',
    type: 'input',
    data: { label: 'Call Start' },
    position: { x: 250, y: 25 },
    style: { background: '#10b981', color: 'white', border: '2px solid #059669' },
  },
  {
    id: 'greeting',
    data: { label: 'Greeting & Identification' },
    position: { x: 200, y: 125 },
    style: { background: '#3b82f6', color: 'white', border: '2px solid #2563eb' },
  },
  {
    id: 'intent',
    data: { label: 'Intent Detection' },
    position: { x: 200, y: 225 },
    style: { background: '#6366f1', color: 'white', border: '2px solid #4f46e5' },
  },
  {
    id: 'dispute-flow',
    data: { label: 'Dispute Resolution Flow' },
    position: { x: 100, y: 325 },
    style: { background: '#8b5cf6', color: 'white', border: '2px solid #7c3aed' },
  },
  {
    id: 'info-gathering',
    data: { label: 'Information Gathering' },
    position: { x: 300, y: 325 },
    style: { background: '#a855f7', color: 'white', border: '2px solid #9333ea' },
  },
  {
    id: 'resolution',
    data: { label: 'Resolution & Next Steps' },
    position: { x: 200, y: 425 },
    style: { background: '#ec4899', color: 'white', border: '2px solid #db2777' },
  },
  {
    id: 'end',
    type: 'output',
    data: { label: 'Call End' },
    position: { x: 250, y: 525 },
    style: { background: '#ef4444', color: 'white', border: '2px solid #dc2626' },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: 'start', target: 'greeting', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2-3', source: 'greeting', target: 'intent', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3-4', source: 'intent', target: 'dispute-flow', label: 'Dispute', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3-5', source: 'intent', target: 'info-gathering', label: 'Info', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4-6', source: 'dispute-flow', target: 'resolution', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5-6', source: 'info-gathering', target: 'resolution', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e6-7', source: 'resolution', target: 'end', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
];

const AgentFlowConfig: React.FC<AgentFlowConfigProps> = ({ agentName, onClose, onSave }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // ElevenLabs Configuration State
  const [config, setConfig] = useState<ElevenLabsAgentConfig>({
    name: agentName,
    voice_id: 'eleven_flash_v2_5',
    voice_settings: {
      stability: 0.5,
      similarity_boost: 0.75,
      style: 0.0,
      use_speaker_boost: true,
    },
    language: 'en',
    model_id: 'eleven_turbo_v2',
    first_message: 'Hi, this is ChargeGuard calling about your recent dispute. Is now a good time to talk?',
    prompt: {
      system_prompt: 'You are a professional dispute resolution agent. Be empathetic, clear, and solution-oriented.',
      temperature: 0.7,
      max_tokens: 500,
    },
    max_duration_seconds: 600,
    interruption_threshold: 0.5,
    keywords: ['refund', 'fraud', 'cancel', 'dispute', 'chargeback'],
    opt_out_phrase: 'stop calling',
    tools: [],
    webhook_events: {
      on_call_start: '',
      on_call_end: '',
      on_transfer: '',
    },
  });

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleSave = () => {
    onSave(config);
    onClose();
  };

  const modalContent = (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-xl w-full max-w-7xl h-[90vh] shadow-2xl flex">

        {/* Left Side: React Flow */}
        <div className="w-2/5 border-r border-slate-200 flex flex-col">
          <div className="p-6 border-b border-slate-200">
            <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <Zap size={20} className="text-blue-600" />
              Conversation Flow
            </h3>
            <p className="text-xs text-slate-500 mt-1">Visual conversation logic</p>
          </div>

          <div className="flex-1 relative">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
            >
              <Background />
              <Controls />
            </ReactFlow>

            <div className="absolute bottom-4 left-4 bg-white p-3 rounded-lg shadow-lg border border-slate-200 max-w-[200px]">
              <p className="text-xs text-slate-600 mb-2">
                Click nodes to edit conversation steps
              </p>
              <button className="flex items-center gap-2 px-2 py-1.5 bg-blue-600 text-white rounded-md text-xs font-semibold hover:bg-blue-700 w-full">
                <Plus size={12} /> Add Node
              </button>
            </div>
          </div>
        </div>

        {/* Right Side: Configuration */}
        <div className="flex-1 flex flex-col">

          {/* Header */}
          <div className="p-6 border-b border-slate-200 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Settings size={20} className="text-blue-600" />
                {agentName}
              </h2>
              <p className="text-xs text-slate-500 mt-1">ElevenLabs Voice Agent Configuration</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleSave}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700"
              >
                <Save size={16} /> Save
              </button>
              <button
                onClick={onClose}
                className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Scrollable Configuration */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="space-y-6">

              {/* Voice Selection */}
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 className="font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <Phone size={16} className="text-blue-600" /> Voice Settings
                </h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">Voice Model</label>
                    <select
                      value={config.voice_id}
                      onChange={(e) => setConfig({ ...config, voice_id: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                    >
                      <option value="eleven_flash_v2_5">Flash v2.5 (Fastest)</option>
                      <option value="eleven_turbo_v2">Turbo v2 (High Quality)</option>
                      <option value="eleven_multilingual_v2">Multilingual v2</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">Language</label>
                    <select
                      value={config.language}
                      onChange={(e) => setConfig({ ...config, language: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                    >
                      <option value="en">English</option>
                      <option value="es">Spanish</option>
                      <option value="fr">French</option>
                      <option value="de">German</option>
                    </select>
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-semibold text-slate-700">Stability</label>
                      <span className="text-sm text-slate-600">{config.voice_settings?.stability.toFixed(2)}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.01"
                      value={config.voice_settings?.stability || 0.5}
                      onChange={(e) => setConfig({
                        ...config,
                        voice_settings: { ...config.voice_settings!, stability: parseFloat(e.target.value) }
                      })}
                      className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                    <p className="text-xs text-slate-500 mt-1">Lower = more variable, Higher = more consistent</p>
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-semibold text-slate-700">Similarity Boost</label>
                      <span className="text-sm text-slate-600">{config.voice_settings?.similarity_boost.toFixed(2)}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.01"
                      value={config.voice_settings?.similarity_boost || 0.75}
                      onChange={(e) => setConfig({
                        ...config,
                        voice_settings: { ...config.voice_settings!, similarity_boost: parseFloat(e.target.value) }
                      })}
                      className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>
                </div>
              </div>

              {/* First Message & Prompt */}
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 className="font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <MessageSquare size={16} className="text-blue-600" /> Conversation
                </h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">First Message</label>
                    <textarea
                      value={config.first_message}
                      onChange={(e) => setConfig({ ...config, first_message: e.target.value })}
                      rows={2}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                      placeholder="Opening message..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">System Prompt</label>
                    <textarea
                      value={config.prompt?.system_prompt}
                      onChange={(e) => setConfig({
                        ...config,
                        prompt: { ...config.prompt!, system_prompt: e.target.value }
                      })}
                      rows={5}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm font-mono"
                      placeholder="Agent behavior..."
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-2">Temperature</label>
                      <input
                        type="number"
                        min="0"
                        max="1"
                        step="0.1"
                        value={config.prompt?.temperature || 0.7}
                        onChange={(e) => setConfig({
                          ...config,
                          prompt: { ...config.prompt!, temperature: parseFloat(e.target.value) }
                        })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-2">Max Tokens</label>
                      <input
                        type="number"
                        value={config.prompt?.max_tokens || 500}
                        onChange={(e) => setConfig({
                          ...config,
                          prompt: { ...config.prompt!, max_tokens: parseInt(e.target.value) }
                        })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Call Settings */}
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 className="font-bold text-slate-900 mb-3">Call Settings</h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">Max Duration (seconds)</label>
                    <input
                      type="number"
                      value={config.max_duration_seconds || 600}
                      onChange={(e) => setConfig({ ...config, max_duration_seconds: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-semibold text-slate-700">Interruption Threshold</label>
                      <span className="text-sm text-slate-600">{config.interruption_threshold?.toFixed(1)}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={config.interruption_threshold || 0.5}
                      onChange={(e) => setConfig({ ...config, interruption_threshold: parseFloat(e.target.value) })}
                      className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">Keywords to Monitor</label>
                    <input
                      type="text"
                      value={config.keywords?.join(', ')}
                      onChange={(e) => setConfig({ ...config, keywords: e.target.value.split(',').map(k => k.trim()) })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                      placeholder="refund, fraud, cancel"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">Opt-out Phrase</label>
                    <input
                      type="text"
                      value={config.opt_out_phrase}
                      onChange={(e) => setConfig({ ...config, opt_out_phrase: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
                      placeholder="stop calling"
                    />
                  </div>
                </div>
              </div>

              {/* Webhooks */}
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                <h3 className="font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <FileText size={16} className="text-blue-600" /> Webhooks
                </h3>

                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">On Call Start</label>
                    <input
                      type="url"
                      value={config.webhook_events?.on_call_start}
                      onChange={(e) => setConfig({
                        ...config,
                        webhook_events: { ...config.webhook_events!, on_call_start: e.target.value }
                      })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-xs"
                      placeholder="https://api.example.com/call-start"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">On Call End</label>
                    <input
                      type="url"
                      value={config.webhook_events?.on_call_end}
                      onChange={(e) => setConfig({
                        ...config,
                        webhook_events: { ...config.webhook_events!, on_call_end: e.target.value }
                      })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-xs"
                      placeholder="https://api.example.com/call-end"
                    />
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
            <button className="flex items-center gap-2 px-3 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-semibold hover:bg-slate-300">
              <Play size={14} /> Test Agent
            </button>
            <div className="text-xs text-slate-500">
              ElevenLabs SDK Configuration
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
};

export default AgentFlowConfig;
