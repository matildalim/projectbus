# Backend: ProjectBus Algorithms

## Overview
Python implementation of 4 core algorithms that analyze bus trips and calculate fuel optimization opportunities.

## Algorithms

### 1. Load Classifier
- **Input:** Passenger count
- **Output:** Light (0-30) / Medium (31-60) / Heavy (61+)
- **Logic:** Simple threshold-based classification

### 2. Acceleration Detector
- **Input:** GPS speed time-series
- **Output:** Gentle (<1.5 m/s²) / Moderate / Aggressive (>2.5 m/s²)
- **Logic:** Calculate speed changes over time

### 3. Fuel Estimator
- **Input:** Load category + Acceleration pattern
- **Output:** Fuel consumption (L/km)
- **Logic:** Physics-based lookup table with penalties
  - Heavy load + Aggressive = 17% penalty
  - Medium load + Aggressive = 7% penalty
  - Light load + Aggressive = 2% penalty

### 4. Savings Calculator
- **Input:** Actual fuel vs Optimal fuel
- **Output:** Waste (liters, SGD, percentage)
- **Logic:** Subtraction + cost calculation

## Data Flow
```
Raw Trip Data → Load Classifier → Acceleration Detector → Fuel Estimator → Savings Calculator → JSON Output
```

## Output Files
- `fleet_weekly_stats.json` - Fleet-wide analytics for operations dashboard
- `scenario_light.json` - Light load demo trip
- `scenario_heavy_optimal.json` - Heavy load with gentle acceleration
- `scenario_heavy_wasteful.json` - Heavy load with aggressive acceleration (the problem)

## Coming Soon
- [ ] Data simulator
- [ ] Algorithm implementations
- [ ] Processing pipeline
- [ ] Demo scenarios
```

---

### **4.3: Create .gitignore**

1. Right-click root folder `projectbus-sbs/`
2. **New File** → `.gitignore`

**Add this content:**
```
# Frontend (Node.js)
frontend/node_modules/
frontend/dist/
frontend/.env
frontend/.vite/

# Backend (Python)
backend/__pycache__/
backend/*.pyc
backend/.env
backend/venv/
backend/.venv/
backend/*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Output files (optional - uncomment to exclude from git)
# backend/output/*.json