import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def generate_styled_report(csv_path: str, threshold: float):
    df = pd.read_csv(csv_path)
    
    table = Table(title="🌊 Flood Hazard Analysis", header_style="bold magenta", border_style="blue")
    table.add_column("Station ID", justify="center")
    table.add_column("Water Level (m)", justify="right")
    table.add_column("Status", justify="center")

    for _, row in df.iterrows():
        level = row['level']
        if level >= threshold:
            status = "[bold red]🚨 HIGH RISK[/bold red]"
        elif level >= (threshold * 0.7):
            status = "[bold yellow]⚠️ WARNING[/bold yellow]"
        else:
            status = "[bold green]✅ SAFE[/bold green]"
            
        table.add_row(str(row['station']), f"{level:.2f}", status)

    console.print(Panel.fit("Hydro-Flow Analysis Results", style="bold cyan"))
    console.print(table)