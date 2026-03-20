# Quantum Computing

Learning quantum computing from scratch, with the end goal of implementing Shor's algorithm to factor large products of primes.

## Setup

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install cirq
```

## Learning Path

1. **Basics** (`basics.py`) — qubits, gates, superposition, entanglement, measurement
2. **Interference** — amplitude cancellation/reinforcement to bias outcomes
3. **Phase kickback** — controlled gates affecting the control qubit's phase
4. **Quantum Fourier Transform** — converting phase information into measurable bit patterns
5. **Phase estimation** — extracting the phase of a unitary operator using QFT
6. **Shor's algorithm** — period finding via phase estimation to factor integers

## Key Concepts

- Qubits start in |0⟩ and are transformed by deterministic, reversible gates (unitary matrices)
- Measurement is the only source of randomness — it collapses the state probabilistically
- The state vector has 2^n complex amplitudes for n qubits — this exponential space is why quantum computers are hard to simulate classically
- Quantum algorithms work by using interference to make the right answer likely and wrong answers unlikely
- Any quantum circuit decomposes into single-qubit rotations and CNOT gates
