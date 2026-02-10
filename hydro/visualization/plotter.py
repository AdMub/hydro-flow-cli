import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_cross_section(profile: dict, depth: float, filename: str = "cross_section.png"):
    """
    Generates a professional engineering cross-section of the river channel.
    """
    b = profile['channel_width']
    z = profile.get('side_slope', 0.0)
    name = profile['basin_name']
    
    # Calculate dimensions for plotting
    top_width = b + (2 * z * depth)
    height = depth * 1.5 # Add some freeboard for visuals
    
    # Coordinate points for the Trapezoid (Bank)
    # Left Bank Top, Left Toe, Right Toe, Right Bank Top
    x_bank = [-b/2 - z*height, -b/2, b/2, b/2 + z*height]
    y_bank = [height, 0, 0, height]
    
    # Coordinate points for Water Level
    x_water = [-b/2 - z*depth, b/2 + z*depth]
    y_water = [depth, depth]
    
    plt.figure(figsize=(10, 6))
    
    # Plot Banks
    plt.plot(x_bank, y_bank, 'k-', linewidth=3, label='River Bed')
    plt.fill_between(x_bank, y_bank, 0, color='#8B4513', alpha=0.3) # Earth color
    
    # Plot Water
    plt.plot(x_water, y_water, 'b-', linewidth=2, label=f'Water Level ({depth}m)')
    plt.fill_between(x_bank, y_bank, 0, where=(np.array(y_bank) <= depth), color='#00BFFF', alpha=0.6, interpolate=True)
    
    # Plot Water Surface specifically (to handle the fill correctly)
    plt.fill_between([-b/2 - z*depth, b/2 + z*depth], [depth, depth], [0,0], color='#00BFFF', alpha=0.5)

    # Styles
    plt.title(f"Hydraulic Cross-Section: {name}", fontsize=14)
    plt.xlabel("Channel Width (m)")
    plt.ylabel("Elevation (m)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Save
    output_path = Path("local_workspace") / filename
    output_path.parent.mkdir(exist_ok=True) # Ensure folder exists
    plt.savefig(output_path)
    plt.close()
    
    return str(output_path)