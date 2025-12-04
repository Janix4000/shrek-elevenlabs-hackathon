import React, { useState } from 'react';
import { Check, ExternalLink, Settings, AlertCircle, Plus, X } from 'lucide-react';
import { CreditCard } from 'lucide-react';

interface Integration {
  id: string;
  name: string;
  description: string;
  logoComponent: React.ReactNode;
  connected: boolean;
  status?: 'active' | 'warning' | 'error';
  lastSync?: string;
  metrics?: {
    label: string;
    value: string;
  }[];
}

const StripeLogo = () => (
  <div className="w-12 h-12 bg-[#635BFF] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M13.976 9.15c-2.172-.806-3.356-1.426-3.356-2.409 0-.831.683-1.305 1.901-1.305 2.227 0 4.515.858 6.09 1.631l.89-5.494C18.252.975 15.697 0 12.165 0 9.667 0 7.589.654 6.104 1.872 4.56 3.147 3.757 4.992 3.757 7.218c0 4.039 2.467 5.76 6.476 7.219 2.585.92 3.445 1.571 3.445 2.711 0 .866-.723 1.384-2.011 1.384-2.27 0-5.058-.973-6.962-2.168L3.757 22.03c2.082 1.19 4.91 1.97 7.734 1.97 2.682 0 4.866-.587 6.295-1.779 1.544-1.291 2.355-3.179 2.355-5.468.001-3.969-2.524-5.745-6.165-7.583z"/>
    </svg>
  </div>
);

const PayPalLogo = () => (
  <div className="w-12 h-12 bg-white border border-slate-200 rounded-lg flex items-center justify-center p-2">
    <img src="/paypal.png" alt="PayPal" className="w-full h-full object-contain" />
  </div>
);

const SquareLogo = () => (
  <div className="w-12 h-12 bg-[#000000] rounded-lg flex items-center justify-center">
    <div className="w-6 h-6 bg-white rounded"></div>
  </div>
);

const AdyenLogo = () => (
  <div className="w-12 h-12 bg-[#0ABF53] rounded-lg flex items-center justify-center text-white font-bold text-lg">
    A
  </div>
);

const BraintreeLogo = () => (
  <div className="w-12 h-12 bg-[#6772E5] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M12 2L3 7v5c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V7.3l7-3.89v9.58z"/>
    </svg>
  </div>
);

const AuthorizeNetLogo = () => (
  <div className="w-12 h-12 bg-[#0A2240] rounded-lg flex items-center justify-center">
    <CreditCard size={24} color="white" />
  </div>
);

const MollieLogo = () => (
  <div className="w-12 h-12 bg-gradient-to-br from-[#121212] to-[#000000] rounded-lg flex items-center justify-center text-white font-bold text-sm">
    mollie
  </div>
);

const VisaLogo = () => (
  <div className="w-12 h-12 bg-white border border-slate-200 rounded-lg flex items-center justify-center p-2">
    <img src="/Visa_Brandmark_Blue_RGB-1.png" alt="Visa" className="w-full h-full object-contain" />
  </div>
);

const MastercardLogo = () => (
  <div className="w-12 h-12 bg-white border border-slate-200 rounded-lg flex items-center justify-center">
    <div className="relative w-6 h-4">
      <div className="w-4 h-4 bg-[#EB001B] rounded-full absolute left-0 top-0"></div>
      <div className="w-4 h-4 bg-[#F79E1B] rounded-full absolute right-0 top-0"></div>
    </div>
  </div>
);

const AmexLogo = () => (
  <div className="w-12 h-12 bg-white border border-slate-200 rounded-lg flex items-center justify-center p-2">
    <img src="/amex.png" alt="American Express" className="w-full h-full object-contain" />
  </div>
);

const SalesforceLogo = () => (
  <div className="w-12 h-12 bg-[#00A1E0] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M10.006 5.412a3.986 3.986 0 013.54-2.138c1.169 0 2.226.503 2.954 1.302a5.483 5.483 0 012.208-.465c3.013 0 5.456 2.443 5.456 5.455a5.436 5.436 0 01-1.11 3.3 4.853 4.853 0 011.112 3.088c0 2.687-2.178 4.865-4.865 4.865-.486 0-.954-.073-1.396-.206a4.615 4.615 0 01-3.9 2.137 4.612 4.612 0 01-3.856-2.074 3.98 3.98 0 01-1.502.292A3.988 3.988 0 014.66 16.98a5.455 5.455 0 01-2.825-4.788c0-3.013 2.443-5.456 5.456-5.456.266 0 .527.02.783.058a3.968 3.968 0 011.932-1.382z"/>
    </svg>
  </div>
);

