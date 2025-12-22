"""
Data Simulator for ProjectBus
Generates realistic Route 12 bus trip data for testing algorithms
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Constants
ROUTE_12_STOPS = [
    {"id": "S001", "name": "Tampines Interchange", "position_km": 0.0},
    {"id": "S002", "name": "Tampines Ave 4", "position_km": 1.2},
    {"id": "S003", "name": "Simei MRT", "position_km": 2.8},
    {"id": "S004", "name": "Bedok North", "position_km": 4.5},
    {"id": "S005", "name": "Bedok Reservoir", "position_km": 6.2},
    {"id": "S006", "name": "Bedok Interchange", "position_km": 8.0},
    {"id": "S007", "name": "Bedok South", "position_km": 9.5},
    {"id": "S008", "name": "Tanah Merah", "position_km": 11.2},
    {"id": "S009", "name": "Siglap", "position_km": 13.0},
    {"id": "S010", "name": "Marine Parade", "position_km": 15.2},
]

BUS_CAPACITY = 84
ROUTE_LENGTH_KM = 15.2
NUM_BUSES = 10
TRIPS_PER_BUS_PER_DAY = 6  # ~420 trips per week


def generate_passenger_load(stop_index, time_of_day, is_peak):
    """Generate realistic passenger boarding/alighting based on stop and time"""
    
    # Peak hours: 7-9 AM, 5-7 PM
    if is_peak:
        if stop_index <= 2:  # Tampines/Simei area (morning peak - boarding)
            boarding = random.randint(15, 35)
            alighting = random.randint(0, 5)
        elif stop_index == 5:  # Bedok Interchange (major hub)
            boarding = random.randint(20, 40)
            alighting = random.randint(10, 25)
        elif stop_index >= 8:  # Marine Parade area (evening peak - alighting)
            boarding = random.randint(5, 15)
            alighting = random.randint(15, 30)
        else:
            boarding = random.randint(8, 20)
            alighting = random.randint(5, 15)
    else:  # Off-peak
        boarding = random.randint(2, 10)
        alighting = random.randint(2, 8)
    
    return boarding, alighting


def generate_speed_profile(acceleration_style, segment_distance_km):
    """Generate GPS speed samples for a segment based on acceleration style"""
    
    # Acceleration profiles (time to reach max speed)
    if acceleration_style == "GENTLE":
        accel_time_sec = 25
        max_speed_kmh = 45
    elif acceleration_style == "MODERATE":
        accel_time_sec = 15
        max_speed_kmh = 50
    else:  # AGGRESSIVE
        accel_time_sec = 10
        max_speed_kmh = 55
    
    speeds = []
    timestamps = []
    
    # Start from stop (speed = 0)
    current_time = 0
    speeds.append(0)
    timestamps.append(current_time)
    
    # Acceleration phase (0 to max speed)
    num_accel_samples = accel_time_sec // 5  # Sample every 5 seconds
    for i in range(1, num_accel_samples + 1):
        speed = (max_speed_kmh / num_accel_samples) * i
        current_time += 5
        speeds.append(round(speed, 1))
        timestamps.append(current_time)
    
    # Cruising phase (maintain speed)
    cruise_distance = segment_distance_km * 0.6  # 60% of segment at max speed
    cruise_time_sec = (cruise_distance / max_speed_kmh) * 3600
    num_cruise_samples = int(cruise_time_sec // 5)
    
    for _ in range(num_cruise_samples):
        current_time += 5
        speeds.append(max_speed_kmh)
        timestamps.append(current_time)
    
    # Deceleration phase (max speed to 0)
    num_decel_samples = 4  # Slower deceleration
    for i in range(num_decel_samples, 0, -1):
        speed = (max_speed_kmh / num_decel_samples) * i
        current_time += 5
        speeds.append(round(speed, 1))
        timestamps.append(current_time)
    
    # Final stop
    current_time += 5
    speeds.append(0)
    timestamps.append(current_time)
    
    return speeds, timestamps


def determine_acceleration_style(passenger_load, driver_behavior):
    """Determine acceleration style based on load and driver behavior"""
    
    # Some drivers always drive gently, some are aggressive
    if driver_behavior == "gentle":
        return "GENTLE"
    elif driver_behavior == "aggressive":
        # Even aggressive drivers should be gentler with heavy loads (but many don't)
        if passenger_load > 60 and random.random() > 0.6:  # 40% still aggressive
            return "AGGRESSIVE"
        else:
            return "MODERATE"
    else:  # "moderate"
        if passenger_load > 60 and random.random() > 0.7:  # 30% use gentle
            return "GENTLE"
        else:
            return "MODERATE"


def generate_trip(bus_id, driver_id, trip_num, date, start_hour):
    """Generate a complete trip with passenger data and GPS speeds"""
    
    # Determine if peak hour
    is_peak = (7 <= start_hour <= 9) or (17 <= start_hour <= 19)
    
    # Assign driver behavior (consistent per driver)
    driver_behaviors = {
        "D001": "gentle",
        "D002": "gentle", 
        "D003": "moderate",
        "D004": "moderate",
        "D005": "moderate",
        "D006": "moderate",
        "D007": "aggressive",
        "D008": "aggressive",
        "D009": "moderate",
        "D010": "gentle",
    }
    driver_behavior = driver_behaviors.get(driver_id, "moderate")
    
    # Generate trip
    trip_id = f"T{date.strftime('%Y%m%d')}{bus_id[-3:]}{trip_num:02d}"
    
    passenger_events = []
    speed_data = []
    current_passengers = 0
    total_distance = 0
    
    # Process each stop
    for i, stop in enumerate(ROUTE_12_STOPS):
        # Passenger boarding/alighting
        if i == 0:
            boarding, alighting = generate_passenger_load(i, start_hour, is_peak)
            alighting = 0  # First stop, no one alights
        else:
            boarding, alighting = generate_passenger_load(i, start_hour, is_peak)
            alighting = min(alighting, current_passengers)  # Can't alight more than onboard
        
        current_passengers = max(0, current_passengers + boarding - alighting)
        current_passengers = min(current_passengers, BUS_CAPACITY)  # Cap at capacity
        
        passenger_events.append({
            "stop_id": stop["id"],
            "stop_name": stop["name"],
            "boarding": boarding,
            "alighting": alighting,
            "total_onboard": current_passengers
        })
        
        # Generate speed data for segment to next stop
        if i < len(ROUTE_12_STOPS) - 1:
            segment_distance = ROUTE_12_STOPS[i + 1]["position_km"] - stop["position_km"]
            
            # Determine acceleration style for this segment
            accel_style = determine_acceleration_style(current_passengers, driver_behavior)
            
            speeds, timestamps = generate_speed_profile(accel_style, segment_distance)
            
            # Add to speed data
            for speed, ts in zip(speeds, timestamps):
                speed_data.append({
                    "timestamp": ts,
                    "speed_kmh": speed,
                    "segment": i,
                    "passenger_load": current_passengers
                })
    
    return {
        "trip_id": trip_id,
        "bus_id": bus_id,
        "driver_id": driver_id,
        "route": "12",
        "date": date.strftime("%Y-%m-%d"),
        "start_time": f"{start_hour:02d}:00:00",
        "is_peak": is_peak,
        "total_distance_km": ROUTE_LENGTH_KM,
        "passenger_events": passenger_events,
        "speed_data": speed_data
    }


def generate_week_data():
    """Generate a full week of trip data for Route 12"""
    
    all_trips = []
    
    # Generate for Monday-Friday (5 days)
    start_date = datetime(2024, 12, 16)  # Monday
    
    for day in range(5):
        current_date = start_date + timedelta(days=day)
        
        # Each bus makes 6 trips per day
        for bus_num in range(1, NUM_BUSES + 1):
            bus_id = f"SBS{1234 + bus_num}K"
            driver_id = f"D{bus_num:03d}"
            
            # Trip times throughout the day
            trip_hours = [6, 9, 12, 15, 18, 21]
            
            for trip_num, hour in enumerate(trip_hours, 1):
                trip = generate_trip(bus_id, driver_id, trip_num, current_date, hour)
                all_trips.append(trip)
    
    return all_trips


def save_to_file(data, filename):
    """Save data to JSON file"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved: {filepath}")
    return filepath


