import math

# Average annual rainfall data by state in inches
# Source: NOAA Climate Data
STATE_RAINFALL = {
    'Alabama': 56.0,
    'Alaska': 22.0,
    'Arizona': 13.6,
    'Arkansas': 50.0,
    'California': 22.0,
    'Colorado': 15.9,
    'Connecticut': 47.0,
    'Delaware': 45.0,
    'Florida': 54.5,
    'Georgia': 50.0,
    'Hawaii': 63.7,
    'Idaho': 18.9,
    'Illinois': 39.2,
    'Indiana': 41.7,
    'Iowa': 34.0,
    'Kansas': 28.9,
    'Kentucky': 48.0,
    'Louisiana': 60.1,
    'Maine': 42.2,
    'Maryland': 44.5,
    'Massachusetts': 47.7,
    'Michigan': 32.4,
    'Minnesota': 27.3,
    'Mississippi': 59.0,
    'Missouri': 42.2,
    'Montana': 15.3,
    'Nebraska': 23.6,
    'Nevada': 9.5,
    'New Hampshire': 43.4,
    'New Jersey': 47.1,
    'New Mexico': 14.6,
    'New York': 41.8,
    'North Carolina': 50.3,
    'North Dakota': 17.8,
    'Ohio': 39.1,
    'Oklahoma': 36.5,
    'Oregon': 27.4,
    'Pennsylvania': 42.9,
    'Rhode Island': 47.9,
    'South Carolina': 49.8,
    'South Dakota': 20.1,
    'Tennessee': 54.2,
    'Texas': 28.9,
    'Utah': 12.2,
    'Vermont': 42.7,
    'Virginia': 44.3,
    'Washington': 38.4,
    'West Virginia': 45.2,
    'Wisconsin': 32.6,
    'Wyoming': 12.9
}

# Hawaii-specific rainfall data
# Source: Hawaii Stormwater Management Guidelines
HAWAII_REGIONS = {
    'Kona': {'annual_rainfall': 75.0, 'intensity_factor': 1.2},  # Wet side
    'Hilo': {'annual_rainfall': 140.0, 'intensity_factor': 1.4}, # Very wet
    'Honolulu': {'annual_rainfall': 25.0, 'intensity_factor': 1.0}, # Dry side
    'Kauai North': {'annual_rainfall': 85.0, 'intensity_factor': 1.3},
    'Maui Upcountry': {'annual_rainfall': 65.0, 'intensity_factor': 1.1}
}

def calculate_pipe_diameter(rainfall_inches, drainage_area_sqft, safety_factor=1.5):
    """
    Calculate recommended pipe diameter based on rainfall and drainage area.
    Uses the Rational Method formula Q = CIA
    
    Args:
        rainfall_inches: Annual rainfall in inches
        drainage_area_sqft: Drainage area in square feet
        safety_factor: Multiplier for extreme conditions (default 1.5)
    
    Returns:
        tuple: (normal_diameter_inches, extreme_diameter_inches)
    """
    # Convert annual rainfall to intensity (inches per hour)
    # Using a more aggressive conversion factor
    intensity = rainfall_inches / (365 * 12)  # Changed from 24 to 12 hours to account for daytime concentration
    
    # Runoff coefficient (typical value for developed areas)
    C = 0.75  # Increased from 0.65 for more conservative estimate
    
    # Convert square feet to acres
    A = drainage_area_sqft / 43560
    
    # Calculate flow rate in cubic feet per second (cfs)
    Q = C * intensity * A * 43560 / 3600  # Convert to cubic feet per second
    
    # Apply Manning's equation to determine pipe diameter
    n = 0.013  # Manning's roughness coefficient
    S = 0.02   # Slope (ft/ft)
    
    # Calculate normal diameter
    normal_diameter = math.pow((Q * n) / (0.463 * math.pow(S, 0.5)), 0.375) * 12
    
    # Calculate extreme diameter with safety factor
    extreme_diameter = normal_diameter * safety_factor
    
    return round(normal_diameter, 1), round(extreme_diameter, 1)

def get_pipe_recommendations(state, drainage_area_sqft):
    """
    Get pipe size recommendations for a given state and drainage area.
    
    Args:
        state: Name of the US state
        drainage_area_sqft: Drainage area in square feet
    
    Returns:
        dict: Recommendations including normal and extreme pipe sizes
    """
    state = state.title()  # Normalize state name
    
    if state not in STATE_RAINFALL:
        return {"error": f"State '{state}' not found in database"}
    
    rainfall = STATE_RAINFALL[state]
    normal_size, extreme_size = calculate_pipe_diameter(rainfall, drainage_area_sqft)
    
    # Round up to nearest standard pipe size
    standard_sizes = [4, 6, 8, 10, 12, 15, 18, 24, 30, 36, 42, 48]
    
    def round_to_standard_size(size):
        for std_size in standard_sizes:
            if std_size >= size:
                return std_size
        return standard_sizes[-1]
    
    normal_size = round_to_standard_size(normal_size)
    extreme_size = round_to_standard_size(extreme_size)
    
    return {
        "state": state,
        "annual_rainfall": rainfall,
        "drainage_area_sqft": drainage_area_sqft,
        "normal_pipe_size": normal_size,
        "extreme_pipe_size": extreme_size,
        "unit": "inches"
    }

