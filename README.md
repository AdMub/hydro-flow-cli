# 🌊 Hydro-Flow CLI

> **The Hydrologist's Terminal Assistant**
> *Advanced open-channel flow modeling, Monte Carlo risk analysis, and hydraulic auto-design.*

![Hydro-Flow Hero Image](PLACEHOLDER_LINK_TO_YOUR_COVER_IMAGE_OR_TERMINAL_SCREENSHOT.png)
*(A Digital Twin of the Ona River Basin generated directly in the terminal)*

## 🚀 Overview

**Hydro-Flow CLI** is an AI-augmented command-line tool designed to bring **HEC-RAS caliber hydrology** to the terminal.

Hydrologic modeling usually requires expensive, heavy GUI software. **Hydro-Flow** breaks this barrier by providing a "Headless" engineering engine that helps engineers **design** channels, **visualize** flood risks, and **stress-test** infrastructure using statistical simulations—all from a simple CLI.

Battle-tested on the **Ona River Basin** (Nigeria), it empowers engineers to perform complex geospatial and hydraulic analysis using **Scipy**, **NumPy**, and **Docker**.

---

## 📺 Demo Video

[![Watch the Hydro-Flow Demo](https://img.youtube.com/vi/PLACEHOLDER_VIDEO_ID/0.jpg)](PLACEHOLDER_LINK_TO_YOUR_YOUTUBE_VIDEO)

> *Watch how Hydro-Flow solves complex inverse hydraulic problems in under 2 minutes.*

---

## ✨ Key Features & Engineering Logic

### 1. 🤖 Auto-Design (The Inverse Solver)
**The Problem:** Usually, engineers guess channel dimensions until they find one that works (Trial & Error).
**The Solution:** Hydro-Flow solves the **Inverse Hydraulic Problem** using **Scipy Optimization** (Newton-Raphson Method). It calculates the *exact* minimum channel width required to handle a target flood while minimizing excavation costs.

```bash
hydro design --target-q 500 --max-depth 5.0

# Output:
# ✅ OPTIMAL DESIGN FOUND
# Recommended Width: 8.79 m
# Excavation Volume: 118.97 m²/unit
```

## 🎲 Monte Carlo Stress Testing (Stochastic Analysis)
**The Problem:** Standard calculators assume perfect conditions. They fail to account for real-world variability.
**The Solution:** Hydro-Flow runs **1,000 parallel simulations** with randomized variables (Roughness $n \pm 10\%$, Flash Flood Surge $y \pm 20\%$) to generate a **Probability Density Function** of failure.


Predicts infrastructure reliability by running **1,000 parallel simulations** with randomized environmental variables (roughness, rainfall surge). It generates a **Probability Density Histogram** to visualize risk.

```bash
hydro stress-test --depth 3.8 --iterations 1000
# 📊 Failure Probability: 24.5% (Risk Histogram Saved)
```

## 🎨 Visual Digital Twin
Instantly generates professional hydraulic cross-sections (`.png`) showing water levels against channel banks using procedural plotting.

```bash
hydro visualize --depth 4.5
```

## 🌉 Bridge Scour Analysis
Calculates the **Backwater Effect** (Afflux) caused by bridge constrictions using **Bernoulli's Energy Principle.**

```bash
hydro bridge-check --contraction 0.7
# Rise in Water Level: +1.11 m
```

## 🤖 The AI Co-Engineer Experience
Built for the **GitHub Copilot CLI Challenge,** this project pushes the boundaries of BASH-based engineering.

1. **Solving Inverse Problems:** I used Copilot to implement the **Scipy Optimization** logic (`minimize_scalar`) to automatically minimize excavation costs.
    
2. **Visual Engineering:** Copilot helped write the `Matplotlib` engine to procedurally plot river banks and water surface fills using coordinate geometry.

3. **Dockerization:** When I hit a `PYTHONPATH` resolution error during containerization, Copilot CLI helped me debug the environment variables and `__init__.py` structure to ensure true portability.

## 🛠️ Installation & Usage
1. **Clone & Install**
```bash
git clone [https://github.com/AdMub/hydro-flow-cli.git](https://github.com/AdMub/hydro-flow-cli.git)
cd hydro-flow-cli
pip install -e .
```

2. **Run the Test Suite**
```bash
hydro test-suite
```

3. **Docker Support (Production Ready)**
```bash
docker build -t hydro-flow .
docker run --rm hydro-flow design --target-q 300 --max-depth 4.0
```

## 📂 Project Structure
```
hydro-flow-cli/
├── hydro/
│   ├── simulation/    # Monte Carlo & Scipy Optimization Engines
│   ├── visualization/ # Matplotlib Plotter
│   ├── hazard/        # AI Engineering Advisor
│   └── cli.py         # Typer Application
├── tests/             # Automated Unit Tests
├── Dockerfile         # Production Container
└── requirements.txt   # Dependencies
```


Built with Python, Typer, Rich, Scipy, Matplotlib, and GitHub Copilot.


