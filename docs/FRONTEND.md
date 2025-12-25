# Frontend

## Purpose
The frontend is a React + Vite prototype that renders two interfaces:
- Operations dashboard for fleet analysis
- Driver display for in-vehicle guidance

All data comes from static JSON files in `frontend/public/data/`.

## Entry points
- `frontend/src/main.tsx` mounts the React app and the `DataProvider`.
- `frontend/src/App.tsx` toggles between Operations and Driver views and controls demo scenarios.

## Data flow
- `frontend/src/context/DataContext.tsx` loads JSON based on `scenarioType`.
- For fleet view, it fetches `fleet_weekly_stats.json`.
- For single-trip scenarios, it fetches a scenario JSON and also pulls fleet stats for comparison.

## Main screens
- `frontend/src/components/operations-dashboard.tsx`
  - Header with quick stats and period.
  - 2x2 grid of panels: LoadImpactChart, AccelerationHeatmap, SavingsCard, DriverLeaderboard.
- `frontend/src/components/driver-display.tsx`
  - Single-screen kiosk layout with large guidance and status elements.
  - Demo-only controls to switch load level and acceleration.

## Charts and UI components
- `frontend/src/components/load-impact-chart.tsx` uses Recharts for bar comparison.
- `frontend/src/components/acceleration-heatmap.tsx` renders a semantic heatmap table.
- `frontend/src/components/savings-card.tsx` shows either fleet or trip-level savings.
- `frontend/src/components/driver-leaderboard.tsx` is a static sample leaderboard.

## Styling
- Tailwind CSS utilities drive layout and typography.
- Global tokens live in `frontend/src/styles/globals.css` and `frontend/src/index.css`.

## Running the frontend
```bash
cd frontend
npm install
npm run dev
```
Then open `http://localhost:5173`.

