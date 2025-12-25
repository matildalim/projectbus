# ProjectBus: Load-Adaptive Acceleration System

**SBS Transit Fuel Efficiency Optimization Solution**

## Problem
Bus drivers lack visibility into passenger load and its impact on fuel consumption. Heavy buses (61+ passengers) driven with aggressive acceleration waste **17% more fuel** than gentle acceleration, costing SBS Transit **$2.18M annually** fleet-wide.

## Solution
4-step algorithm system that:
1. **Classifies passenger load** (Light/Medium/Heavy)
2. **Detects acceleration patterns** (Gentle/Moderate/Aggressive)
3. **Estimates fuel consumption** with physics-based penalties
4. **Calculates savings potential** and provides driver guidance

## Key Insight
- Light load + Aggressive acceleration = 2% fuel penalty (negligible)
- Heavy load + Aggressive acceleration = **17% fuel penalty** (critical)

## Impact
- **Route 12:** 220L/week savings, $17K/year
- **Fleet-wide:** $2.18M/year potential
- **Uses existing infrastructure** (door sensors + GPS)

## Project Structure
```
projectbus-sbs/
├── frontend/          # Figma Make UI prototype (React + Vite)
│   ├── src/          # React components
│   └── public/data/  # Backend-generated JSON
│
└── backend/          # Python algorithms (core logic)
    ├── algorithms/   # 4 core algorithms
    ├── pipeline/     # Data processing
    └── output/       # Generated JSON files
```

## Documentation
- Docs index: `docs/README.md`
- Architecture and diagrams: `docs/ARCHITECTURE.md`
- Backend pipeline and algorithms: `docs/BACKEND.md`
- Frontend UI and data flow: `docs/FRONTEND.md`
- Data model and JSON outputs: `docs/DATA.md`
- Runbooks and guides: `docs/GUIDES.md`

## Tech Stack
- **Frontend:** React + TypeScript + Vite + Tailwind CSS
- **Backend:** Python 3.x
- **Data:** JSON (simulated SBS Transit data)

## Setup

### Frontend (Figma Make UI)
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Backend (Algorithms - Coming Soon)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python process_trips.py
```

## Demo Scenarios
1. **Light Load Trip** - Efficient (any acceleration OK)
2. **Heavy Load Optimal** - Gentle acceleration, 0.98 L/km
3. **Heavy Load Wasteful** - Aggressive acceleration, 1.15 L/km (17% penalty)

## Hackathon Context
Built for SBS Transit Hackathon 2025 - Problem Statement 4: Fuel Efficiency Optimization

**Team:** Matilda, Junming
**Date:** December 2025
