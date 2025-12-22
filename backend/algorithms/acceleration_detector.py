"""
Acceleration Detector Algorithm
Analyzes GPS speed data to detect acceleration patterns
Classifies as Gentle/Moderate/Aggressive
"""

# Acceleration thresholds (m/s²)
GENTLE_THRESHOLD = 1.5
MODERATE_THRESHOLD = 2.5

# Conversion constant
KMH_TO_MS = 3.6  # Divide km/h by 3.6 to get m/s


def calculate_acceleration(speed_start_kmh, speed_end_kmh, time_delta_sec):
    """
    Calculate acceleration between two speed measurements
    
    Args:
        speed_start_kmh (float): Starting speed in km/h
        speed_end_kmh (float): Ending speed in km/h
        time_delta_sec (float): Time difference in seconds
    
    Returns:
        float: Acceleration in m/s²
    """
    
    if time_delta_sec == 0:
        return 0.0
    
    # Convert speeds to m/s
    speed_start_ms = speed_start_kmh / KMH_TO_MS
    speed_end_ms = speed_end_kmh / KMH_TO_MS
    
    # Calculate acceleration: (v_final - v_initial) / time
    acceleration = (speed_end_ms - speed_start_ms) / time_delta_sec
    
    return acceleration


def classify_acceleration(accel_ms2):
    """
    Classify acceleration rate
    
    Args:
        accel_ms2 (float): Acceleration in m/s²
    
    Returns:
        str: 'GENTLE' | 'MODERATE' | 'AGGRESSIVE'
    """
    
    if accel_ms2 < GENTLE_THRESHOLD:
        return "GENTLE"
    elif accel_ms2 < MODERATE_THRESHOLD:
        return "MODERATE"
    else:
        return "AGGRESSIVE"


def detect_acceleration_events(speed_data):
    """
    Detect all acceleration events from speed time-series data
    
    Args:
        speed_data (list): List of speed samples
            Each sample: {'timestamp': int, 'speed_kmh': float, 'segment': int}
    
    Returns:
        list: Acceleration events with classifications
    """
    
    events = []
    
    # Process consecutive speed samples
    for i in range(len(speed_data) - 1):
        current = speed_data[i]
        next_sample = speed_data[i + 1]
        
        # Calculate time delta
        time_delta = next_sample['timestamp'] - current['timestamp']
        
        if time_delta <= 0:
            continue
        
        # Calculate acceleration
        accel = calculate_acceleration(
            current['speed_kmh'],
            next_sample['speed_kmh'],
            time_delta
        )
        
        # Only track positive accelerations (speeding up, not braking)
        if accel > 0.1:  # Threshold to filter out noise
            event = {
                'start_time': current['timestamp'],
                'end_time': next_sample['timestamp'],
                'start_speed_kmh': current['speed_kmh'],
                'end_speed_kmh': next_sample['speed_kmh'],
                'acceleration_ms2': round(accel, 2),
                'category': classify_acceleration(accel),
                'segment': current.get('segment', 0)
            }
            events.append(event)
    
    return events


def analyze_segment_acceleration(speed_data, segment_id):
    """
    Analyze acceleration pattern for a specific segment
    
    Args:
        speed_data (list): Speed samples for the trip
        segment_id (int): Segment number to analyze
    
    Returns:
        dict: Acceleration analysis for the segment
    """
    
    # Filter speed data for this segment
    segment_speeds = [s for s in speed_data if s.get('segment') == segment_id]
    
    if len(segment_speeds) < 2:
        return {
            'segment_id': segment_id,
            'category': 'UNKNOWN',
            'avg_acceleration': 0,
            'max_acceleration': 0,
            'acceleration_events': []
        }
    
    # Detect acceleration events in this segment
    events = detect_acceleration_events(segment_speeds)
    
    if not events:
        return {
            'segment_id': segment_id,
            'category': 'GENTLE',
            'avg_acceleration': 0,
            'max_acceleration': 0,
            'acceleration_events': []
        }
    
    # Calculate statistics
    accelerations = [e['acceleration_ms2'] for e in events]
    avg_accel = sum(accelerations) / len(accelerations)
    max_accel = max(accelerations)
    
    # Count by category
    gentle = sum(1 for e in events if e['category'] == 'GENTLE')
    moderate = sum(1 for e in events if e['category'] == 'MODERATE')
    aggressive = sum(1 for e in events if e['category'] == 'AGGRESSIVE')
    
    # Determine dominant category for segment
    if aggressive > 0:
        dominant_category = 'AGGRESSIVE'
    elif moderate > gentle:
        dominant_category = 'MODERATE'
    else:
        dominant_category = 'GENTLE'
    
    return {
        'segment_id': segment_id,
        'category': dominant_category,
        'avg_acceleration': round(avg_accel, 2),
        'max_acceleration': round(max_accel, 2),
        'total_events': len(events),
        'gentle_count': gentle,
        'moderate_count': moderate,
        'aggressive_count': aggressive,
        'acceleration_events': events
    }


