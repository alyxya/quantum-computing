# Quantum Computing: From Qubits to Shor's Algorithm

A hands-on learning path using Google Cirq. Every file runs and produces output.

## Setup

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install cirq numpy
```

## Reference

Quick-reference material you can consult while working through exercises:

- `reference/gates.py` — single-qubit gates (X, Y, Z, H, S, T, rotations)
- `reference/multi_qubit.py` — CNOT, CZ, SWAP, tensor products, controlled gates
- `reference/circuits.py` — Bell states, GHZ, interference, Deutsch's algorithm

Run any reference file directly: `python reference/gates.py`

## Exercises

Work through in order. Each exercise asks you to predict the outcome first, then uncomment code to verify.

```bash
cd exercises
python 01_single_qubit_gates.py
```

| # | File | Topics |
|---|------|--------|
| 1 | `01_single_qubit_gates.py` | X, H, Z, S gates; measurement; non-commutativity |
| 2 | `02_multi_qubit_operations.py` | Tensor products, CNOT, CZ, SWAP, multi-qubit state vectors |
| 3 | `03_entanglement.py` | Bell states, GHZ state, entanglement vs interference |
| 4 | `04_interference.py` | H-Z-H, sqrt(X)-CZ-sqrt(X), Deutsch's algorithm |
| 5 | `05_phase_kickback.py` | Controlled gates, eigenvalue kickback |
| 6 | `06_quantum_fourier_transform.py` | QFT circuits for 1-3 qubits, inverse QFT |
| 7 | `07_phase_estimation.py` | QPE with Z, S, T gates; imperfect phases |
| 8 | `08_shors_algorithm.py` | Period finding, modular exponentiation, factoring N=15 |

## Key Concepts

- Qubits start in |0⟩ and are transformed by deterministic, reversible gates (unitary matrices)
- Measurement is the only source of randomness — it collapses the state probabilistically
- The state vector has 2^n complex amplitudes for n qubits — this exponential space is why quantum computers are hard to simulate classically
- Quantum algorithms work by using interference to make the right answer likely and wrong answers unlikely
- Any quantum circuit decomposes into single-qubit rotations and CNOT gates
