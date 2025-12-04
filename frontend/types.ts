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
  chargeId?: string; // Stripe charge ID for conversation
  conversationId?: string; // Active conversation ID
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

// Conversation API Types
export enum ConversationStatus {
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export interface TranscriptEntry {
  speaker: 'agent' | 'user';
  text: string;
  timestamp: number;
}

export interface DisputeEvaluation {
  resolved: boolean;
  resolution_type?: string;
  confidence?: number;
  reasoning?: string;
}

export interface EvidenceResult {
  dispute_id: string;
  evaluation: DisputeEvaluation;
  evidence_generated: Record<string, string>;
  status: string;
  submitted_to_stripe: boolean;
}

export interface ConversationResult {
  conversation_id: string;
  status: ConversationStatus;
  transcript?: TranscriptEntry[];
  duration_seconds?: number;
  summary?: string;
  evidence_result?: EvidenceResult;
  error?: string;
}

export interface ConversationStartResponse {
  conversation_id: string;
  status: 'started';
}