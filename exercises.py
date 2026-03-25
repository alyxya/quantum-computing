"""
Quantum Computing Exercises
============================
Work through these in order. Each exercise asks you to:
  1. PREDICT what the state vector / measurement results will be
  2. Write the circuit in Cirq
  3. Run it and check your prediction

The helper function show() prints the state vector and measurement histogram
so you can verify your answers.

Useful reference:
  - H (Hadamard): |0⟩ → (|0⟩+|1⟩)/√2,  |1⟩ → (|0⟩-|1⟩)/√2
  - X (NOT):      |0⟩ → |1⟩,             |1⟩ → |0⟩
  - Z (phase):    |0⟩ → |0⟩,             |1⟩ → -|1⟩
  - CNOT:         flips target if control is |1⟩
  - State vector order for 2 qubits: [|00⟩, |01⟩, |10⟩, |11⟩]
"""

import cirq
import numpy as np

simulator = cirq.Simulator()

def show(circuit, repetitions=1000):
    """Show the state vector before measurement, then sample."""
    # Get gates-only circuit (no measurements) for state vector
    gates_only = cirq.Circuit(
        op for moment in circuit for op in moment
        if not cirq.is_measurement(op)
    )
    result = simulator.simulate(gates_only)
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
        print(f"Measurements ({repetitions}x): {samples.histogram(key='result')}")
    print()


# ============================================================
# EXERCISE 1: Single qubit gates
# ============================================================
# Build a circuit that applies X then H to a single qubit.
# Before coding: what is the state vector after X? After X then H?
#
# Hint: X turns |0⟩ into |1⟩. Then H acts on |1⟩.

print("=" * 50)
print("EXERCISE 1: X then H on one qubit")
print("=" * 50)
print("TODO: predict the final state, then uncomment the code\n")

q0 = cirq.LineQubit(0)

# circuit = cirq.Circuit([
#     cirq.X(q0),
#     cirq.H(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: Order matters
# ============================================================
# Now do H then X on the same qubit.
# Is the result different from Exercise 1? Predict first!

print("=" * 50)
print("EXERCISE 2: H then X on one qubit")
print("=" * 50)
print("TODO: predict the final state, then uncomment the code\n")

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 3: Phase matters
# ============================================================
# Apply H, then Z, then measure.
# Z doesn't change probabilities on its own (|0⟩→|0⟩, |1⟩→-|1⟩).
# So will this measure differently from just H alone?
#
# Then try: H, Z, H, measure. Now what happens?

print("=" * 50)
print("EXERCISE 3a: H then Z then measure")
print("=" * 50)
print("TODO: predict, then uncomment\n")

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.Z(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)

print("=" * 50)
print("EXERCISE 3b: H then Z then H then measure")
print("=" * 50)
print("TODO: predict, then uncomment\n")

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.Z(q0),
#     cirq.H(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 4: Two qubits, no entanglement
# ============================================================
# Apply H to q0 only. Leave q1 alone. Measure both.
# What are the possible outcomes? What are the probabilities?

print("=" * 50)
print("EXERCISE 4: H on q0, nothing on q1")
print("=" * 50)
print("TODO: predict the 4-element state vector, then uncomment\n")

q0, q1 = cirq.LineQubit.range(2)

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 5: Creating entanglement
# ============================================================
# Apply H to q0, then CNOT(q0, q1). Measure both.
# This is the Bell state from basics.py — but now predict the
# state vector yourself: which of the 4 amplitudes are nonzero?

print("=" * 50)
print("EXERCISE 5: Bell state")
print("=" * 50)
print("TODO: predict the 4-element state vector, then uncomment\n")

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 6: The other Bell states
# ============================================================
# There are 4 Bell states. Exercise 5 made (|00⟩+|11⟩)/√2.
# Can you make these three?
#   a) (|00⟩ - |11⟩) / √2
#   b) (|01⟩ + |10⟩) / √2
#   c) (|01⟩ - |10⟩) / √2
#
# Hint: you only need H, X, Z, and CNOT.

print("=" * 50)
print("EXERCISE 6: The other three Bell states")
print("=" * 50)
print("TODO: build circuits for each, verify with show()\n")

# circuit_a = cirq.Circuit([
#     # TODO: (|00⟩ - |11⟩) / √2
# ])
# show(circuit_a)

# circuit_b = cirq.Circuit([
#     # TODO: (|01⟩ + |10⟩) / √2
# ])
# show(circuit_b)

# circuit_c = cirq.Circuit([
#     # TODO: (|01⟩ - |10⟩) / √2
# ])
# show(circuit_c)


# ============================================================
# EXERCISE 7: Predict the histogram
# ============================================================
# Three qubits. H on all three. Measure all three.
# How many possible outcomes? What does the histogram look like?

print("=" * 50)
print("EXERCISE 7: Superposition on 3 qubits")
print("=" * 50)
print("TODO: predict, then uncomment\n")

q0, q1, q2 = cirq.LineQubit.range(3)

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.H(q1),
#     cirq.H(q2),
#     cirq.measure(q0, q1, q2, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 8: Interference with two qubits
# ============================================================
# Build this circuit and predict the outcome:
#   H on q0, CNOT(q0,q1), H on q0, measure q0
#
# This is NOT the same as H,H (which cancels). The CNOT
# in between entangles q0 with q1. Does q0 still return to |0⟩?

print("=" * 50)
print("EXERCISE 8: Does CNOT break the H-H cancellation?")
print("=" * 50)
print("TODO: predict, then uncomment\n")

q0, q1 = cirq.LineQubit.range(2)

# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.H(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)
