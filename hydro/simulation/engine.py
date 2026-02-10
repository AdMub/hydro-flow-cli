import json
import math
from pathlib import Path
from scipy.optimize import minimize_scalar  # <--- The CS Powerhouse

class HydraulicEngine:
    def __init__(self, profile_path: str):
        self.profile = self._load_profile(profile_path)

    def _load_profile(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def calculate_discharge(self, depth: float):
        """
        Standard Manning's Calculation (The 'Forward' Problem).
        Calculates discharge for a Trapezoidal Channel.
        """
        b = self.profile['channel_width']
        z = self.profile.get('side_slope', 0.0)
        n = self.profile['manning_n']
        s = self.profile['slope']
        
        # 1. Calculate Geometric Properties
        area = (b + (z * depth)) * depth
        perimeter = b + (2 * depth * math.sqrt(1 + (z**2)))
        radius = area / perimeter if perimeter > 0 else 0
        
        # 2. Calculate Discharge (Manning's Equation)
        discharge = (1/n) * area * (math.pow(radius, 2/3)) * (math.sqrt(s))
        velocity = discharge / area if area > 0 else 0
        
        return {
            "discharge": round(discharge, 2),
            "velocity": round(velocity, 2),
            "area": round(area, 2),
            "perimeter": round(perimeter, 2)
        }

    def design_optimal_channel(self, target_discharge: float, max_depth: float):
        """
        SOLVES THE INVERSE PROBLEM (Auto-Design):
        Find the minimal channel width (b) required to carry specific flow (Q).
        Objective: Minimize Excavation Cost (Cross-Sectional Area).
        """
        n = self.profile['manning_n']
        s = self.profile['slope']
        z = self.profile.get('side_slope', 0.0)
        
        # We define a Cost Function that the AI tries to minimize
        def cost_function(trial_width):
            if trial_width <= 0: return 999999 # Physical impossibility penalty
            
            # 1. Calculate Hydraulic Properties for this trial width
            area = (trial_width + z * max_depth) * max_depth
            perimeter = trial_width + 2 * max_depth * math.sqrt(1 + z**2)
            
            if perimeter <= 0: return 999999
            radius = area / perimeter
            
            # 2. Calculate Capacity (Manning's)
            capacity = (1/n) * area * (radius**(2/3)) * (s**0.5)
            
            # 3. Constraint: We MUST meet the Target Discharge
            # If capacity is too low, return a huge penalty so the optimizer avoids this width
            if capacity < target_discharge:
                return 999999 + (target_discharge - capacity) # Penalty + Gap
            
            # 4. Objective: If capacity is met, return the Area (Excavation Cost)
            return area

        # Run the Scipy Optimizer (Bounded search between 0.5m and 100m width)
        result = minimize_scalar(cost_function, bounds=(0.5, 100.0), method='bounded')
        
        if result.success and result.fun < 900000:
            return {
                "optimal_width": round(result.x, 2),
                "excavation_area": round(result.fun, 2),
                "status": "Optimized"
            }
        else:
            return {"status": "Failed to Converge"}
        
    def calculate_bridge_afflux(self, upstream_depth: float, contraction_ratio: float = 0.8):
        """
        Calculates the rise in water level (Afflux) caused by a bridge constriction.
        Uses the Energy Equation (Bernoulli).
        """
        # Normal Flow State
        normal_flow = self.calculate_discharge(upstream_depth)
        v1 = normal_flow['velocity']
        g = 9.81
        
        # Velocity increases at bridge (V2 = V1 / ratio)
        v2 = v1 / contraction_ratio
        
        # Calculate Head Loss (hL) due to turbulence
        k_loss = 0.5
        head_loss = k_loss * ((v2**2) / (2*g))
        
        # Afflux (Rise in water level)
        afflux = ((v2**2 - v1**2) / (2*g)) + head_loss
        
        return {
            "afflux": round(afflux, 3),
            "new_water_level": round(upstream_depth + afflux, 3),
            "bridge_velocity": round(v2, 2)
        }