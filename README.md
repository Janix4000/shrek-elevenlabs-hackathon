# ChargeGuard - AI-Powered Dispute Resolution Platform

ChargeGuard is an end-to-end dispute resolution platform powered by ElevenLabs voice AI and RAG (Retrieval-Augmented Generation). The platform automatically handles customer disputes through natural voice conversations and provides a comprehensive dashboard for monitoring and management.

## Project Structure

```
shrek-elevenlabs-hackathon/
├── backend/          # Python backend with ElevenLabs integration
│   ├── main.py              # Main application entry point
│   ├── rag_service.py       # RAG service for dispute analysis
│   ├── elevenlabs_wrapper/  # ElevenLabs API wrapper
│   ├── policies.json        # Company policies
│   ├── orders.json          # Order data
│   └── requirements.txt     # Python dependencies
├── frontend/         # React + TypeScript dashboard
│   ├── components/          # React components
│   ├── services/            # API services
│   ├── App.tsx             # Main app component
│   └── package.json        # Node dependencies
└── README.md        # This file
```

## Features

### Backend
- **ElevenLabs Voice AI Integration**: Natural conversational AI for handling customer disputes
- **RAG Pipeline**: Retrieval-Augmented Generation for policy-aware dispute resolution
- **Pinecone Vector Database**: Stores and retrieves relevant policies and past cases
- **Dispute Classification**: Automatically categorizes disputes (fraud, delivery issues, etc.)
- **Real-time Transcription**: Converts voice conversations to text

### Frontend
- **Interactive Dashboard**: Real-time overview of dispute resolution metrics
- **Dispute Management**: Search, filter, and review all disputes
- **Agent Studio**: Configure and manage ElevenLabs voice agents
- **Analytics**: Win rates by country, dispute reasons breakdown
- **RAG Pipeline Visualization**: See the AI decision-making process in action

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn
- ElevenLabs API key
- Pinecone API key
- Google Gemini API key (for RAG)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
export PINECONE_API_KEY="your-pinecone-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

4. Upload policies to Pinecone:
```bash
python upload_to_pinecone.py
```

5. Run the backend:
```bash
python main.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:5173](http://localhost:5173) in your browser

### Building for Production

#### Frontend
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`.

## Tech Stack

### Backend
- **Python 3.8+**
- **ElevenLabs API**: Conversational AI voice agents
- **Pinecone**: Vector database for RAG
- **Google Gemini**: AI for dispute analysis
- **FastAPI/Flask**: REST API (if applicable)

### Frontend
- **React 19.2.1**: UI framework
- **TypeScript 5.8.2**: Type safety
- **Vite 6.2.0**: Build tool and dev server
- **Tailwind CSS 3.4.18**: Styling
- **Recharts 3.5.1**: Data visualization
- **react-simple-maps 3.0.0**: Geographical visualizations
- **Lucide React**: Icon library

## Configuration

### Backend Configuration
Edit the following JSON files in the `backend/` directory:
- `policies.json`: Company return/refund policies
- `orders.json`: Order and customer data
- `dispute_scripts.json`: Conversation templates
- `resolution_authority.json`: Escalation rules

### Frontend Configuration
The frontend connects to the backend API. Update the API endpoint in `frontend/services/geminiService.ts` if needed.

## API Integration

The frontend expects the backend to expose the following endpoints:

- `POST /api/analyze-dispute`: Analyze a dispute transcript
- `GET /api/disputes`: Get all disputes
- `GET /api/metrics`: Get KPI metrics
- `POST /api/agent/configure`: Configure voice agent

## Deployment

### Deploy to Vercel (Frontend)
```bash
cd frontend
vercel deploy
```

### Deploy Backend
The backend can be deployed to:
- **Railway**: Python deployment platform
- **Render**: Web service deployment
- **AWS Lambda**: Serverless deployment
- **Google Cloud Run**: Container deployment

## Environment Variables

### Backend
```
ELEVENLABS_API_KEY=your-key-here
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=your-environment
GEMINI_API_KEY=your-key-here
```

### Frontend
```
VITE_API_URL=http://localhost:8000
VITE_GEMINI_API_KEY=your-key-here
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project was created for the ElevenLabs Hackathon.

## Acknowledgments

- **ElevenLabs**: For the amazing voice AI platform
- **Huel**: Product data inspiration
- **Pinecone**: Vector database infrastructure
- **Google Gemini**: AI capabilities