const HubspotLogo = () => (
  <div className="w-12 h-12 bg-[#FF7A59] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M18.164 7.93V5.084a2.198 2.198 0 001.267-1.978v-.083A2.198 2.198 0 0017.233.825h-.082a2.198 2.198 0 00-2.198 2.198v.083c0 .843.474 1.576 1.167 1.946V7.93a5.33 5.33 0 00-2.821 1.409l-7.096-5.06a2.196 2.196 0 10-.978 1.37l7.038 5.018a5.335 5.335 0 00-1.087 3.228c0 2.95 2.386 5.337 5.337 5.337s5.337-2.387 5.337-5.337a5.331 5.331 0 00-3.686-5.056v-.01z"/>
    </svg>
  </div>
);

const ZendeskLogo = () => (
  <div className="w-12 h-12 bg-[#03363D] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M12.914 2.904V16.29L2.5 2.905h10.414zM2.5 21.096V7.71L12.914 21.096H2.5zm18.086 0H10.172V7.71L20.586 21.096zM10.172 2.904h10.414V16.29L10.172 2.905z"/>
    </svg>
  </div>
);

const IntercomLogo = () => (
  <div className="w-12 h-12 bg-[#1F8DED] rounded-lg flex items-center justify-center">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
      <path d="M17.625 12.188c0 .207-.168.375-.375.375s-.375-.168-.375-.375V8.813c0-.207.168-.375.375-.375s.375.168.375.375v3.375zm-2.25 1.5c0 .207-.168.375-.375.375s-.375-.168-.375-.375V7.313c0-.207.168-.375.375-.375s.375.168.375.375v6.375zm-2.25 1.124c0 .207-.168.375-.375.375s-.375-.168-.375-.375V6.563c0-.207.168-.375.375-.375s.375.168.375.375v8.25zm-2.25-1.124c0 .207-.168.375-.375.375s-.375-.168-.375-.375V7.313c0-.207.168-.375.375-.375s.375.168.375.375v6.375zm-2.25-1.5c0 .207-.168.375-.375.375s-.375-.168-.375-.375V8.813c0-.207.168-.375.375-.375s.375.168.375.375v3.375zM12 3.75c-4.556 0-8.25 3.694-8.25 8.25S7.444 20.25 12 20.25s8.25-3.694 8.25-8.25S16.556 3.75 12 3.75z"/>
    </svg>
  </div>
);

const KlarnaLogo = () => (
  <div className="w-12 h-12 bg-white border border-slate-200 rounded-lg flex items-center justify-center p-2">
    <img src="/Klarna.png" alt="Klarna" className="w-full h-full object-contain" />
  </div>
);

