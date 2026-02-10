import typer
import json
import os
import time
import pandas as pd
from rich.console import Console
from rich.panel import Panel

# Custom Modules
from hydro.simulation.engine import HydraulicEngine
from hydro.hazard.report import generate_styled_report
from hydro.crs.checker import validate_crs
from hydro.hazard.advisor import advise_on_risk
from hydro.visualization.plotter import plot_cross_section
from hydro.utils.dem_loader import get_elevation_from_dem
from hydro.simulation.monte_carlo import run_flood_risk_simulation

# Initialize Typer and Rich
app = typer.Typer(help="🌊 Hydro-Flow CLI: The Hydrologist's Terminal Assistant")
console = Console()

@app.command()
def check_crs(file_path: str):
    """Verify the Coordinate Reference System (CRS) of a GeoJSON or TIFF."""
    console.print(f"[bold blue]🔍 Analyzing CRS for:[/bold blue] {file_path}...")
    result = validate_crs(file_path)
    if "Error" in result:
        console.print(f"[bold red]❌ {result}[/bold red]")
    else:
        console.print(f"[bold green]✅ Success:[/bold green] {result}")

@app.command()
def wizard():
    """Interactive mode to create a new Basin Profile."""
    console.print(Panel("🧙‍♂️ [bold magenta]Hydro-Flow Profile Wizard[/bold magenta]", border_style="magenta"))
    
    name = typer.prompt("What is the Basin Name?")
    width = typer.prompt("Channel Bottom Width (m)", type=float)
    slope = typer.prompt("Channel Slope (e.g., 0.001)", type=float)
    n_val = typer.prompt("Manning's Roughness (n)", type=float, default=0.035)
    side_slope = typer.prompt("Side Slope (z) [Horizontal/Vertical]", type=float, default=2.0)
    
    profile_data = {
        "basin_name": name,
        "channel_width": width,
        "slope": slope,
        "manning_n": n_val,
        "side_slope": side_slope,
        "threshold_high": 4.5
    }
    
    os.makedirs("data/profiles", exist_ok=True)
    filename = name.lower().replace(" ", "_") + ".json"
    path = f"data/profiles/{filename}"
    
    with open(path, "w") as f:
        json.dump(profile_data, f, indent=4)
        
    console.print(f"\n[bold green]✅ Profile Saved![/bold green] You can now run:\n[cyan]hydro simulate --profile {path}[/cyan]")

@app.command()
def simulate(
    profile: str = typer.Option("data/profiles/ona.json", help="Path to basin JSON profile"), 
    depth: float = typer.Option(2.0, help="Water depth in meters")
):
    """Run a hydraulic simulation using a basin profile."""
    console.print(f"[bold yellow]⚙️ Running simulation...[/bold yellow]")
    
    try:
        engine = HydraulicEngine(profile)
        result = engine.calculate_discharge(depth)
        
        # Logic to handle dictionary output from advanced engine
        if isinstance(result, dict):
            q = result['discharge']
            details = f"\nVelocity: {result['velocity']} m/s | Area: {result['area']} m²"
        else:
            q = result
            details = ""

        console.print(f"\n[bold cyan]Basin:[/bold cyan] {engine.profile['basin_name']}")
        console.print(f"[bold cyan]Depth:[/bold cyan] {depth}m")
        
        console.print(Panel(
            f"🚀 Calculated Discharge: [bold]{q} m³/s[/bold]{details}", 
            border_style="green",
            expand=False
        ))
        
    except Exception as e:
        console.print(f"[bold red]❌ Simulation failed:[/bold red] {e}")

@app.command()
def hazard(
    csv_file: str, 
    threshold: float = typer.Option(4.0, help="Hazard threshold in meters")
):
    """Generate a high-visibility flood hazard report with Engineering Advice."""
    console.print(f"[bold magenta]📊 Generating Report for:[/bold magenta] {csv_file}")
    
    try:
        generate_styled_report(csv_file, threshold)
        console.print("\n[bold cyan]🧠 AI Engineering Recommendations:[/bold cyan]")
        
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            if row['level'] > threshold:
                advice = advise_on_risk(row['station'], row['level'], threshold)
                console.print(Panel(advice, title=f"Station: {row['station']}", border_style="red"))
                
    except Exception as e:
        console.print(f"[bold red]❌ Report generation failed:[/bold red] {e}")

@app.command()
def visualize(
    profile: str = typer.Option("data/profiles/ona.json", help="Profile to plot"),
    depth: float = typer.Option(3.0, help="Current water depth")
):
    """GENERATE A CROSS-SECTION IMAGE of the river channel."""
    console.print(f"[bold yellow]🎨 Generating Digital Twin for:[/bold yellow] {profile}")
    
    with open(profile, 'r') as f:
        data = json.load(f)
        
    output = plot_cross_section(data, depth)
    
    console.print(Panel(
        f"[bold green]Image Saved:[/bold green] {output}\n"
        f"Open this file to see the hydraulic cross-section.",
        title="Visualization Complete",
        border_style="green"
    ))

