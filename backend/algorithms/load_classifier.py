"""
Load Classifier Algorithm
Classifies passenger load into Light/Medium/Heavy categories
"""

# Constants
EMPTY_BUS_WEIGHT_KG = 12000
AVG_PASSENGER_WEIGHT_KG = 70
BUS_CAPACITY = 84

# Load category thresholds
LIGHT_THRESHOLD = 30
MEDIUM_THRESHOLD = 60


def classify_load(passenger_count, capacity=BUS_CAPACITY):
    """
    Classify passenger load into Light/Medium/Heavy
    
    Args:
        passenger_count (int): Number of passengers on bus
        capacity (int): Bus capacity (default 84)
    
    Returns:
        dict: {
            'category': 'LIGHT' | 'MEDIUM' | 'HEAVY',
            'passenger_count': int,
            'capacity_percentage': float,
            'total_weight_kg': float,
            'weight_increase_percentage': float
        }
    """
    
    # Calculate bus weight
    passenger_weight = passenger_count * AVG_PASSENGER_WEIGHT_KG
    total_weight = EMPTY_BUS_WEIGHT_KG + passenger_weight
    weight_increase = (passenger_weight / EMPTY_BUS_WEIGHT_KG) * 100
    capacity_pct = (passenger_count / capacity) * 100
    
    # Classify based on thresholds
    if passenger_count <= LIGHT_THRESHOLD:
        category = "LIGHT"
    elif passenger_count <= MEDIUM_THRESHOLD:
        category = "MEDIUM"
    else:
        category = "HEAVY"
    
    return {
        'category': category,
        'passenger_count': passenger_count,
        'capacity_percentage': round(capacity_pct, 1),
        'total_weight_kg': total_weight,
        'weight_increase_percentage': round(weight_increase, 1),
        'empty_weight_kg': EMPTY_BUS_WEIGHT_KG,
        'passenger_weight_kg': passenger_weight
    }


def classify_trip_segments(passenger_events):
    """
    Classify load for each segment of a trip
    
    Args:
        passenger_events (list): List of passenger events from trip data
            Each event: {'stop_id', 'boarding', 'alighting', 'total_onboard'}
    
    Returns:
        list: Load analysis for each segment
    """
    
    segments = []
    
    for i, event in enumerate(passenger_events):
        load_analysis = classify_load(event['total_onboard'])
        
        segment = {
            'segment_id': i,
            'stop_name': event.get('stop_name', f"Stop {i}"),
            'passenger_count': event['total_onboard'],
            'load_category': load_analysis['category'],
            'capacity_percentage': load_analysis['capacity_percentage'],
            'total_weight_kg': load_analysis['total_weight_kg']
        }
        
        segments.append(segment)
    
    return segments


def get_dominant_load_category(segments):
    """
    Determine the dominant load category for entire trip
    
    Args:
        segments (list): List of segment load analyses
    
    Returns:
        str: 'LIGHT' | 'MEDIUM' | 'HEAVY' (most common category)
    """
    
    # Count each category
    counts = {'LIGHT': 0, 'MEDIUM': 0, 'HEAVY': 0}
    
    for segment in segments:
        category = segment['load_category']
        counts[category] += 1
    
    # Return category with highest count
    dominant = max(counts, key=counts.get)
    
    return dominant


def analyze_trip_load(trip_data):
    """
    Complete load analysis for a trip
    
    Args:
        trip_data (dict): Trip data with passenger_events
    
    Returns:
        dict: Complete load analysis for the trip
    """
    
    # Classify each segment
    segments = classify_trip_segments(trip_data['passenger_events'])
    
    # Get dominant category
    dominant_category = get_dominant_load_category(segments)
    
    # Calculate statistics
    passenger_counts = [s['passenger_count'] for s in segments]
    max_load = max(passenger_counts)
    avg_load = sum(passenger_counts) / len(passenger_counts)
    
    # Count heavy load segments
    heavy_segments = sum(1 for s in segments if s['load_category'] == 'HEAVY')
    
    return {
        'trip_id': trip_data['trip_id'],
        'dominant_load_category': dominant_category,
        'max_passenger_count': max_load,
        'avg_passenger_count': round(avg_load, 1),
        'heavy_load_segments': heavy_segments,
        'total_segments': len(segments),
        'segments': segments
    }


# Test function
def test_classifier():
    """Test the load classifier with sample data"""
    
    print("🧪 Testing Load Classifier\n")
    
    # Test individual classifications
    test_cases = [15, 45, 72]
    
    for pax in test_cases:
        result = classify_load(pax)
        print(f"Passengers: {pax}")
        print(f"  Category: {result['category']}")
        print(f"  Capacity: {result['capacity_percentage']}%")
        print(f"  Total Weight: {result['total_weight_kg']:,} kg")
        print(f"  Weight Increase: +{result['weight_increase_percentage']}%")
        print()
    
    # Test with trip data
    print("📊 Testing with sample trip:")
    sample_trip = {
        'trip_id': 'T001',
        'passenger_events': [
            {'stop_name': 'Tampines', 'total_onboard': 15},
            {'stop_name': 'Simei', 'total_onboard': 42},
            {'stop_name': 'Bedok', 'total_onboard': 68},
            {'stop_name': 'Marine Parade', 'total_onboard': 45}
        ]
    }
    
    analysis = analyze_trip_load(sample_trip)
    print(f"Trip: {analysis['trip_id']}")
    print(f"Dominant Load: {analysis['dominant_load_category']}")
    print(f"Max Passengers: {analysis['max_passenger_count']}")
    print(f"Avg Passengers: {analysis['avg_passenger_count']}")
    print(f"Heavy Segments: {analysis['heavy_load_segments']}/{analysis['total_segments']}")
    print("\n✅ Load Classifier Test Complete!")


if __name__ == "__main__":
    test_classifier()
    
# Classify any passenger count → Light/Medium/Heavy
# - Calculate bus weight and weight increase percentage
# - Analyze entire trips segment-by-segment
# - Determine dominant load category for trips
