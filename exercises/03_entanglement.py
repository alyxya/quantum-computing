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
#
# Hint: H|0⟩ = (|0⟩+|1⟩)/√2. Then CNOT copies q0 into q1:
# (|0⟩+|1⟩)/√2 ⊗ |0⟩ → (|00⟩+|11⟩)/√2.

print("=" * 50)
print("EXERCISE 1: Create Bell state |Φ+⟩")
print("=" * 50)
print("PREDICT: what is the state vector after H then CNOT?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: Create Bell state |Φ−⟩
# ============================================================
# Target: (|00⟩ - |11⟩) / √2.
# Start from |Φ+⟩ and add one gate to flip the sign of |11⟩.
# PREDICT: which gate do you add, and where?
#
# Hint: Z on q0 maps |0⟩→|0⟩ and |1⟩→-|1⟩.
# Apply Z to q0 after creating |Φ+⟩, or equivalently,
# apply Z to q0 before the CNOT (after H).

print("=" * 50)
print("EXERCISE 2: Create Bell state |Φ−⟩")
print("=" * 50)
print("PREDICT: what gate converts |Φ+⟩ to |Φ−⟩?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.Z(q0),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 3: Create Bell state |Ψ+⟩
# ============================================================
# Target: (|01⟩ + |10⟩) / √2.
# Start from |Φ+⟩ and add one gate to swap |0⟩ and |1⟩ on one qubit.
# PREDICT: which gate and which qubit?
#
# Hint: X on q1 flips q1, turning |00⟩→|01⟩ and |11⟩→|10⟩.

print("=" * 50)
print("EXERCISE 3: Create Bell state |Ψ+⟩")
print("=" * 50)
print("PREDICT: what gate converts |Φ+⟩ to |Ψ+⟩?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.X(q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 4: Create Bell state |Ψ−⟩
# ============================================================
# Target: (|01⟩ - |10⟩) / √2.
# Combine the techniques from Exercises 2 and 3.
# PREDICT: what is the state vector?
#
# Hint: you need both a phase flip and a bit flip.
# Apply Z on q0 and X on q1 after creating |Φ+⟩.

print("=" * 50)
print("EXERCISE 4: Create Bell state |Ψ−⟩")
print("=" * 50)
print("PREDICT: what gates convert |Φ+⟩ to |Ψ−⟩?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.Z(q0),
#     cirq.X(q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 5: GHZ state (3 qubits)
# ============================================================
# Create the GHZ state: (|000⟩ + |111⟩) / √2.
# This is the 3-qubit generalization of |Φ+⟩.
# PREDICT: what is the 8-element state vector?
#
# Hint: H on q0, then CNOT(q0,q1), then CNOT(q0,q2).
# The CNOT cascade copies q0's state to q1 and q2.
# Only |000⟩ and |111⟩ have nonzero amplitudes.

print("=" * 50)
print("EXERCISE 5: GHZ state (3 qubits)")
print("=" * 50)
print("PREDICT: what is the 8-element state vector?\n")

# q0, q1, q2 = cirq.LineQubit.range(3)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.CNOT(q0, q2),
#     cirq.measure(q0, q1, q2, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 6: Entanglement breaks interference
# ============================================================
# Without entanglement: H then H cancels back to |0⟩ (Exercise 01-4 idea).
# With entanglement: H, CNOT(q0,q1), H on q0, measure q0.
# PREDICT: does q0 still return to |0⟩ deterministically?
#
# Hint: the CNOT entangles q0 with q1 between the two H gates.
# After H-CNOT: (|00⟩+|11⟩)/√2.
# After second H on q0: (|+0⟩+|−1⟩)/√2 — expand this out.
# q0 is no longer in a pure state on its own; it's 50/50.
# Entanglement with q1 destroys the interference on q0.

print("=" * 50)
print("EXERCISE 6: Entanglement breaks interference")
print("=" * 50)
print("PREDICT: is q0 deterministic or 50/50 after H-CNOT-H?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.H(q0),
#     cirq.measure(q0, key='q0'),
#     cirq.measure(q1, key='q1'),
# ])
# show(circuit)
