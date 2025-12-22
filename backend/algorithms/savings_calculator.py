"""
Savings Calculator Algorithm
Calculates fuel waste, cost impact, and generates recommendations
The final algorithm that quantifies the business case
"""

# Constants
FUEL_COST_SGD = 1.50  # SGD per liter
DAYS_PER_WEEK = 5
WEEKS_PER_YEAR = 52


def calculate_segment_savings(fuel_estimate):
    """
    Calculate savings potential for a single segment
    
    Args:
        fuel_estimate (dict): Output from fuel_estimator.estimate_segment_fuel
    
    Returns:
        dict: Savings analysis
    """
    
    excess_fuel = fuel_estimate['excess_fuel_liters']
    
    if excess_fuel <= 0:
        return {
            'has_savings_potential': False,
            'wasted_fuel': 0,
            'wasted_cost': 0,
            'recommendation': 'Already optimal'
        }
    
    wasted_cost = excess_fuel * FUEL_COST_SGD
    
    # Generate specific recommendation
    load = fuel_estimate['load_category']
    accel = fuel_estimate['accel_category']
    
    if load == 'HEAVY' and accel == 'AGGRESSIVE':
        priority = 'CRITICAL'
        action = f"CRITICAL: Heavy load ({load}) with aggressive acceleration wastes {fuel_estimate['penalty_percentage']}%. Use GENTLE acceleration immediately."
    elif load == 'HEAVY' and accel == 'MODERATE':
        priority = 'HIGH'
        action = f"Heavy load detected. Switch to GENTLE acceleration to eliminate {fuel_estimate['penalty_percentage']}% waste."
    elif load == 'MEDIUM' and accel == 'AGGRESSIVE':
        priority = 'MEDIUM'
        action = f"Medium load with aggressive acceleration. Use moderate or gentle acceleration."
    else:
        priority = 'LOW'
        action = f"Minor optimization possible. Consider gentler acceleration."
    
    return {
        'has_savings_potential': True,
        'wasted_fuel': round(excess_fuel, 3),
        'wasted_cost': round(wasted_cost, 2),
        'priority': priority,
        'recommendation': action
    }


def calculate_trip_savings(fuel_estimation):
    """
    Calculate total savings potential for a trip
    
    Args:
        fuel_estimation (dict): Output from fuel_estimator.estimate_trip_fuel
    
    Returns:
        dict: Complete trip savings analysis
    """
    
    total_waste = fuel_estimation.get('wasted_fuel_liters', 0)
    total_cost_waste = fuel_estimation.get('wasted_cost_sgd', 0)
    
    if total_waste <= 0:
        return {
            'trip_id': fuel_estimation['trip_id'],
            'has_savings': False,
            'total_wasted_fuel': 0,
            'total_wasted_cost': 0,
            'recommendation': 'Trip is already optimally driven'
        }
    
    # Analyze segments for specific issues
    segments = fuel_estimation.get('segments', [])
    segment_savings = []
    
    heavy_aggressive_count = 0
    heavy_aggressive_waste = 0
    
    for seg in segments:
        savings = calculate_segment_savings(seg)
        savings['segment_id'] = seg['segment_id']
        savings['stop_name'] = seg.get('stop_name', f"Stop {seg['segment_id']}")
        segment_savings.append(savings)
        
        # Track heavy + aggressive segments
        if seg['load_category'] == 'HEAVY' and seg['accel_category'] == 'AGGRESSIVE':
            heavy_aggressive_count += 1
            heavy_aggressive_waste += seg['excess_fuel_liters']
    
    # Generate overall recommendation
    if heavy_aggressive_count > 0:
        main_issue = f"{heavy_aggressive_count} segment(s) with HEAVY load + AGGRESSIVE acceleration"
        main_action = "Use GENTLE acceleration when passenger count exceeds 60"
        priority = 'CRITICAL'
    elif fuel_estimation.get('problem_segments', 0) > 0:
        main_issue = "Multiple segments with suboptimal load/acceleration combinations"
        main_action = "Adjust acceleration based on current passenger load"
        priority = 'HIGH'
    else:
        main_issue = "Minor inefficiencies across trip"
        main_action = "Generally use gentler acceleration"
        priority = 'MEDIUM'
    
    return {
        'trip_id': fuel_estimation['trip_id'],
        'has_savings': True,
        'total_wasted_fuel': round(total_waste, 2),
        'total_wasted_cost': round(total_cost_waste, 2),
        'waste_percentage': fuel_estimation.get('waste_percentage', 0),
        'heavy_aggressive_segments': heavy_aggressive_count,
        'heavy_aggressive_waste': round(heavy_aggressive_waste, 2),
        'priority': priority,
        'main_issue': main_issue,
        'main_action': main_action,
        'segments': segment_savings
    }


