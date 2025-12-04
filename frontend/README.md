# ChargeGuard Dashboard - Frontend

This is the React + TypeScript frontend for the ChargeGuard dispute resolution platform.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- **Dashboard**: Overview of KPIs, win rates, and dispute trends
- **Disputes**: Manage and search through all disputes
- **Agent Studio**: Configure ElevenLabs voice agents
- **Automations**: Set up automated workflows
- **Integrations**: Connect with payment processors

## Tech Stack

- React 19.2.1
- TypeScript 5.8.2
- Vite 6.2.0
- Tailwind CSS 3.4.18
- Recharts (data visualization)
- React Simple Maps (geographical data)
- Lucide React (icons)

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_GEMINI_API_KEY=your-gemini-api-key
```

## Project Structure

```
frontend/
├── components/          # React components
│   ├── Dashboard.tsx   # Main dashboard view
│   ├── Disputes.tsx    # Dispute management
│   ├── AgentStudio.tsx # Agent configuration
│   ├── Automations.tsx # Automation workflows
│   ├── Integrations.tsx # Integration settings
│   └── Header.tsx      # Navigation header
├── services/           # API services
│   └── geminiService.ts # Gemini AI integration
├── public/             # Static assets
├── App.tsx             # Main app component
├── types.ts            # TypeScript types
└── index.tsx           # App entry point
```

## Available Scripts

- `npm run dev` - Start development server (http://localhost:5173)
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

## Connecting to Backend

The frontend expects the backend API to be running on `http://localhost:8000` by default. Update `VITE_API_URL` in your `.env` file to point to your backend.

### Expected API Endpoints

- `POST /api/analyze-dispute` - Analyze dispute transcripts
- `GET /api/disputes` - Fetch all disputes
- `GET /api/metrics` - Get KPI metrics
- `POST /api/agent/configure` - Configure voice agents

## Deployment

### Vercel
```bash
vercel deploy
```

### Build Output
The `dist/` directory contains the production build and can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

## Notes

- The app uses `.npmrc` with `legacy-peer-deps=true` to handle React 19 compatibility with react-simple-maps
- Mock data is currently used in `App.tsx` - replace with API calls once backend is connected
