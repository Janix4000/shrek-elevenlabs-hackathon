import { GoogleGenAI } from "@google/genai";

// Initialize Gemini
// Note: In a real app, ensure process.env.API_KEY is handled securely.
// Depending on the environment this might be a placeholder until the user acts.
const getAI = () => {
    const apiKey = process.env.API_KEY;
    if (!apiKey) return null;
    return new GoogleGenAI({ apiKey });
};

export const analyzeDisputeTranscript = async (transcript: string, amount: number, customer: string) => {
  const ai = getAI();
  if (!ai) {
    // Fallback if no API Key provided
    return {
      recommendation: "Review Needed",
      reasoning: "API Key missing. Please check manual review guidelines.",
      action: "Manual Review"
    };
  }

  try {
    const prompt = `
      You are an expert Chargeback Analyst. Analyze the following customer service transcript for a dispute.
      Customer: ${customer}
      Dispute Amount: $${amount}
      
      Transcript:
      "${transcript}"

      Task:
      1. Determine if the merchant should issue a refund or fight the dispute (provide evidence).
      2. Provide a short reasoning summary (max 2 sentences).
      3. Assign a recommended action: "Approve Refund" or "Reject & Fight".

      Output JSON format:
      {
        "recommendation": "Approve Refund" | "Reject & Fight",
        "reasoning": "string",
        "confidence": number (0-100)
      }
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        responseMimeType: "application/json"
      }
    });

    const text = response.text;
    if (!text) throw new Error("No response from AI");
    
    return JSON.parse(text);

  } catch (error) {
    console.error("Gemini Analysis Error:", error);
    return {
      recommendation: "Error",
      reasoning: "AI could not process this request. Please review manually.",
      confidence: 0
    };
  }
};

export const simulateAgentResponse = async (userMessage: string, config: any) => {
    const ai = getAI();
    if (!ai) return "AI Configuration Error: No API Key.";

    try {
        const prompt = `
        Act as an automated voice agent for 'ChargeGuard'.
        Current Settings:
        - Tone: ${config.tone > 50 ? 'Highly Empathetic' : 'Formal and Direct'}
        - Verbosity: ${config.verbosity > 50 ? 'Conversational' : 'Concise'}
        
        The user says: "${userMessage}"
        
        Respond naturally as the agent.
        `;

        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
        });
        
        return response.text || "...";
    } catch (e) {
        return "System Error: Unable to generate response.";
    }
}