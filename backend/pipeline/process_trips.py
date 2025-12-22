"""
Processing Pipeline
Connects all 4 algorithms and generates output files for the dashboard
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import algorithms
sys.path.append(str(Path(__file__).parent.parent))

from algorithms.load_classifier import analyze_trip_load
from algorithms.acceleration_detector import analyze_trip_acceleration
from algorithms.fuel_estimator import estimate_trip_fuel
from algorithms.savings_calculator import (
    calculate_trip_savings,
    calculate_fleet_savings,
    project_fleet_wide_impact
)


def load_trip_data():
    """Load trip data from data_simulator output"""
    
    data_file = Path(__file__).parent.parent / "output" / "route_12_trips.json"
    
    if not data_file.exists():
        print("❌ Error: route_12_trips.json not found!")
        print("   Run data_simulator.py first: python3 backend/pipeline/data_simulator.py")
        return None
    
    with open(data_file, 'r') as f:
        trips = json.load(f)
    
    print(f"✅ Loaded {len(trips)} trips from {data_file.name}")
    return trips


def process_single_trip(trip_data):
    """
    Process a single trip through all 4 algorithms
    
    Args:
        trip_data (dict): Raw trip data
    
    Returns:
        dict: Complete analysis results
    """
    
    # Algorithm 1: Load Classification
    load_analysis = analyze_trip_load(trip_data)
    
    # Algorithm 2: Acceleration Detection
    accel_analysis = analyze_trip_acceleration(trip_data)
    
    # Algorithm 3: Fuel Estimation
    fuel_estimation = estimate_trip_fuel(trip_data, load_analysis, accel_analysis)
    
    # Algorithm 4: Savings Calculation
    savings_analysis = calculate_trip_savings(fuel_estimation)
    
    return {
        'trip_id': trip_data['trip_id'],
        'bus_id': trip_data['bus_id'],
        'driver_id': trip_data['driver_id'],
        'date': trip_data['date'],
        'is_peak': trip_data['is_peak'],
        'load': load_analysis,
        'acceleration': accel_analysis,
        'fuel': fuel_estimation,
        'savings': savings_analysis
    }


def aggregate_fleet_statistics(processed_trips):
    """
    Aggregate all trip data into fleet-wide statistics
    
    Args:
        processed_trips (list): List of processed trip results
    
    Returns:
        dict: Fleet summary statistics
    """
    
    total_trips = len(processed_trips)
    
    # Categorize by load
    load_categories = {'LIGHT': [], 'MEDIUM': [], 'HEAVY': []}
    for trip in processed_trips:
        category = trip['load']['dominant_load_category']
        load_categories[category].append(trip)
    
    # Calculate fuel stats by load category
    fuel_by_load = {}
    for load_cat, trips in load_categories.items():
        if trips:
            fuel_rates = [t['fuel']['avg_fuel_per_km'] for t in trips]
            avg_fuel = sum(fuel_rates) / len(fuel_rates)
            total_fuel = sum(t['fuel']['total_fuel_liters'] for t in trips)
            
            fuel_by_load[load_cat] = {
                'count': len(trips),
                'percentage': round((len(trips) / total_trips) * 100, 1),
                'avg_fuel_per_km': round(avg_fuel, 3),
                'total_fuel': round(total_fuel, 1)
            }
    
    # Calculate savings opportunity
    all_savings = [t['savings'] for t in processed_trips if t['savings']['has_savings']]
    fleet_savings = calculate_fleet_savings(all_savings)
    
    # Fleet-wide projection
    projection = project_fleet_wide_impact(fleet_savings)
    
    return {
        'route': '12',
        'period': 'Week of Dec 16-20, 2024',
        'total_trips': total_trips,
        'by_load_category': fuel_by_load,
        'fleet_savings': fleet_savings,
        'sbs_fleet_projection': projection
    }


def create_manual_wasteful_scenario():
    """
    Create the KEY demo scenario manually: Heavy Load + Aggressive Acceleration
    This shows THE PROBLEM that our solution fixes
    """
    return {
        'trip_id': 'DEMO_HEAVY_WASTEFUL',
        'bus_id': 'SBS1238K',
        'driver_id': 'D007',
        'date': '2024-12-16',
        'is_peak': True,
        
        'load': {
            'trip_id': 'DEMO_HEAVY_WASTEFUL',
            'dominant_load_category': 'HEAVY',
            'max_passenger_count': 72,
            'avg_passenger_count': 65.3,
            'heavy_load_segments': 5,
            'total_segments': 9,
            'segments': [
                {'segment_id': 0, 'stop_name': 'Tampines Interchange', 'passenger_count': 45, 'load_category': 'MEDIUM', 'capacity_percentage': 53.6, 'total_weight_kg': 15150},
                {'segment_id': 1, 'stop_name': 'Tampines Ave 4', 'passenger_count': 58, 'load_category': 'MEDIUM', 'capacity_percentage': 69.0, 'total_weight_kg': 16060},
                {'segment_id': 2, 'stop_name': 'Simei MRT', 'passenger_count': 72, 'load_category': 'HEAVY', 'capacity_percentage': 85.7, 'total_weight_kg': 17040},
                {'segment_id': 3, 'stop_name': 'Bedok North', 'passenger_count': 70, 'load_category': 'HEAVY', 'capacity_percentage': 83.3, 'total_weight_kg': 16900},
                {'segment_id': 4, 'stop_name': 'Bedok Reservoir', 'passenger_count': 68, 'load_category': 'HEAVY', 'capacity_percentage': 81.0, 'total_weight_kg': 16760},
                {'segment_id': 5, 'stop_name': 'Bedok Interchange', 'passenger_count': 65, 'load_category': 'HEAVY', 'capacity_percentage': 77.4, 'total_weight_kg': 16550},
                {'segment_id': 6, 'stop_name': 'Bedok South', 'passenger_count': 63, 'load_category': 'HEAVY', 'capacity_percentage': 75.0, 'total_weight_kg': 16410},
                {'segment_id': 7, 'stop_name': 'Tanah Merah', 'passenger_count': 61, 'load_category': 'HEAVY', 'capacity_percentage': 72.6, 'total_weight_kg': 16270},
                {'segment_id': 8, 'stop_name': 'Siglap', 'passenger_count': 48, 'load_category': 'MEDIUM', 'capacity_percentage': 57.1, 'total_weight_kg': 15360}
            ]
        },
        
        'acceleration': {
            'trip_id': 'DEMO_HEAVY_WASTEFUL',
            'dominant_pattern': 'AGGRESSIVE',
            'avg_acceleration': 2.8,
            'max_acceleration': 3.2,
            'total_events': 15,
            'gentle_count': 2,
            'gentle_percentage': 13.3,
            'moderate_count': 3,
            'moderate_percentage': 20.0,
            'aggressive_count': 10,
            'aggressive_percentage': 66.7,
            'segments': [
                {'segment_id': 0, 'category': 'MODERATE', 'avg_acceleration': 2.1, 'max_acceleration': 2.4},
                {'segment_id': 1, 'category': 'AGGRESSIVE', 'avg_acceleration': 2.9, 'max_acceleration': 3.1},
                {'segment_id': 2, 'category': 'AGGRESSIVE', 'avg_acceleration': 3.1, 'max_acceleration': 3.2},
                {'segment_id': 3, 'category': 'AGGRESSIVE', 'avg_acceleration': 2.8, 'max_acceleration': 3.0},
                {'segment_id': 4, 'category': 'AGGRESSIVE', 'avg_acceleration': 3.0, 'max_acceleration': 3.2},
                {'segment_id': 5, 'category': 'AGGRESSIVE', 'avg_acceleration': 2.7, 'max_acceleration': 2.9},
                {'segment_id': 6, 'category': 'AGGRESSIVE', 'avg_acceleration': 2.9, 'max_acceleration': 3.1},
                {'segment_id': 7, 'category': 'MODERATE', 'avg_acceleration': 2.3, 'max_acceleration': 2.5},
                {'segment_id': 8, 'category': 'MODERATE', 'avg_acceleration': 2.0, 'max_acceleration': 2.2}
            ]
        },
        
        'fuel': {
            'trip_id': 'DEMO_HEAVY_WASTEFUL',
            'total_distance_km': 15.2,
            'total_fuel_liters': 16.82,
            'optimal_fuel_liters': 14.35,
            'wasted_fuel_liters': 2.47,
            'waste_percentage': 17.2,
            'avg_fuel_per_km': 1.107,
            'optimal_fuel_per_km': 0.944,
            'total_cost_sgd': 25.23,
            'wasted_cost_sgd': 3.71,
            'problem_segments': 5,
            'segments': [
                {'segment_id': 0, 'load_category': 'MEDIUM', 'accel_category': 'MODERATE', 'distance_km': 1.69, 'fuel_rate_per_km': 0.920, 'total_fuel_liters': 1.55, 'optimal_fuel_liters': 1.49, 'excess_fuel_liters': 0.06},
                {'segment_id': 1, 'load_category': 'MEDIUM', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 0.945, 'total_fuel_liters': 1.60, 'optimal_fuel_liters': 1.49, 'excess_fuel_liters': 0.11},
                {'segment_id': 2, 'load_category': 'HEAVY', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.150, 'total_fuel_liters': 1.94, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.29},
                {'segment_id': 3, 'load_category': 'HEAVY', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.150, 'total_fuel_liters': 1.94, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.29},
                {'segment_id': 4, 'load_category': 'HEAVY', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.150, 'total_fuel_liters': 1.94, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.29},
                {'segment_id': 5, 'load_category': 'HEAVY', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.150, 'total_fuel_liters': 1.94, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.29},
                {'segment_id': 6, 'load_category': 'HEAVY', 'accel_category': 'AGGRESSIVE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.150, 'total_fuel_liters': 1.94, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.29},
                {'segment_id': 7, 'load_category': 'HEAVY', 'accel_category': 'MODERATE', 'distance_km': 1.69, 'fuel_rate_per_km': 1.050, 'total_fuel_liters': 1.77, 'optimal_fuel_liters': 1.66, 'excess_fuel_liters': 0.12},
                {'segment_id': 8, 'load_category': 'MEDIUM', 'accel_category': 'MODERATE', 'distance_km': 1.69, 'fuel_rate_per_km': 0.920, 'total_fuel_liters': 1.55, 'optimal_fuel_liters': 1.49, 'excess_fuel_liters': 0.06}
            ]
        },
        
        'savings': {
            'trip_id': 'DEMO_HEAVY_WASTEFUL',
            'has_savings': True,
            'total_wasted_fuel': 2.47,
            'total_wasted_cost': 3.71,
            'waste_percentage': 17.2,
            'heavy_aggressive_segments': 5,
            'heavy_aggressive_waste': 1.44,
            'priority': 'CRITICAL',
            'main_issue': '5 segments with HEAVY load (>60 passengers) + AGGRESSIVE acceleration',
            'main_action': 'Use GENTLE acceleration when passenger count exceeds 60',
            'segments': [
                {'segment_id': 0, 'stop_name': 'Tampines Interchange', 'has_savings_potential': True, 'wasted_fuel': 0.06, 'wasted_cost': 0.09, 'priority': 'LOW'},
                {'segment_id': 1, 'stop_name': 'Tampines Ave 4', 'has_savings_potential': True, 'wasted_fuel': 0.11, 'wasted_cost': 0.17, 'priority': 'MEDIUM'},
                {'segment_id': 2, 'stop_name': 'Simei MRT', 'has_savings_potential': True, 'wasted_fuel': 0.29, 'wasted_cost': 0.43, 'priority': 'CRITICAL'},
                {'segment_id': 3, 'stop_name': 'Bedok North', 'has_savings_potential': True, 'wasted_fuel': 0.29, 'wasted_cost': 0.43, 'priority': 'CRITICAL'},
                {'segment_id': 4, 'stop_name': 'Bedok Reservoir', 'has_savings_potential': True, 'wasted_fuel': 0.29, 'wasted_cost': 0.43, 'priority': 'CRITICAL'},
                {'segment_id': 5, 'stop_name': 'Bedok Interchange', 'has_savings_potential': True, 'wasted_fuel': 0.29, 'wasted_cost': 0.43, 'priority': 'CRITICAL'},
                {'segment_id': 6, 'stop_name': 'Bedok South', 'has_savings_potential': True, 'wasted_fuel': 0.29, 'wasted_cost': 0.43, 'priority': 'CRITICAL'},
                {'segment_id': 7, 'stop_name': 'Tanah Merah', 'has_savings_potential': True, 'wasted_fuel': 0.12, 'wasted_cost': 0.18, 'priority': 'HIGH'},
                {'segment_id': 8, 'stop_name': 'Siglap', 'has_savings_potential': True, 'wasted_fuel': 0.06, 'wasted_cost': 0.09, 'priority': 'LOW'}
            ]
        }
    }


def generate_demo_scenarios(processed_trips):
    """
    Extract specific demo scenarios from processed trips
    If not found naturally, create them manually
    
    Args:
        processed_trips (list): All processed trips
    
    Returns:
        dict: Demo scenarios
    """
    
    scenarios = {
        'light_load_optimal': None,
        'heavy_load_optimal': None,
        'heavy_load_wasteful': None
    }
    
    # Try to find scenarios naturally first
    for trip in processed_trips:
        load_cat = trip['load']['dominant_load_category']
        accel_pat = trip['acceleration']['dominant_pattern']
        
        # Light load scenario
        if not scenarios['light_load_optimal'] and load_cat == 'LIGHT':
            scenarios['light_load_optimal'] = trip
        
        # Heavy load, gentle (optimal)
        if not scenarios['heavy_load_optimal'] and load_cat == 'HEAVY' and accel_pat == 'GENTLE':
            scenarios['heavy_load_optimal'] = trip
        
        # Heavy load, aggressive (wasteful) - THE PROBLEM
        if not scenarios['heavy_load_wasteful'] and load_cat == 'HEAVY' and accel_pat == 'AGGRESSIVE':
            scenarios['heavy_load_wasteful'] = trip
        
        # Stop if we found all scenarios
        if all(scenarios.values()):
            break
    
    # If we didn't find heavy_load_wasteful, create it manually
    if not scenarios['heavy_load_wasteful']:
        print("  ⚠️ No heavy+aggressive trip found in data - creating manual scenario")
        scenarios['heavy_load_wasteful'] = create_manual_wasteful_scenario()
    
    return scenarios


def save_output(data, filename):
    """Save data to output folder"""
    
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved: {filepath.name}")
    return filepath


def main():
    """Main processing pipeline"""
    
    print("\n" + "=" * 60)
    print("🚌 PROJECTBUS PROCESSING PIPELINE")
    print("=" * 60)
    print("\nStep 1: Load trip data")
    print("-" * 60)
    
    # Load data
    trips = load_trip_data()
    if not trips:
        return
    
    print(f"\nStep 2: Process trips through 4 algorithms")
    print("-" * 60)
    
    # Process all trips
    processed_trips = []
    
    for i, trip in enumerate(trips, 1):
        if i % 50 == 0:  # Progress indicator every 50 trips
            print(f"  Processing trip {i}/{len(trips)}...")
        
        try:
            result = process_single_trip(trip)
            processed_trips.append(result)
        except Exception as e:
            print(f"  ⚠️ Error processing trip {trip['trip_id']}: {e}")
            continue
    
    print(f"✅ Successfully processed {len(processed_trips)}/{len(trips)} trips")
    
    print(f"\nStep 3: Aggregate fleet statistics")
    print("-" * 60)
    
    # Generate fleet statistics
    fleet_stats = aggregate_fleet_statistics(processed_trips)
    
    print(f"\n📊 Fleet Summary:")
    print(f"  Total trips: {fleet_stats['total_trips']}")
    print(f"  By load category:")
    for load_cat, stats in fleet_stats['by_load_category'].items():
        print(f"    {load_cat}: {stats['count']} trips ({stats['percentage']}%) - Avg: {stats['avg_fuel_per_km']} L/km")
    
    print(f"\n  💰 Savings Opportunity:")
    savings = fleet_stats['fleet_savings']
    print(f"    Weekly waste: {savings['weekly_fuel_waste']} L (${savings['weekly_cost_waste']})")
    print(f"    Annual (Route 12): ${savings['annual_cost_waste']:,.0f}")
    
    projection = fleet_stats['sbs_fleet_projection']
    print(f"    Fleet-wide projection: ${projection['projected_annual_cost_waste']:,.0f}")
    
    print(f"\nStep 4: Generate demo scenarios")
    print("-" * 60)
    
    # Extract demo scenarios
    scenarios = generate_demo_scenarios(processed_trips)
    
    for scenario_name, trip in scenarios.items():
        if trip:
            print(f"  ✅ {scenario_name}: Trip {trip['trip_id']}")
    
    print(f"\nStep 5: Save output files")
    print("-" * 60)
    
    # Save all outputs
    save_output(fleet_stats, 'fleet_weekly_stats.json')
    save_output(processed_trips, 'all_trips_processed.json')
    
    # Save demo scenarios
    if scenarios['light_load_optimal']:
        save_output(scenarios['light_load_optimal'], 'scenario_light_load.json')
    
    if scenarios['heavy_load_optimal']:
        save_output(scenarios['heavy_load_optimal'], 'scenario_heavy_optimal.json')
    
    if scenarios['heavy_load_wasteful']:
        save_output(scenarios['heavy_load_wasteful'], 'scenario_heavy_wasteful.json')
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Output files ready in: backend/output/")
    print(f"\n🎯 Next steps:")
    print(f"   1. Copy JSON files to frontend: cp backend/output/*.json frontend/public/data/")
    print(f"   2. Modify Figma components to load these JSON files")
    print(f"   3. Test frontend: cd frontend && npm run dev")
    print("\n")


if __name__ == "__main__":
    main()