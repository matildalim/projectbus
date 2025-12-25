# Backend

## Purpose
The backend simulates bus trips, classifies load and acceleration patterns, estimates fuel usage, and computes cost savings. It emits JSON outputs consumed by the frontend.

## Key modules

### Pipeline
- `backend/pipeline/data_simulator.py`
  - Generates Route 12 trips with stops, boarding/alighting, and speed profiles.
  - Writes `backend/output/route_12_trips.json`.
- `backend/pipeline/process_trips.py`
  - Runs all four algorithms on each trip.
  - Aggregates fleet statistics and creates demo scenarios.
  - Writes JSON outputs for the frontend.

### Algorithms
- `backend/algorithms/load_classifier.py`
  - Classifies passenger load per segment and per trip (LIGHT, MEDIUM, HEAVY).
- `backend/algorithms/acceleration_detector.py`
  - Detects acceleration events from speed time-series data.
  - Classifies acceleration (GENTLE, MODERATE, AGGRESSIVE).
- `backend/algorithms/fuel_estimator.py`
  - Calculates fuel rates and penalties by load and acceleration.
  - Produces a per-segment and per-trip estimate.
- `backend/algorithms/savings_calculator.py`
  - Converts excess fuel to cost impact.
  - Builds trip-level and fleet-level recommendations.

## Outputs
- `backend/output/route_12_trips.json` (raw simulated trip inputs)
- `backend/output/all_trips_processed.json` (per-trip analysis results)
- `backend/output/fleet_weekly_stats.json` (fleet aggregates)
- `backend/output/scenario_light_load.json`
- `backend/output/scenario_heavy_optimal.json`
- `backend/output/scenario_heavy_wasteful.json`

## Running the pipeline
From the repo root:
```bash
python3 backend/pipeline/data_simulator.py
python3 backend/pipeline/process_trips.py
```
Then copy outputs for the frontend:
```bash
cp backend/output/*.json frontend/public/data/
```

## Algorithm notes
- Load thresholds: 0-30 (LIGHT), 31-60 (MEDIUM), 61+ (HEAVY).
- Acceleration thresholds: <1.5 m/s^2 (GENTLE), 1.5-2.5 (MODERATE), >2.5 (AGGRESSIVE).
- Fuel penalties are encoded in `backend/algorithms/fuel_estimator.py` and drive the 17.3% heavy+aggressive penalty.