def calculate_fleet_savings(trip_savings_list):
    """
    Aggregate savings potential across entire fleet
    
    Args:
        trip_savings_list (list): List of trip savings analyses
    
    Returns:
        dict: Fleet-wide savings summary
    """
    
    total_trips = len(trip_savings_list)
    trips_with_waste = sum(1 for t in trip_savings_list if t['has_savings'])
    
    total_fuel_waste = sum(t.get('total_wasted_fuel', 0) for t in trip_savings_list)
    total_cost_waste = sum(t.get('total_wasted_cost', 0) for t in trip_savings_list)
    
    # Count by priority
    critical = sum(1 for t in trip_savings_list if t.get('priority') == 'CRITICAL')
    high = sum(1 for t in trip_savings_list if t.get('priority') == 'HIGH')
    medium = sum(1 for t in trip_savings_list if t.get('priority') == 'MEDIUM')
    
    # Count heavy + aggressive segments across fleet
    total_heavy_aggressive = sum(
        t.get('heavy_aggressive_segments', 0) for t in trip_savings_list
    )
    
    # Calculate per-week and per-year projections
    weekly_waste = total_fuel_waste
    weekly_cost = total_cost_waste
    
    annual_waste = weekly_waste * WEEKS_PER_YEAR
    annual_cost = weekly_cost * WEEKS_PER_YEAR
    
    return {
        'period': 'Weekly',
        'total_trips': total_trips,
        'trips_with_waste': trips_with_waste,
        'waste_percentage': round((trips_with_waste / total_trips * 100), 1) if total_trips > 0 else 0,
        'weekly_fuel_waste': round(weekly_waste, 1),
        'weekly_cost_waste': round(weekly_cost, 2),
        'annual_fuel_waste': round(annual_waste, 1),
        'annual_cost_waste': round(annual_cost, 2),
        'critical_trips': critical,
        'high_priority_trips': high,
        'medium_priority_trips': medium,
        'total_heavy_aggressive_segments': total_heavy_aggressive,
        'avg_waste_per_trip': round(total_fuel_waste / total_trips, 2) if total_trips > 0 else 0
    }


def project_fleet_wide_impact(route_savings, num_routes=127, num_buses=3300):
    """
    Project Route 12 savings to entire SBS Transit fleet
    
    Args:
        route_savings (dict): Fleet savings for Route 12
        num_routes (int): Total number of SBS routes
        num_buses (int): Total fleet size
    
    Returns:
        dict: Fleet-wide projection
    """
    
    # Conservative multiplier (not all routes same as Route 12)
    route_multiplier = num_routes * 0.8  # 80% of routes have similar patterns
    
    projected_annual_waste = route_savings['annual_fuel_waste'] * route_multiplier
    projected_annual_cost = route_savings['annual_cost_waste'] * route_multiplier
    
    return {
        'basis': f"Route 12 (Week of Dec 16-20, 2024)",
        'projection_method': f"Extrapolated to {num_routes} routes (80% applicability)",
        'total_fleet_buses': num_buses,
        'projected_annual_fuel_waste': round(projected_annual_waste, 0),
        'projected_annual_cost_waste': round(projected_annual_cost, 0),
        'cost_per_bus_per_year': round(projected_annual_cost / num_buses, 2),
        'savings_if_50pct_adoption': round(projected_annual_cost * 0.5, 0),
        'savings_if_80pct_adoption': round(projected_annual_cost * 0.8, 0)
    }


def generate_driver_report(driver_trips_savings):
    """
    Generate performance report for individual driver
    
    Args:
        driver_trips_savings (list): Savings analyses for driver's trips
    
    Returns:
        dict: Driver performance report
    """
    
    total_trips = len(driver_trips_savings)
    total_waste = sum(t.get('total_wasted_fuel', 0) for t in driver_trips_savings)
    total_cost_waste = sum(t.get('total_wasted_cost', 0) for t in driver_trips_savings)
    
    # Count problematic trips
    critical_trips = sum(1 for t in driver_trips_savings if t.get('priority') == 'CRITICAL')
    heavy_aggressive_segments = sum(
        t.get('heavy_aggressive_segments', 0) for t in driver_trips_savings
    )
    
    # Calculate weekly savings potential
    weekly_savings = round(total_cost_waste, 2)
    annual_savings = round(weekly_savings * WEEKS_PER_YEAR, 2)
    
    # Generate feedback
    if critical_trips > 0:
        feedback = f"⚠️ {critical_trips} trips with critical waste (Heavy load + Aggressive acceleration)"
        action = "Primary focus: Use GENTLE acceleration when passenger count >60"
        performance_level = "NEEDS IMPROVEMENT"
    elif total_waste > 5:
        feedback = f"Some inefficiency detected across {total_trips} trips"
        action = "Be more mindful of current passenger load when accelerating"
        performance_level = "FAIR"
    elif total_waste > 2:
        feedback = "Minor optimization opportunities"
        action = "Continue current practices, small improvements possible"
        performance_level = "GOOD"
    else:
        feedback = "Excellent fuel-efficient driving!"
        action = "Maintain current practices"
        performance_level = "EXCELLENT"
    
    return {
        'total_trips': total_trips,
        'total_fuel_wasted': round(total_waste, 2),
        'total_cost_wasted': round(total_cost_waste, 2),
        'weekly_savings_potential': weekly_savings,
        'annual_savings_potential': annual_savings,
        'critical_trips': critical_trips,
        'heavy_aggressive_segments': heavy_aggressive_segments,
        'performance_level': performance_level,
        'feedback': feedback,
        'recommended_action': action
    }