const INTEGRATIONS: Integration[] = [
  {
    id: 'stripe',
    name: 'Stripe',
    description: 'Accept payments and manage disputes globally',
    logoComponent: <StripeLogo />,
    connected: true,
    status: 'active',
    lastSync: '2 mins ago',
    metrics: [
      { label: 'Disputes', value: '47' },
      { label: 'Win Rate', value: '68%' }
    ]
  },
  {
    id: 'paypal',
    name: 'PayPal',
    description: 'Process PayPal and credit card payments',
    logoComponent: <PayPalLogo />,
    connected: true,
    status: 'active',
    lastSync: '5 mins ago',
    metrics: [
      { label: 'Disputes', value: '23' },
      { label: 'Win Rate', value: '72%' }
    ]
  },
  {
    id: 'square',
    name: 'Square',
    description: 'Point of sale and online payment processing',
    logoComponent: <SquareLogo />,
    connected: true,
    status: 'active',
    lastSync: '12 mins ago',
    metrics: [
      { label: 'Disputes', value: '8' },
      { label: 'Win Rate', value: '75%' }
    ]
  },
  {
    id: 'visa',
    name: 'Visa',
    description: 'Direct integration with Visa dispute network',
    logoComponent: <VisaLogo />,
    connected: true,
    status: 'active',
    lastSync: '1 min ago',
    metrics: [
      { label: 'Disputes', value: '156' },
      { label: 'Win Rate', value: '64%' }
    ]
  },
  {
    id: 'mastercard',
    name: 'Mastercard',
    description: 'Mastercard chargeback management',
    logoComponent: <MastercardLogo />,
    connected: true,
    status: 'active',
    lastSync: '3 mins ago',
    metrics: [
      { label: 'Disputes', value: '98' },
      { label: 'Win Rate', value: '69%' }
    ]
  },
  {
    id: 'amex',
    name: 'American Express',
    description: 'Amex dispute resolution system',
    logoComponent: <AmexLogo />,
    connected: true,
    status: 'active',
    lastSync: '7 mins ago',
    metrics: [
      { label: 'Disputes', value: '34' },
      { label: 'Win Rate', value: '71%' }
    ]
  },
  {
    id: 'adyen',
    name: 'Adyen',
    description: 'End-to-end payments platform for enterprises',
    logoComponent: <AdyenLogo />,
    connected: true,
    status: 'active',
    lastSync: '8 mins ago',
    metrics: [
      { label: 'Disputes', value: '12' },
      { label: 'Win Rate', value: '81%' }
    ]
  },
  {
    id: 'salesforce',
    name: 'Salesforce',
    description: 'Sync customer and transaction data',
    logoComponent: <SalesforceLogo />,
    connected: true,
    status: 'active',
    lastSync: '15 mins ago',
    metrics: [
      { label: 'Contacts', value: '12.4k' }
    ]
  },
  {
    id: 'hubspot',
    name: 'HubSpot',
    description: 'Customer relationship management platform',
    logoComponent: <HubspotLogo />,
    connected: true,
    status: 'active',
    lastSync: '22 mins ago',
    metrics: [
      { label: 'Contacts', value: '8.9k' }
    ]
  },
  {
    id: 'zendesk',
    name: 'Zendesk',
    description: 'Customer support ticket integration',
    logoComponent: <ZendeskLogo />,
    connected: true,
    status: 'active',
    lastSync: '6 mins ago',
    metrics: [
      { label: 'Tickets', value: '342' }
    ]
  },
  {
    id: 'klarna',
    name: 'Klarna',
    description: 'Buy now, pay later payment solution',
    logoComponent: <KlarnaLogo />,
    connected: true,
    status: 'active',
    lastSync: '4 mins ago',
    metrics: [
      { label: 'Disputes', value: '19' },
      { label: 'Win Rate', value: '73%' }
    ]
  },
  {
    id: 'intercom',
    name: 'Intercom',
    description: 'Live chat and customer messaging',
    logoComponent: <IntercomLogo />,
    connected: false,
    status: undefined
  },
  {
    id: 'braintree',
    name: 'Braintree',
    description: 'PayPal-owned payment gateway service',
    logoComponent: <BraintreeLogo />,
    connected: false,
    status: undefined
  },
  {
    id: 'authorize-net',
    name: 'Authorize.Net',
    description: 'Payment gateway for online transactions',
    logoComponent: <AuthorizeNetLogo />,
    connected: false,
    status: undefined
  },
  {
    id: 'mollie',
    name: 'Mollie',
    description: 'European payment processor with local methods',
    logoComponent: <MollieLogo />,
    connected: false,
    status: undefined
  }
];

