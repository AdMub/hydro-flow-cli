import random
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from hydro.simulation.engine import HydraulicEngine

def run_flood_risk_simulation(profile_path: str, base_depth: float, iterations: int = 1000):
    """
    Performs a Monte Carlo simulation AND generates a risk histogram.
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
        # 1. Random n (roughness changes +/- 10%)
        random_n = base_n * random.uniform(0.9, 1.1)
        # 2. Random Depth (Flash flood surge +/- 20%)
        random_depth = base_depth * random.uniform(0.8, 1.3)
        
        # Temporary profile update in memory
        engine.profile['manning_n'] = random_n
        
        output = engine.calculate_discharge(random_depth)
        
        # Check Failure (Did random depth exceed threshold?)
        if random_depth > threshold:
            failures += 1
            
        results.append(output['discharge'])
        
    probability = (failures / iterations) * 100
    
    # --- VISUALIZATION: GENERATE HISTOGRAM ---
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=30, color='#4682B4', edgecolor='black', alpha=0.7)
    
    # Add mean line
    mean_val = np.mean(results)
    plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean Flow: {mean_val:.1f}')
    
    plt.title(f"Monte Carlo Risk Distribution ({iterations} Iterations)", fontsize=14)
    plt.xlabel("Discharge (m³/s)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save Graph
    output_path = Path("local_workspace") / "risk_distribution.png"
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    
    return {
        "probability": probability,
        "p95_discharge": np.percentile(results, 95),
        "mean_discharge": np.mean(results),
        "graph": str(output_path)
    }