def get_hawaii_recommendations(drainage_area_sqft):
    """
    Get detailed pipe recommendations for different regions in Hawaii.
    Hawaii uses different standards due to:
    1. Intense tropical rainfall
    2. Flash flood considerations
    3. Volcanic soil conditions
    4. Regional microclimate variations
    
    Args:
        drainage_area_sqft: Drainage area in square feet
    
    Returns:
        dict: Recommendations for each region
    """
    results = {}
    for region, data in HAWAII_REGIONS.items():
        # Use higher safety factors for Hawaii due to tropical storms
        safety_factor = 2.0  # Increased from standard 1.5
        
        # Calculate with regional intensity factor
        rainfall = data['annual_rainfall']
        intensity_factor = data['intensity_factor']
        
        # Adjust calculations for Hawaii's conditions
        normal_size, extreme_size = calculate_pipe_diameter(
            rainfall * intensity_factor,  # Adjusted rainfall
            drainage_area_sqft,
            safety_factor
        )
        
        results[region] = {
            'annual_rainfall': rainfall,
            'normal_pipe_size': normal_size,
            'extreme_pipe_size': extreme_size,
            'notes': get_hawaii_region_notes(region)
        }
    
    return results

def get_hawaii_region_notes(region):
    """Get specific notes for each Hawaii region."""
    notes = {
        'Kona': "Volcanic soil, high permeability. Consider lava tube presence.",
        'Hilo': "Highest rainfall area. Flash flood prone. Use additional overflow systems.",
        'Honolulu': "Urban area. Consider high-intensity short-duration storms.",
        'Kauai North': "High rainfall, steep terrain. Use additional erosion controls.",
        'Maui Upcountry': "Variable rainfall, volcanic soil. Monitor soil stability."
    }
    return notes.get(region, "")

def show_all_states(drainage_area=50000):
    """
    Display pipe recommendations for all states using the same drainage area.
    
    Args:
        drainage_area: Drainage area in square feet (default 50000)
    """
    print(f"\nPipe Size Recommendations for All States")
    print(f"Using drainage area of {drainage_area} square feet")
    print("\n{:<20} {:<15} {:<15} {:<15}".format(
        "State", "Rainfall (in)", "Normal (in)", "Extreme (in)"))
    print("-" * 65)
    
    # Sort states alphabetically
    for state in sorted(STATE_RAINFALL.keys()):
        result = get_pipe_recommendations(state, drainage_area)
        print("{:<20} {:<15.1f} {:<15} {:<15}".format(
            state,
            result['annual_rainfall'],
            result['normal_pipe_size'],
            result['extreme_pipe_size']
        ))

def show_hawaii_comparison(drainage_area=50000):
    """Display detailed comparison of Hawaii regions vs mainland standards."""
    print("\nHawaii Regional Drainage Requirements")
    print(f"Using drainage area of {drainage_area} square feet")
    print("\nStandard Mainland Calculation (Average):")
    mainland = get_pipe_recommendations("Hawaii", drainage_area)
    print(f"  Annual Rainfall: {mainland['annual_rainfall']} inches")
    print(f"  Normal Pipe Size: {mainland['normal_pipe_size']} inches")
    print(f"  Extreme Pipe Size: {mainland['extreme_pipe_size']} inches")
    
    print("\nDetailed Hawaii Regional Analysis:")
    print("-" * 80)
    hawaii_data = get_hawaii_recommendations(drainage_area)
    for region, data in hawaii_data.items():
        print(f"\n{region}:")
        print(f"  Annual Rainfall: {data['annual_rainfall']} inches")
        print(f"  Normal Pipe Size: {data['normal_pipe_size']} inches")
        print(f"  Extreme Pipe Size: {data['extreme_pipe_size']} inches")
        print(f"  Special Considerations: {data['notes']}")

def main():
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python pipe_calculator.py <state_name> <drainage_area_square_feet>")
        print("Example: python pipe_calculator.py Virginia 5000")
        sys.exit(1)
        
    state = sys.argv[1]
    try:
        drainage_area = float(sys.argv[2])
    except ValueError:
        print("Error: Drainage area must be a number")
        sys.exit(1)
        
    result = get_pipe_recommendations(state, drainage_area)
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        sys.exit(1)
        
    print(f"\nResults for {result['state']}:")
    print(f"Annual Rainfall: {result['annual_rainfall']} inches")
    print(f"Drainage Area: {result['drainage_area_sqft']} square feet")
    print(f"Recommended Pipe Sizes:")
    print(f"  - Normal Conditions: {result['normal_pipe_size']} inches")
    print(f"  - Extreme Conditions: {result['extreme_pipe_size']} inches")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments, show all states
        show_all_states()
        print("\n" + "="*80)
        print("DETAILED HAWAII ANALYSIS")
        print("="*80)
        show_hawaii_comparison()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "hawaii":
        # Show Hawaii specific analysis
        show_hawaii_comparison()
    elif len(sys.argv) == 3:
        # State and drainage area provided
        main()
    else:
        print("Usage:")
        print("  Show all states: python pipe_calculator.py")
        print("  Hawaii analysis: python pipe_calculator.py hawaii")
        print("  Single state: python pipe_calculator.py <state_name> <drainage_area_square_feet>")
        print("Example: python pipe_calculator.py Virginia 5000")
        sys.exit(1)
