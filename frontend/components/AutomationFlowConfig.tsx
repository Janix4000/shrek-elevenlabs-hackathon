import React, { useState } from 'react';
import { X, Save, MapPin, Globe, Wrench, Phone, Mail, MessageSquare, Clock } from 'lucide-react';

export interface AutomationConfig {
  name: string;
  trigger: {
    event: string;
    conditions: string[];
    threshold: number;
  };
  frequency: {
    timing: string;
    maxAttempts: number;
    retryInterval: number;
  };
  geography: {
    regions: string[];
    businessHours: { start: string; end: string };
  };
  language: {
    primary: string;
    autoDetect: boolean;
  };
  tools: {
    voice: boolean;
    email: boolean;
    sms: boolean;
  };
}

interface AutomationFlowConfigProps {
  automationName: string;
  onClose: () => void;
  onSave: (config: AutomationConfig) => void;
}

const AutomationFlowConfig: React.FC<AutomationFlowConfigProps> = ({
  automationName,
  onClose,
  onSave,
}) => {
  const [geography, setGeography] = useState({
    regions: ['North America', 'Europe'],
    businessHours: { start: '09:00', end: '17:00' },
  });

  const [language, setLanguage] = useState({
    primary: 'English',
    autoDetect: true,
  });

  const [tools, setTools] = useState({
    voice: true,
    email: true,
    sms: false,
  });

  const [trigger, setTrigger] = useState({
    event: 'dispute_value',
    conditions: ['value_exceeds_threshold'],
    threshold: 100,
  });

  const [frequency, setFrequency] = useState({
    timing: 'immediately',
    maxAttempts: 3,
    retryInterval: 2,
  });

  const handleSave = () => {
    const config: AutomationConfig = {
      name: automationName,
      trigger,
      frequency,
      geography,
      language,
      tools,
    };
    onSave(config);
  };

  const regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America'];
  const languages = ['English', 'Spanish', 'French', 'German', 'Portuguese'];

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-6" onClick={onClose}>
      <div
        className="bg-card rounded-xl w-full max-w-3xl shadow-2xl max-h-[90vh] overflow-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-border sticky top-0 bg-card z-10">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">{automationName}</h2>
            <p className="text-sm text-slate-500 mt-1">Configure automation settings</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X size={20} className="text-slate-600" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-8">

          {/* Trigger Settings */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <Clock size={16} className="text-blue-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Trigger Conditions</h3>
            </div>

            <div className="space-y-4 pl-10">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  When to activate this automation
                </label>
                <select
                  value={trigger.event}
                  onChange={(e) => setTrigger({ ...trigger, event: e.target.value })}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 font-medium"
                >
                  <option value="dispute_value">Dispute value exceeds threshold</option>
                  <option value="dispute_created">Immediately when dispute is created</option>
                  <option value="fraud_detected">Fraud pattern detected</option>
                  <option value="time_elapsed">After time period elapses</option>
                </select>
              </div>

              {trigger.event === 'dispute_value' && (
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Threshold amount ($)
                  </label>
                  <input
                    type="number"
                    value={trigger.threshold}
                    onChange={(e) => setTrigger({ ...trigger, threshold: Number(e.target.value) })}
                    className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 font-medium"
                  />
                </div>
              )}
            </div>
          </div>

          {/* Frequency */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                <Clock size={16} className="text-indigo-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Frequency & Retry Settings</h3>
            </div>

            <div className="space-y-4 pl-10">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  When to execute
                </label>
                <select
                  value={frequency.timing}
                  onChange={(e) => setFrequency({ ...frequency, timing: e.target.value })}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 font-medium"
                >
                  <option value="immediately">Immediately</option>
                  <option value="after_5_min">After 5 minutes</option>
                  <option value="after_1_hour">After 1 hour</option>
                  <option value="after_24_hours">After 24 hours</option>
                  <option value="business_hours_only">Next business hours</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Maximum retry attempts
                </label>
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={frequency.maxAttempts}
                    onChange={(e) => setFrequency({ ...frequency, maxAttempts: Number(e.target.value) })}
                    className="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <span className="text-sm font-bold text-slate-900 w-8 text-center">{frequency.maxAttempts}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Number of times to retry if initial attempt fails</p>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Retry interval (hours)
                </label>
                <input
                  type="number"
                  min="1"
                  max="48"
                  value={frequency.retryInterval}
                  onChange={(e) => setFrequency({ ...frequency, retryInterval: Number(e.target.value) })}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 font-medium"
                />
                <p className="text-xs text-slate-500 mt-1">Time to wait between retry attempts</p>
              </div>
            </div>
          </div>

          {/* Geography */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                <MapPin size={16} className="text-emerald-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Geography</h3>
            </div>

            <div className="space-y-4 pl-10">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Active regions
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {regions.map((region) => (
                    <label
                      key={region}
                      className="flex items-center gap-2 p-3 border-2 border-slate-200 rounded-lg cursor-pointer hover:border-blue-300 transition-colors has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50"
                    >
                      <input
                        type="checkbox"
                        checked={geography.regions.includes(region)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setGeography({
                              ...geography,
                              regions: [...geography.regions, region],
                            });
                          } else {
                            setGeography({
                              ...geography,
                              regions: geography.regions.filter((r) => r !== region),
                            });
                          }
                        }}
                        className="w-4 h-4 text-blue-600"
                      />
                      <span className="text-sm font-medium text-slate-900">{region}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Business hours (local time)
                </label>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <input
                      type="time"
                      value={geography.businessHours.start}
                      onChange={(e) =>
                        setGeography({
                          ...geography,
                          businessHours: { ...geography.businessHours, start: e.target.value },
                        })
                      }
                      className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <input
                      type="time"
                      value={geography.businessHours.end}
                      onChange={(e) =>
                        setGeography({
                          ...geography,
                          businessHours: { ...geography.businessHours, end: e.target.value },
                        })
                      }
                      className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Language */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <Globe size={16} className="text-purple-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Language</h3>
            </div>

            <div className="space-y-4 pl-10">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Primary language
                </label>
                <select
                  value={language.primary}
                  onChange={(e) => setLanguage({ ...language, primary: e.target.value })}
                  className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-blue-500 font-medium"
                >
                  {languages.map((lang) => (
                    <option key={lang} value={lang}>
                      {lang}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-start gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <input
                  type="checkbox"
                  id="autoDetect"
                  checked={language.autoDetect}
                  onChange={(e) => setLanguage({ ...language, autoDetect: e.target.checked })}
                  className="mt-0.5 w-4 h-4 text-blue-600"
                />
                <label htmlFor="autoDetect" className="flex-1">
                  <div className="font-semibold text-blue-900 text-sm">
                    Auto-detect customer language
                  </div>
                  <div className="text-xs text-blue-700 mt-1">
                    Automatically use customer's preferred language from their profile
                  </div>
                </label>
              </div>
            </div>
          </div>

          {/* Communication Tools */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-amber-100 rounded-lg flex items-center justify-center">
                <Wrench size={16} className="text-amber-600" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Communication Channels</h3>
            </div>

            <div className="space-y-3 pl-10">
              {/* Voice */}
              <div className="flex items-center justify-between p-4 border-2 border-slate-200 rounded-lg">
                <div className="flex items-center gap-3">
                  <Phone size={20} className="text-blue-600" />
                  <div>
                    <div className="font-semibold text-slate-900 text-sm">Voice Call</div>
                    <div className="text-xs text-slate-500">AI-powered phone calls</div>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={tools.voice}
                    onChange={(e) => setTools({ ...tools, voice: e.target.checked })}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              {/* Email */}
              <div className="flex items-center justify-between p-4 border-2 border-slate-200 rounded-lg">
                <div className="flex items-center gap-3">
                  <Mail size={20} className="text-emerald-600" />
                  <div>
                    <div className="font-semibold text-slate-900 text-sm">Email</div>
                    <div className="text-xs text-slate-500">Automated email notifications</div>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={tools.email}
                    onChange={(e) => setTools({ ...tools, email: e.target.checked })}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                </label>
              </div>

              {/* SMS */}
              <div className="flex items-center justify-between p-4 border-2 border-slate-200 rounded-lg">
                <div className="flex items-center gap-3">
                  <MessageSquare size={20} className="text-purple-600" />
                  <div>
                    <div className="font-semibold text-slate-900 text-sm">SMS</div>
                    <div className="text-xs text-slate-500">Text message alerts</div>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={tools.sms}
                    onChange={(e) => setTools({ ...tools, sms: e.target.checked })}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                </label>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="flex gap-3 p-6 border-t border-border bg-muted sticky bottom-0">
          <button
            onClick={handleSave}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-slate-900 text-white rounded-lg font-semibold hover:bg-slate-800"
          >
            <Save size={16} />
            Save Configuration
          </button>
          <button
            onClick={onClose}
            className="px-4 py-3 border border-border rounded-lg text-muted-foreground hover:bg-card font-semibold"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AutomationFlowConfig;
