# 🌊 Hydro-Flow CLI

> **The Hydrologist's Terminal Assistant**
> *Advanced open-channel flow modeling, Monte Carlo risk analysis, and hydraulic auto-design.*

![Hydro-Flow Demo](https://placehold.co/800x400?text=Hydro-Flow+Visual+Output)
*(Replace this with your actual 'risk_distribution.png' or 'cross_section.png' after you upload them)*

## 🚀 Overview
**Hydro-Flow CLI** is an AI-augmented command-line tool designed to bring HEC-RAS caliber hydrology to the terminal. While most CLI tools are simple calculators, Hydro-Flow helps engineers **design** channels, **visualize** flood risks, and **stress-test** infrastructure using statistical simulations.

Battle-tested on the **Ona River Basin** (Nigeria), it empowers engineers to perform complex geospatial and hydraulic analysis without leaving the command line.

## ✨ Key Features

### 🤖 Auto-Design (Inverse Solver)
Solves the "Inverse Hydraulic Problem" using **Scipy Optimization**. Instead of guessing dimensions, Hydro-Flow calculates the *exact* minimum channel width required to handle a target flood using the **Newton-Raphson method**.
```bash
hydro design --target-q 500 --max-depth 5.0
# ✅ OPTIMAL DESIGN FOUND: Recommended Width: 8.79 m
```

## 🎲 Monte Carlo Stress Testing
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


