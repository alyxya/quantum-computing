"""Entanglement and Bell states. Create and verify quantum correlations."""

from utils import show, simulator
import cirq
import numpy as np

# ============================================================
# REFERENCE: The four Bell states
# ============================================================
# |Φ+⟩ = (|00⟩ + |11⟩) / √2   state vector: [0.707, 0, 0, 0.707]
# |Φ−⟩ = (|00⟩ - |11⟩) / √2   state vector: [0.707, 0, 0, -0.707]
# |Ψ+⟩ = (|01⟩ + |10⟩) / √2   state vector: [0, 0.707, 0.707, 0]
# |Ψ−⟩ = (|01⟩ - |10⟩) / √2   state vector: [0, 0.707, -0.707, 0]
#
# Bell states are maximally entangled: measuring one qubit
# instantly determines the other, but each individual qubit
# is completely random (50/50).
# ============================================================


# ============================================================
# EXERCISE 1: Create Bell state |Φ+⟩
# ============================================================
# The most common entangled state: (|00⟩ + |11⟩) / √2.
# Apply H to q0, then CNOT with q0 as control and q1 as target.
# PREDICT: what is the state vector?

print("=" * 50)
print("EXERCISE 1: Create Bell state |Φ+⟩")
print("=" * 50)
print("PREDICT: what is the state vector after H then CNOT?\n")

q0, q1 = cirq.LineQubit.range(2)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 2: Create Bell state |Φ−⟩
# ============================================================
# Target: (|00⟩ - |11⟩) / √2.
# Start from |Φ+⟩ and add one gate to flip the sign of |11⟩.
# PREDICT: which gate do you add, and where?

print("=" * 50)
print("EXERCISE 2: Create Bell state |Φ−⟩")
print("=" * 50)
print("PREDICT: what gate converts |Φ+⟩ to |Φ−⟩?\n")

q0, q1 = cirq.LineQubit.range(2)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.Z(q0),
    cirq.measure(q0, q1, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 3: Create Bell state |Ψ+⟩
# ============================================================
# Target: (|01⟩ + |10⟩) / √2.
# Start from |Φ+⟩ and add one gate to swap |0⟩ and |1⟩ on one qubit.
# PREDICT: which gate and which qubit?

print("=" * 50)
print("EXERCISE 3: Create Bell state |Ψ+⟩")
print("=" * 50)
print("PREDICT: what gate converts |Φ+⟩ to |Ψ+⟩?\n")

q0, q1 = cirq.LineQubit.range(2)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.X(q1),
    cirq.measure(q0, q1, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 4: Create Bell state |Ψ−⟩
# ============================================================
# Target: (|01⟩ - |10⟩) / √2.
# Combine the techniques from Exercises 2 and 3.
# PREDICT: what is the state vector?

print("=" * 50)
print("EXERCISE 4: Create Bell state |Ψ−⟩")
print("=" * 50)
print("PREDICT: what gates convert |Φ+⟩ to |Ψ−⟩?\n")

q0, q1 = cirq.LineQubit.range(2)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.Z(q0),
    cirq.CNOT(q0, q1),
    cirq.X(q1),
    cirq.measure(q0, q1, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 5: GHZ state (3 qubits)
# ============================================================
# Create the GHZ state: (|000⟩ + |111⟩) / √2.
# This is the 3-qubit generalization of |Φ+⟩.
# PREDICT: what is the 8-element state vector?

print("=" * 50)
print("EXERCISE 5: GHZ state (3 qubits)")
print("=" * 50)
print("PREDICT: what is the 8-element state vector?\n")

q0, q1, q2 = cirq.LineQubit.range(3)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.CNOT(q1, q2),
    cirq.measure(q0, q1, q2, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 6: Entanglement breaks interference
# ============================================================
# Without entanglement: H then H cancels back to |0⟩ (Exercise 01-4 idea).
# With entanglement: H, CNOT(q0,q1), H on q0, measure q0.
# PREDICT: does q0 still return to |0⟩ deterministically?

print("=" * 50)
print("EXERCISE 6: Entanglement breaks interference")
print("=" * 50)
print("PREDICT: is q0 deterministic or 50/50 after H-CNOT-H?\n")

q0, q1 = cirq.LineQubit.range(2)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.H(q0),
    cirq.measure(q0, key='q0'),
    cirq.measure(q1, key='q1'),
])
show(circuit)
