import random
import numpy as np
from rich.progress import track
from hydro.simulation.engine import HydraulicEngine

def run_flood_risk_simulation(profile_path: str, base_depth: float, iterations: int = 1000):
    """
    Performs a Monte Carlo simulation to estimate failure probability.
    Variability factors:
    - Rainfall spikes (Depth variation)
    - Vegetation growth (Manning's n variation)
    """
    engine = HydraulicEngine(profile_path)
    failures = 0
    results = []
    
    # Base parameters
    base_n = engine.profile['manning_n']
    threshold = engine.profile['threshold_high']
    
    for _ in range(iterations):
        # CS Logic: Randomize environmental factors
        # 1. Random n (roughness changes +/- 10%)
        random_n = base_n * random.uniform(0.9, 1.1)
        engine.profile['manning_n'] = random_n
        
        # 2. Random Depth (Flash flood surge +/- 20%)
        random_depth = base_depth * random.uniform(0.8, 1.3)
        
        # Run Simulation
        output = engine.calculate_discharge(random_depth)
        
        # Check Failure (Did water exceed bank threshold?)
        if random_depth > threshold:
            failures += 1
            
        results.append(output['discharge'])
        
    probability = (failures / iterations) * 100
    
    return {
        "probability": probability,
        "p95_discharge": np.percentile(results, 95), # 95th percentile flow
        "mean_discharge": np.mean(results)
    }