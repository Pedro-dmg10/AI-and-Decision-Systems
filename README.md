# Berth Allocation Problem (BAP) Solver

##  Overview

This project addresses the **Berth Allocation Problem (BAP)** in container terminals, where multiple vessels must be scheduled for processing at limited quay space. The primary objective is to **minimize the total weighted flow time** across all vessels, considering their size, arrival time, processing time, and importance.

The project is implemented in **Python** and divided into three progressive assignments:

1. **Input parsing and validation**
2. **Uninformed search-based scheduling**
3. **Informed search with heuristics for optimization**

---

##  Problem Description

The berth is modeled as a sequence of `S` discrete sections:  
`0, 1, ..., S-1`.

There are `N` vessels, each with the following parameters:

- `aᵢ`: Arrival time
- `pᵢ`: Processing time
- `sᵢ`: Size (number of berth sections)
- `wᵢ`: Weight (importance)

###  Constraints

- Only one quay is available.
- Each vessel, once moored, occupies consecutive sections and cannot move until processing is completed.
- Each berth section can host at most one vessel at a time.
- Time and space are discretized into integers.

###  Objective

Minimize the **total weighted flow time**:

\[
F = \sum_{i=0}^{N-1} w_i \cdot f_i \quad \text{where} \quad f_i = c_i - a_i
\]

Here:
- `fᵢ` is the flow time (departure - arrival)
- `cᵢ` is the departure time (`cᵢ = uᵢ + pᵢ`)
- `uᵢ` is the start time of processing

---

##  Features

- Read and parse problem instances from input files
- Represent vessel scheduling states
- Validate constraints and compute objective cost
- Solve using:
-  **Uninformed search** (Assignment 2)
-  **Informed search** with heuristics (Assignment 3)
- Output a valid berth schedule


