# AI-Based Data Center Energy Audit – Simulation Module

## Role
**Balasundaram Nandaa**  
**Simulation & Scenario Analysis Lead**

## Objective
This module simulates the impact of optimization actions on a data center in order to compare baseline and optimized scenarios and validate whether the platform can achieve the target of **–25% CO₂ emissions**.

## Responsibilities
The simulation module is responsible for:

- simulating before/after energy consumption
- simulating before/after CO₂ emissions
- modeling savings for each optimization action
- combining actions into one optimized scenario
- validating whether the –25% CO₂ target is achieved
- supporting comparison tables and charts in the UI

## Files Updated
The following files were added or updated for the simulation module:

- `simulation/config.py`
- `simulation/scenario.py`
- `simulation/simulation_engine.py`
- `simulation/ui_simulation.py`

## Methodology
The simulation starts from the baseline metrics provided in the case study and applies optimization actions to estimate savings.

### Actions simulated
- **Server consolidation**
- **Virtualization**
- **Cooling optimization**

### Outputs calculated
- baseline total energy consumption
- optimized total energy consumption
- energy saved in **MWh/year**
- baseline CO₂ emissions
- optimized CO₂ emissions
- CO₂ saved in **tCO₂/year**
- total reduction percentage
- target achieved / not achieved

## Simulation Logic
Single actions are evaluated independently to measure their individual impact.

A combined scenario is then built by applying all actions together to estimate the total optimization result.

The module returns:
- `baseline`
- `single_actions`
- `combined`

## Current Result
Example result from the implemented simulation:

- **Baseline Energy:** 7884.0 MWh/year
- **Optimized Energy:** 5026.05 MWh/year
- **Energy Saved:** 2857.95 MWh/year
- **Baseline CO₂:** 449.388 t/year
- **Optimized CO₂:** 286.485 t/year
- **CO₂ Saved:** 162.903 t/year
- **Reduction Achieved:** 36.25%
- **Target Achieved:** Yes

## UI Support
The simulation module also supports frontend visualization through:
- baseline vs optimized comparison table
- savings by action table
- baseline vs optimized energy chart
- target validation display

## How to Run
Install dependencies:

```bash
pip install -r requirements.txt