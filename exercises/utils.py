"""Shared utilities for quantum computing exercises."""

import cirq
import numpy as np

simulator = cirq.Simulator()


def show(circuit, repetitions=1000, label=None):
    """Show the state vector before measurement, then sample.

    Args:
        circuit: A cirq.Circuit, optionally containing measurements.
        repetitions: Number of times to sample (default 1000).
        label: Optional header label to print.
    """
    if label:
        print(f"--- {label} ---")

    # Get gates-only circuit (no measurements) for state vector
    gates_only = cirq.Circuit(
        op for moment in circuit for op in moment
        if not cirq.is_measurement(op)
    )
    # Use all qubits from the full circuit so idle qubits are included
    all_qubits = sorted(circuit.all_qubits())
    result = simulator.simulate(gates_only, qubit_order=all_qubits)
    sv = np.round(result.final_state_vector, 3)
    print(f"Circuit:\n{circuit}\n")
    print(f"State vector: {sv}")

    # Show probabilities
    probs = np.abs(sv) ** 2
    n_qubits = int(np.log2(len(sv)))
    labels = [format(i, f'0{n_qubits}b') for i in range(len(sv))]
    nonzero = [(l, p) for l, p in zip(labels, probs) if p > 0.001]
    print(f"Probabilities: {', '.join(f'|{l}⟩={p:.1%}' for l, p in nonzero)}")

    # Run measurements if circuit has them
    if any(cirq.is_measurement(op) for moment in circuit for op in moment):
        samples = simulator.run(circuit, repetitions=repetitions)
        for key in sorted(samples.measurements.keys()):
            print(f"Measurements ({repetitions}x) [{key}]: {samples.histogram(key=key)}")
    print()