@app.command()
def scan_dem(
    lat: float, 
    lon: float,
    dem_file: str = "data/dem/ona_basin.tif"
):
    """Query the Digital Elevation Model (DEM) for ground topology."""
    console.print(f"[bold blue]🛰️ Connecting to Geospatial Engine...[/bold blue]")
    
    with console.status("[bold green]Sampling Raster Data...[/bold green]"):
        time.sleep(1.5) # UX Pause
        elevation = get_elevation_from_dem(lat, lon, dem_file)
        
    console.print(Panel(
        f"📍 Coordinates: {lat}, {lon}\n"
        f"⛰️ Elevation: [bold]{elevation} meters[/bold]\n"
        f"📂 Source: {dem_file}",
        title="Geospatial Sampling",
        border_style="blue"
    ))

@app.command()
def design(
    target_q: float = typer.Option(..., help="Target Discharge required (m³/s)"),
    max_depth: float = typer.Option(4.0, help="Maximum allowable depth in meters")
):
    """
    🤖 AUTO-DESIGNER: Solves the Inverse Problem to find the optimal channel width.
    """
    console.print(f"[bold yellow]📐 Solving Inverse Design Problem for Q={target_q} m³/s...[/bold yellow]")
    
    # We use the Ona profile as the baseline for slope/roughness
    engine = HydraulicEngine("data/profiles/ona.json")
    
    with console.status("[bold green]Running Newton-Raphson Optimization...[/bold green]"):
        result = engine.design_optimal_channel(target_q, max_depth)
    
    if result.get('status') == "Optimized":
        console.print(Panel(
            f"✅ [bold green]OPTIMAL DESIGN FOUND[/bold green]\n"
            f"Recommended Width: [bold yellow]{result['optimal_width']} m[/bold yellow]\n"
            f"Excavation Volume: {result['excavation_area']} m²/unit\n"
            f"Constraints: Flow > {target_q} m³/s | Depth < {max_depth} m",
            title="Civil Engineering Auto-Designer",
            border_style="green"
        ))
    else:
        console.print(Panel("❌ No Feasible Solution Found.\nTry increasing max depth or slope.", style="bold red"))

@app.command()
def stress_test(
    depth: float = typer.Option(3.5, help="Base water depth"),
    iterations: int = typer.Option(1000, help="Number of Monte Carlo simulations")
):
    """
    MONTE CARLO SIMULATION: Predicts failure probability & Plots Histogram.
    """
    console.print(f"[bold magenta]🎲 Running {iterations} Monte Carlo Simulations...[/bold magenta]")
    
    with console.status("[bold magenta]Crunching Statistics & Generating Graph...[/bold magenta]"):
        result = run_flood_risk_simulation("data/profiles/ona.json", depth, iterations)
        time.sleep(1)

    risk_color = "green"
    if result['probability'] > 20: risk_color = "yellow"
    if result['probability'] > 50: risk_color = "red"

    console.print(Panel(
        f"📊 [bold]Failure Probability:[/bold] [{risk_color}]{result['probability']:.1f}%[/{risk_color}]\n"
        f"🌊 [bold]95th Percentile Flow:[/bold] {result['p95_discharge']:.2f} m³/s\n"
        f"📈 [bold]Mean Flow:[/bold] {result['mean_discharge']:.2f} m³/s\n"
        f"🖼️ [bold]Risk Graph Saved:[/bold] {result['graph']}",
        title="Hydraulic Reliability Analysis",
        border_style=risk_color
    ))

@app.command()
def bridge_check(
    depth: float = typer.Option(3.5, help="Upstream water depth"),
    contraction: float = typer.Option(0.7, help="Bridge width ratio (0.7 = 30% blocked)")
):
    """
    Check Backwater Effect (Afflux) at a bridge constriction.
    """
    engine = HydraulicEngine("data/profiles/ona.json")
    res = engine.calculate_bridge_afflux(depth, contraction)
    
    console.print(Panel(
        f"🌉 [bold]Bridge Impact Analysis[/bold]\n"
        f"Rise in Water Level (Afflux): [bold red]+{res['afflux']} m[/bold red]\n"
        f"Velocity Under Bridge: [bold yellow]{res['bridge_velocity']} m/s[/bold yellow]\n"
        f"New Upstream Level: {res['new_water_level']} m",
        title="Hydraulic Constriction (Bernoulli)",
        border_style="cyan"
    ))

@app.command()
def test_suite():
    """Run the automated engineering validation suite."""
    console.print("[bold magenta]🧪 Running Unit Tests...[/bold magenta]")
    os.system("pytest tests/")

if __name__ == "__main__":
    app()