const Integrations: React.FC = () => {
  const connectedCount = INTEGRATIONS.filter(i => i.connected).length;
  const [configModal, setConfigModal] = useState<string | null>(null);
  const [stripeConfig, setStripeConfig] = useState({
    apiKey: 'sk_live_••••••••••••••••••••••••4242',
    webhookSecret: 'whsec_••••••••••••••••••••••••',
    autoSync: true,
    syncInterval: '5',
    disputeNotifications: true,
    testMode: false
  });

  const handleConfigure = (integrationId: string) => {
    setConfigModal(integrationId);
  };

  const handleSaveConfig = () => {
    // Here you would save the configuration
    setConfigModal(null);
  };

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl p-6 border border-slate-200">
          <div className="text-sm text-slate-500 mb-2">Connected</div>
          <div className="text-3xl font-bold text-slate-900">{connectedCount}</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-slate-200">
          <div className="text-sm text-slate-500 mb-2">Transactions Synced</div>
          <div className="text-3xl font-bold text-slate-900">378k</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-slate-200">
          <div className="text-sm text-slate-500 mb-2">Avg Sync Time</div>
          <div className="text-3xl font-bold text-slate-900">5 min</div>
        </div>
      </div>

      {/* Connected Integrations */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-900">Active Integrations</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {INTEGRATIONS.filter(i => i.connected).map((integration) => (
          <div
            key={integration.id}
            className="bg-white rounded-xl border border-slate-200 p-5"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                {integration.logoComponent}
                <div>
                  <h3 className="font-semibold text-slate-900">{integration.name}</h3>
                  <p className="text-xs text-slate-500">
                    {['salesforce', 'hubspot', 'zendesk', 'intercom'].includes(integration.id) ? 'CRM & Support' : 'Payment Processor'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700">
                <Check size={12} />
                Active
              </div>
            </div>

            {/* Metrics */}
            {integration.metrics && (
              <div className="flex items-center gap-4 mb-3 pb-3 border-b border-slate-100">
                {integration.metrics.map((metric, idx) => (
                  <div key={idx}>
                    <p className="text-xs text-slate-500">{metric.label}</p>
                    <p className="text-sm font-semibold text-slate-900">{metric.value}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Last Sync */}
            {integration.lastSync && (
              <div className="text-xs text-slate-500 mb-3">
                Last synced: {integration.lastSync}
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleConfigure(integration.id)}
                className="flex-1 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
              >
                <Settings size={14} />
                Configure
              </button>
              <button className="px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 rounded-lg text-sm font-medium transition-colors">
                <ExternalLink size={14} />
              </button>
            </div>
          </div>
        ))}
        </div>
      </div>

      {/* Available Integrations */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-900">Available Integrations</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {INTEGRATIONS.filter(i => !i.connected).map((integration) => (
            <div
              key={integration.id}
              className="bg-white rounded-xl border border-slate-200 hover:border-slate-300 transition-all p-4"
            >
              <div className="flex items-center gap-3 mb-3">
                {integration.logoComponent}
                <div className="flex-1">
                  <h3 className="font-semibold text-slate-900 text-sm">{integration.name}</h3>
                </div>
              </div>

              <p className="text-xs text-slate-600 mb-3">{integration.description}</p>

              <button className="w-full px-3 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2">
                <Plus size={14} />
                Connect
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Configuration Modal */}
      {configModal === 'stripe' && (
        <>
          <div
            className="fixed inset-0 bg-slate-900 opacity-50 z-40"
            onClick={() => setConfigModal(null)}
          ></div>
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              {/* Header */}
              <div className="p-6 border-b border-slate-200 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <StripeLogo />
                  <div>
                    <h2 className="text-xl font-bold text-slate-900">Stripe Configuration</h2>
                    <p className="text-sm text-slate-500">Manage your Stripe integration settings</p>
                  </div>
                </div>
                <button
                  onClick={() => setConfigModal(null)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  <X size={24} />
                </button>
              </div>

              {/* Content */}
              <div className="p-6 space-y-6">
                {/* API Keys Section */}
                <div>
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">API Credentials</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Secret Key
                      </label>
                      <input
                        type="password"
                        value={stripeConfig.apiKey}
                        onChange={(e) => setStripeConfig({ ...stripeConfig, apiKey: e.target.value })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                      <p className="text-xs text-slate-500 mt-1">Your Stripe secret API key (starts with sk_)</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Webhook Secret
                      </label>
                      <input
                        type="password"
                        value={stripeConfig.webhookSecret}
                        onChange={(e) => setStripeConfig({ ...stripeConfig, webhookSecret: e.target.value })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                      <p className="text-xs text-slate-500 mt-1">Webhook signing secret (starts with whsec_)</p>
                    </div>
                  </div>
                </div>

                {/* Sync Settings */}
                <div className="border-t border-slate-200 pt-6">
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">Sync Settings</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <label className="text-sm font-medium text-slate-700">Auto Sync</label>
                        <p className="text-xs text-slate-500">Automatically sync disputes from Stripe</p>
                      </div>
                      <button
                        onClick={() => setStripeConfig({ ...stripeConfig, autoSync: !stripeConfig.autoSync })}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          stripeConfig.autoSync ? 'bg-indigo-600' : 'bg-slate-300'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            stripeConfig.autoSync ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Sync Interval (minutes)
                      </label>
                      <select
                        value={stripeConfig.syncInterval}
                        onChange={(e) => setStripeConfig({ ...stripeConfig, syncInterval: e.target.value })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="1">Every 1 minute</option>
                        <option value="5">Every 5 minutes</option>
                        <option value="15">Every 15 minutes</option>
                        <option value="30">Every 30 minutes</option>
                        <option value="60">Every hour</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Notifications */}
                <div className="border-t border-slate-200 pt-6">
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">Notifications</h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-slate-700">Dispute Notifications</label>
                      <p className="text-xs text-slate-500">Receive alerts for new disputes</p>
                    </div>
                    <button
                      onClick={() => setStripeConfig({ ...stripeConfig, disputeNotifications: !stripeConfig.disputeNotifications })}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        stripeConfig.disputeNotifications ? 'bg-indigo-600' : 'bg-slate-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          stripeConfig.disputeNotifications ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                {/* Test Mode */}
                <div className="border-t border-slate-200 pt-6">
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">Environment</h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-slate-700">Test Mode</label>
                      <p className="text-xs text-slate-500">Use Stripe test environment</p>
                    </div>
                    <button
                      onClick={() => setStripeConfig({ ...stripeConfig, testMode: !stripeConfig.testMode })}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        stripeConfig.testMode ? 'bg-indigo-600' : 'bg-slate-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          stripeConfig.testMode ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                {/* Data Fields Synced */}
                <div className="border-t border-slate-200 pt-6">
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">Data Fields Synced from Stripe</h3>
                  <div className="bg-slate-50 rounded-lg p-4 space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <p className="text-xs font-semibold text-slate-900">Dispute Information</p>
                        <ul className="text-xs text-slate-600 mt-1 space-y-0.5">
                          <li>• Dispute ID & Status</li>
                          <li>• Amount & Currency</li>
                          <li>• Reason & Evidence</li>
                          <li>• Response Deadline</li>
                        </ul>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-900">Customer Data</p>
                        <ul className="text-xs text-slate-600 mt-1 space-y-0.5">
                          <li>• Name & Email</li>
                          <li>• Phone Number</li>
                          <li>• Billing Address</li>
                          <li>• Purchase History</li>
                        </ul>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-900">Transaction Details</p>
                        <ul className="text-xs text-slate-600 mt-1 space-y-0.5">
                          <li>• Charge ID & Amount</li>
                          <li>• Payment Method</li>
                          <li>• Order Description</li>
                          <li>• Transaction Date</li>
                        </ul>
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-slate-900">Delivery Information</p>
                        <ul className="text-xs text-slate-600 mt-1 space-y-0.5">
                          <li>• Shipping Address</li>
                          <li>• Tracking Number</li>
                          <li>• Delivery Status</li>
                          <li>• GPS Coordinates</li>
                        </ul>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-900 mb-1">Webhook Events</p>
                      <div className="flex flex-wrap gap-2">
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">charge.dispute.created</span>
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">charge.dispute.updated</span>
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">charge.dispute.closed</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-xs text-slate-500 mt-2">
                    All data is encrypted in transit and at rest. Synced every {stripeConfig.syncInterval} minute{stripeConfig.syncInterval !== '1' ? 's' : ''}.
                  </p>
                </div>

                {/* Sample Data Preview */}
                <div className="border-t border-slate-200 pt-6">
                  <h3 className="text-sm font-semibold text-slate-900 mb-3">Sample Data Preview</h3>
                  <div className="bg-slate-900 rounded-lg p-4 max-h-64 overflow-y-auto">
                    <pre className="text-xs text-slate-300 font-mono leading-relaxed">
{`{
  "dispute": {
    "id": "dp_1234567890abcdef",
    "amount": 8995,
    "currency": "usd",
    "status": "needs_response",
    "reason": "fraudulent",
    "evidence_details": {
      "due_by": 1694520000
    },
    "charge": {
      "id": "ch_3NzQ2L...",
      "amount": 8995,
      "customer": "cus_OwnerID123",
      "description": "Huel Black Edition x2",
      "receipt_email": "customer@email.com",
      "shipping": {
        "name": "Customer Name",
        "address": {
          "line1": "123 Main Street",
          "city": "Portland",
          "state": "OR",
          "postal_code": "97201"
        },
        "tracking_number": "9400116901234567890",
        "tracking_status": "delivered"
      },
      "metadata": {
        "delivery_gps": "45.5152,-122.6784"
      }
    },
    "payment_method_details": {
      "card": {
        "brand": "visa",
        "last4": "4242"
      }
    }
  },
  "customer": {
    "name": "Customer Name",
    "email": "customer@email.com",
    "phone": "+15035551234"
  }
}`}
                    </pre>
                  </div>
                  <p className="text-xs text-slate-500 mt-2">
                    This is a sanitized example. Actual data includes more fields and varies by dispute type.
                  </p>
                </div>
              </div>

              {/* Footer */}
              <div className="p-6 border-t border-slate-200 flex items-center justify-between">
                <button
                  onClick={() => setConfigModal(null)}
                  className="px-4 py-2 text-slate-700 hover:text-slate-900 font-medium"
                >
                  Cancel
                </button>
                <div className="flex items-center gap-3">
                  <button
                    onClick={handleSaveConfig}
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Integrations;