import { ConversationStartResponse, ConversationResult } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const conversationService = {
  /**
   * Start a new conversation with the given charge ID
   */
  async startConversation(
    chargeId: string,
    fakeConv: boolean = false,
    updateStripe: boolean = false
  ): Promise<ConversationStartResponse> {
    const response = await fetch(
      `${API_BASE_URL}/api/conversation/start?fake_conv=${fakeConv}&update_stripe=${updateStripe}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ charge_id: chargeId }),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to start conversation: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Get the result of a conversation by ID
   */
  async getConversationResult(conversationId: string): Promise<ConversationResult> {
    const response = await fetch(
      `${API_BASE_URL}/api/conversation/${conversationId}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to get conversation result: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Poll for conversation completion
   * Returns a promise that resolves when the conversation is completed or failed
   */
  async pollForCompletion(
    conversationId: string,
    onUpdate?: (result: ConversationResult) => void,
    intervalMs: number = 5000, // Poll every 5 seconds
    timeoutMs: number = 600000, // 10 minutes
    initialDelayMs: number = 60000 // Wait 1 minute before starting to poll
  ): Promise<ConversationResult> {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const result = await this.getConversationResult(conversationId);

          // Call the update callback if provided
          if (onUpdate) {
            onUpdate(result);
          }

          // Check if completed or failed
          if (result.status === 'completed' || result.status === 'failed') {
            resolve(result);
            return;
          }

          // Check timeout
          if (Date.now() - startTime > timeoutMs) {
            reject(new Error('Polling timeout'));
            return;
          }

          // Continue polling
          setTimeout(poll, intervalMs);
        } catch (error) {
          reject(error);
        }
      };

      // Wait 1 minute before starting to poll
      setTimeout(poll, initialDelayMs);
    });
  },
};
