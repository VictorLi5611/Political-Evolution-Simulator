[![Contributors][contributors-shield1]][contributors-url1]

<p align="center">
  <h2 align="center">Political Evolution Simulator</h2>
  <h3 align="center">Modeling Selectorate Theory with Evolving Candidate Strategies</h3>
</p>

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#about-the-project">About the Project</a></li>
    <li><a href="#features">Features</a></li>
    <li>
      <a href="#technical-overview">Technical Overview</a>
      <ul>
        <li><a href="#voter-model">Voter Model</a></li>
        <li><a href="#candidate-strategy">Candidate Strategy</a></li>
        <li><a href="#evolutionary-dynamics">Evolutionary Dynamics</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#file-organization">File Organization</a></li>
    <li><a href="#author">Author</a></li>
  </ol>
</details>

## About The Project

This Python-based simulator extends **Selectorate Theory** by integrating **evolutionary game theory**, **risk-sensitive voting behavior**, and **ideologically biased voter modeling**. It explores how political leaders maintain power by dynamically adapting their strategies for public/private goods allocation, under constraints of partial voter observability and coalition beliefs.

The simulator models iterative election cycles where candidate strategies evolve based on electoral fitness, voter expectations, and ideological alignment. It is designed for academic experimentation, political modeling, and reinforcement learning extensions.

---

## Features

- Ideological voter modeling with risk profiles (safe-seeking, risk-seeking)
- Dynamic allocation of public and private goods by candidates
- Evolutionary update rules with Gaussian mutation
- Support for fixed or mutating ideological platforms
- Coalition formation and strategic voting under uncertainty

---

## Technical Overview

### Voter Model

- Each voter has:
  - Ideological position `p_i ∈ [0,100]`
  - Risk profile: risk-seeking or safe-seeking
- Voters cast ballots based on:
  - Policy proximity: `-|p_i - p(c)|^2`
  - Public goods: `α_c × (R / |V|)`
  - Private goods: `(1 - α_c) × (R / |W_c|)` if included in candidate’s coalition

### Candidate Strategy

- Each candidate has:
  - Ideological position `p(c)`
  - Resource strategy `π_c = (α_c, 1 - α_c)`
- Resources `R` are divided:
  - `α_c` fraction to all voters (public goods)
  - `1 - α_c` to expected supporters (private goods)
- Winning coalition `W_c ⊆ S_c` is formed from supporters

### Evolutionary Dynamics

- After each round:
  - The candidate with the largest viable coalition is elected
  - Losers are replaced by mutated copies of the winner
- Mutation rules:
  - `α_c' = α_c + ε, ε ∼ N(0, σ²)`
  - `p(c)' = p(c) + η, η ∼ N(0, τ²)` (optional)
- Fitness Function:
  - `f(c) = |W_c|` if elected, 0 otherwise

---

## Getting Started

### Prerequisites

- Python 3.7+
- `numpy`

Install dependencies using:

```bash
pip install numpy
```

### Installation

1. Clone the repository by running this command in the course VM terminal:
   ```sh
   git clone https://github.com/VictorLi5611/political-evolution-sim.git
   cd political-evolution-sim
   ```
2. Run the simulation:
   ```bash
   python3 simulation.py
   ```
3. Adjust parameters inside `simulation.py` to configure:

- Number of voters and candidates
- Mutation standard deviations
- Policy mode (fixed vs. evolving)
- Coalition thresholding and risk models

### File Organization

```bash
political-evolution-sim/
├── simulation.py         # Main simulation script
├── README.md             # Project README
```

### Author

**Victor Li**  
GitHub: [VictorLi5611](https://github.com/VictorLi5611)  
MSc Computer Science (Data Science)  
Carleton University  
Research interests: Multi-agent systems, political modeling, reinforcement learning

[contributors-shield1]: https://img.shields.io/static/v1?label=Contributor&message=Victor_Li&color=afff75&style=for-the-badge
[contributors-url1]: https://github.com/victorli5611