def analyze_trip_acceleration(trip_data):
    """
    Complete acceleration analysis for entire trip
    
    Args:
        trip_data (dict): Trip data with speed_data
    
    Returns:
        dict: Complete acceleration analysis
    """
    
    speed_data = trip_data.get('speed_data', [])
    
    if not speed_data:
        return {
            'trip_id': trip_data['trip_id'],
            'dominant_pattern': 'UNKNOWN',
            'error': 'No speed data available'
        }
    
    # Detect all acceleration events
    all_events = detect_acceleration_events(speed_data)
    
    if not all_events:
        return {
            'trip_id': trip_data['trip_id'],
            'dominant_pattern': 'GENTLE',
            'avg_acceleration': 0,
            'max_acceleration': 0,
            'total_events': 0
        }
    
    # Calculate overall statistics
    accelerations = [e['acceleration_ms2'] for e in all_events]
    avg_accel = sum(accelerations) / len(accelerations)
    max_accel = max(accelerations)
    
    # Count by category
    gentle = sum(1 for e in all_events if e['category'] == 'GENTLE')
    moderate = sum(1 for e in all_events if e['category'] == 'MODERATE')
    aggressive = sum(1 for e in all_events if e['category'] == 'AGGRESSIVE')
    
    # Determine dominant pattern
    total = len(all_events)
    aggressive_pct = (aggressive / total) * 100
    moderate_pct = (moderate / total) * 100
    
    if aggressive_pct > 30:  # >30% aggressive events
        dominant = 'AGGRESSIVE'
    elif moderate_pct > 50:
        dominant = 'MODERATE'
    else:
        dominant = 'GENTLE'
    
    # Analyze by segment
    num_segments = len(trip_data.get('passenger_events', [])) - 1
    segment_analyses = []
    
    for seg_id in range(num_segments):
        seg_analysis = analyze_segment_acceleration(speed_data, seg_id)
        segment_analyses.append(seg_analysis)
    
    return {
        'trip_id': trip_data['trip_id'],
        'dominant_pattern': dominant,
        'avg_acceleration': round(avg_accel, 2),
        'max_acceleration': round(max_accel, 2),
        'total_events': total,
        'gentle_count': gentle,
        'gentle_percentage': round((gentle / total) * 100, 1),
        'moderate_count': moderate,
        'moderate_percentage': round((moderate / total) * 100, 1),
        'aggressive_count': aggressive,
        'aggressive_percentage': round((aggressive / total) * 100, 1),
        'segments': segment_analyses
    }


def get_acceleration_summary(acceleration_analysis):
    """
    Generate human-readable summary of acceleration analysis
    
    Args:
        acceleration_analysis (dict): Output from analyze_trip_acceleration
    
    Returns:
        str: Summary text
    """
    
    pattern = acceleration_analysis['dominant_pattern']
    avg_accel = acceleration_analysis['avg_acceleration']
    aggressive_pct = acceleration_analysis.get('aggressive_percentage', 0)
    
    if pattern == 'AGGRESSIVE':
        return f"Aggressive driving detected (avg {avg_accel} m/s², {aggressive_pct}% aggressive events)"
    elif pattern == 'MODERATE':
        return f"Moderate acceleration pattern (avg {avg_accel} m/s²)"
    else:
        return f"Gentle acceleration pattern (avg {avg_accel} m/s²)"


# Test function
def test_detector():
    """Test the acceleration detector with sample data"""
    
    print("🧪 Testing Acceleration Detector\n")
    
    # Test 1: Calculate single acceleration
    print("Test 1: Single acceleration calculation")
    accel = calculate_acceleration(0, 50, 10)  # 0 to 50 km/h in 10 seconds
    print(f"  0 to 50 km/h in 10 sec = {accel:.2f} m/s²")
    print(f"  Category: {classify_acceleration(accel)}")
    print()
    
    # Test 2: Different acceleration styles
    print("Test 2: Acceleration style classification")
    test_cases = [
        (0, 45, 25, "Gentle"),   # 0 to 45 in 25 sec
        (0, 50, 15, "Moderate"), # 0 to 50 in 15 sec
        (0, 55, 10, "Aggressive") # 0 to 55 in 10 sec
    ]
    
    for start, end, time, expected in test_cases:
        accel = calculate_acceleration(start, end, time)
        category = classify_acceleration(accel)
        print(f"  {start} to {end} km/h in {time}s = {accel:.2f} m/s² → {category}")
    print()
    
    # Test 3: Sample trip
    print("Test 3: Analyzing sample trip")
    sample_trip = {
        'trip_id': 'T001',
        'speed_data': [
            {'timestamp': 0, 'speed_kmh': 0, 'segment': 0},
            {'timestamp': 5, 'speed_kmh': 15, 'segment': 0},
            {'timestamp': 10, 'speed_kmh': 30, 'segment': 0},
            {'timestamp': 15, 'speed_kmh': 45, 'segment': 0},
            {'timestamp': 20, 'speed_kmh': 45, 'segment': 0},
            {'timestamp': 25, 'speed_kmh': 30, 'segment': 0},
            {'timestamp': 30, 'speed_kmh': 0, 'segment': 0},
        ],
        'passenger_events': [
            {'total_onboard': 45},
            {'total_onboard': 50}
        ]
    }
    
    analysis = analyze_trip_acceleration(sample_trip)
    print(f"Trip: {analysis['trip_id']}")
    print(f"Dominant Pattern: {analysis['dominant_pattern']}")
    print(f"Avg Acceleration: {analysis['avg_acceleration']} m/s²")
    print(f"Max Acceleration: {analysis['max_acceleration']} m/s²")
    print(f"Total Events: {analysis['total_events']}")
    print(f"  Gentle: {analysis['gentle_count']} ({analysis['gentle_percentage']}%)")
    print(f"  Moderate: {analysis['moderate_count']} ({analysis['moderate_percentage']}%)")
    print(f"  Aggressive: {analysis['aggressive_count']} ({analysis['aggressive_percentage']}%)")
    print()
    print(f"Summary: {get_acceleration_summary(analysis)}")
    print("\n✅ Acceleration Detector Test Complete!")


if __name__ == "__main__":
    test_detector()
    
    
    # **It can:**
# - Calculate acceleration from GPS speed data
#- Classify acceleration as Gentle/Moderate/Aggressive
#- Detect all acceleration events in a trip
#- Analyze acceleration patterns segment-by-segment
#- Determine dominant acceleration pattern for entire trip