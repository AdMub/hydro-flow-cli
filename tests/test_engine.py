import pytest
from hydro.simulation.engine import HydraulicEngine

# Mock profile data
MOCK_PROFILE = {
    "basin_name": "Test River",
    "channel_width": 10.0,
    "slope": 0.001,
    "manning_n": 0.035,
    "side_slope": 2.0
}

def test_trapezoidal_discharge():
    """Test that physics math is accurate."""
    # Create a temporary JSON for the test
    import json
    with open("tests/temp_profile.json", "w") as f:
        json.dump(MOCK_PROFILE, f)
        
    engine = HydraulicEngine("tests/temp_profile.json")
    result = engine.calculate_discharge(depth=2.0)
    
    # We expect positive flow
    assert result['discharge'] > 0
    assert result['area'] == 28.0 # (10 + 2*2)*2 = 28
    assert result['velocity'] > 0