export enum DisputeStatus {
  ActionRequired = 'Action Required',
  Pending = 'Pending',
  Won = 'Won',
  Lost = 'Lost',
}

export type PaymentSource = 'amex' | 'mastercard' | 'visa' | 'paypal' | 'stripe' | 'klarna';

export interface Dispute {
  id: string;
  customerName: string;
  amount: number;
  timeLeftHours: number; // For the 72h window
  status: DisputeStatus;
  confidenceScore: number;
  transcript: string;
  orderItems: string[];
  date: string;
  paymentSource: PaymentSource;
  agentName: string;
  callResult: string;
}

export interface AgentConfig {
  name: string;
  voiceId: string;
  tone: number; // 0 (Formal) to 100 (Empathetic)
  verbosity: number; // 0 (Concise) to 100 (Talkative)
  returnPolicy: string;
}

export interface KPIMetrics {
  savedRevenue: number;
  deflectionRate: number;
  activeDisputes: number;
  recentWins: { id: string; message: string; time: string }[];
}

// Navigation View State
export type ViewState = 'overview' | 'disputes' | 'automations' | 'agent-studio' | 'integrations';