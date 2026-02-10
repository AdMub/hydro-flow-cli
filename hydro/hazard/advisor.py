from rich.console import Console
from rich.panel import Panel

console = Console()

def advise_on_risk(station: str, level: float, threshold: float):
    """
    Simulates an AI Engineer recommending solutions based on flood depth.
    """
    excess = level - threshold
    
    if excess <= 0:
        return "[green]No intervention needed.[/green]"
    
    advice = ""
    if excess < 1.0:
        advice = f"⚠️ [bold yellow]Minor Breach ({excess:.2f}m):[/bold yellow] Recommend temporary sandbagging along the {station} banks."
    elif excess < 2.5:
        advice = f"🚨 [bold orange]Major Breach ({excess:.2f}m):[/bold orange] Evacuate low-lying areas. Deploy mobile flood barriers immediately."
    else:
        advice = f"☠️ [bold red]CATASTROPHIC FAILURE ({excess:.2f}m):[/bold red] Dam failure imminent? Immediate aerial evacuation required. Trigger National Emergency Protocol."
        
    return advice