# Test function
def test_calculator():
    """Test the savings calculator"""
    
    print("🧪 Testing Savings Calculator\n")
    
    # Test 1: Single segment savings
    print("Test 1: Segment savings calculation")
    sample_segment = {
        'segment_id': 0,  # ← Added this
        'stop_name': 'Bedok',  # ← Added this
        'load_category': 'HEAVY',
        'accel_category': 'AGGRESSIVE',
        'distance_km': 1.5,
        'total_fuel_liters': 1.726,
        'optimal_fuel_liters': 1.470,
        'excess_fuel_liters': 0.256,
        'penalty_percentage': 17.3
    }
    
    savings = calculate_segment_savings(sample_segment)
    print(f"  Heavy + Aggressive, 1.5 km:")
    print(f"    Wasted: {savings['wasted_fuel']} L (${savings['wasted_cost']})")
    print(f"    Priority: {savings['priority']}")
    print(f"    Action: {savings['recommendation']}")
    print()
    
    # Test 2: Trip savings
    print("Test 2: Trip savings calculation")
    
    # Create segments with proper IDs
    sample_segments = []
    for i in range(3):
        seg = sample_segment.copy()
        seg['segment_id'] = i
        seg['stop_name'] = f'Stop {i}'
        sample_segments.append(seg)
    
    sample_trip_fuel = {
        'trip_id': 'T001',
        'total_fuel_liters': 16.47,
        'optimal_fuel_liters': 15.39,
        'wasted_fuel_liters': 1.08,
        'wasted_cost_sgd': 1.62,
        'waste_percentage': 7.0,
        'problem_segments': 1,
        'segments': sample_segments  # ← Fixed
    }
    
    trip_savings = calculate_trip_savings(sample_trip_fuel)
    print(f"Trip {trip_savings['trip_id']}:")
    print(f"  Total Waste: {trip_savings['total_wasted_fuel']} L (${trip_savings['total_wasted_cost']})")
    print(f"  Priority: {trip_savings['priority']}")
    print(f"  Issue: {trip_savings['main_issue']}")
    print(f"  Action: {trip_savings['main_action']}")
    print()
    
    # Test 3: Fleet savings
    print("Test 3: Fleet savings projection")
    fleet_trips = [trip_savings] * 300  # 300 trips
    
    fleet_savings = calculate_fleet_savings(fleet_trips)
    print(f"Fleet Summary ({fleet_savings['total_trips']} trips):")
    print(f"  Weekly Waste: {fleet_savings['weekly_fuel_waste']} L")
    print(f"  Weekly Cost: ${fleet_savings['weekly_cost_waste']} SGD")
    print(f"  Annual Waste: {fleet_savings['annual_fuel_waste']} L")
    print(f"  Annual Cost: ${fleet_savings['annual_cost_waste']} SGD")
    print(f"  Critical Trips: {fleet_savings['critical_trips']}")
    print()
    
    # Test 4: Fleet-wide projection
    print("Test 4: SBS Transit fleet-wide projection")
    projection = project_fleet_wide_impact(fleet_savings)
    print(f"  Projected Annual Fleet Waste: {projection['projected_annual_fuel_waste']:,.0f} L")
    print(f"  Projected Annual Cost: ${projection['projected_annual_cost_waste']:,.0f} SGD")
    print(f"  Cost per bus per year: ${projection['cost_per_bus_per_year']} SGD")
    print(f"  Savings at 50% adoption: ${projection['savings_if_50pct_adoption']:,.0f} SGD")
    print(f"  Savings at 80% adoption: ${projection['savings_if_80pct_adoption']:,.0f} SGD")
    print()
    
    # Test 5: Driver report
    print("Test 5: Driver performance report")
    driver_report = generate_driver_report([trip_savings] * 6)  # 6 trips
    print(f"  Performance: {driver_report['performance_level']}")
    print(f"  Weekly Savings Potential: ${driver_report['weekly_savings_potential']}")
    print(f"  Annual Savings Potential: ${driver_report['annual_savings_potential']}")
    print(f"  Feedback: {driver_report['feedback']}")
    print(f"  Action: {driver_report['recommended_action']}")
    
    print("\n✅ Savings Calculator Test Complete!")
    print("\n💰 This algorithm quantifies the business case for your solution!")


if __name__ == "__main__":
    test_calculator()