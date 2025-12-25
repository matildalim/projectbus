# Guides

## Quickstart (frontend only)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`.

## Full pipeline refresh
```bash
python3 backend/pipeline/data_simulator.py
python3 backend/pipeline/process_trips.py
cp backend/output/*.json frontend/public/data/
```
Then run the frontend as above.

## Demo scenarios
Use the buttons in the app header to switch scenarios:
- Fleet View
- Light Load Trip
- Heavy Load (Optimal)
- Heavy Load (Wasteful)

These map to JSON files in `frontend/public/data/` and are loaded by `frontend/src/context/DataContext.tsx`.

## Troubleshooting
- If the UI shows "No data available", confirm JSON files exist in `frontend/public/data/`.
- If the backend pipeline fails, run the simulator first to generate `route_12_trips.json`.
- If charts render blank, check that `fleet_weekly_stats.json` has non-zero `by_load_category` data.

## Design iteration tips
- Most layout and typography decisions live in component class names under `frontend/src/components/`.
- Global tokens and default typography are in `frontend/src/styles/globals.css`.