def main():
    """Main function to generate all data"""
    
    print("🚌 ProjectBus Data Simulator")
    print("=" * 50)
    print(f"Generating trip data for Route 12...")
    print(f"- Buses: {NUM_BUSES}")
    print(f"- Days: 5 (Mon-Fri)")
    print(f"- Trips per bus per day: {TRIPS_PER_BUS_PER_DAY}")
    print(f"- Total trips: {NUM_BUSES * 5 * TRIPS_PER_BUS_PER_DAY}")
    print("=" * 50)
    
    # Generate all trips
    all_trips = generate_week_data()
    
    # Save raw trip data
    save_to_file(all_trips, "route_12_trips.json")
    
    # Generate summary statistics
    total_trips = len(all_trips)
    peak_trips = sum(1 for t in all_trips if t["is_peak"])
    off_peak_trips = total_trips - peak_trips
    
    # Count by load category
    light_load = 0
    medium_load = 0
    heavy_load = 0
    
    for trip in all_trips:
        max_load = max(event["total_onboard"] for event in trip["passenger_events"])
        if max_load <= 30:
            light_load += 1
        elif max_load <= 60:
            medium_load += 1
        else:
            heavy_load += 1
    
    summary = {
        "total_trips": total_trips,
        "peak_trips": peak_trips,
        "off_peak_trips": off_peak_trips,
        "light_load_trips": light_load,
        "medium_load_trips": medium_load,
        "heavy_load_trips": heavy_load,
        "route": "12",
        "period": "Week of Dec 16-20, 2024"
    }
    
    save_to_file(summary, "data_summary.json")
    
    print("\n📊 Summary:")
    print(f"  Total trips: {total_trips}")
    print(f"  Peak trips: {peak_trips} ({peak_trips/total_trips*100:.1f}%)")
    print(f"  Off-peak trips: {off_peak_trips} ({off_peak_trips/total_trips*100:.1f}%)")
    print(f"\n  Light load (<30 pax): {light_load} ({light_load/total_trips*100:.1f}%)")
    print(f"  Medium load (31-60): {medium_load} ({medium_load/total_trips*100:.1f}%)")
    print(f"  Heavy load (61+): {heavy_load} ({heavy_load/total_trips*100:.1f}%)")
    print("\n✅ Data generation complete!")
    print(f"📁 Files saved in: backend/output/")


if __name__ == "__main__":
    main()