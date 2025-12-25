# ProjectBus Documentation

This folder contains the full documentation set for the ProjectBus codebase.

## Quick links
- Architecture overview and diagrams: ARCHITECTURE.md
- Backend algorithms and pipeline: BACKEND.md
- Frontend UI and data flow: FRONTEND.md
- Data model and JSON outputs: DATA.md
- Runbooks and guides: GUIDES.md

## What this project does
ProjectBus is a prototype that analyzes bus passenger load and acceleration behavior to estimate fuel waste and recommend gentler driving. It includes:
- A Python pipeline that simulates trips, runs four algorithms, and emits JSON outputs.
- A React (Vite + TypeScript) frontend that renders dashboards and a driver display from JSON.

## Codebase layout (high level)
- backend/ algorithms and pipeline scripts
- frontend/ React UI prototype and demo data
- docs/ architecture, guides, and data references

