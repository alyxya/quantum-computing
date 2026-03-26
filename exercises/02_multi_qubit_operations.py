"""Multi-qubit operations and tensor products. Learn how qubits combine and interact."""

from utils import show, simulator
import cirq
import numpy as np

# ============================================================
# REFERENCE: Multi-qubit state vector ordering (Cirq convention)
# ============================================================
# For 2 qubits (q0, q1), Cirq uses q0 as the MOST significant bit.
# State vector indices: [|00⟩, |01⟩, |10⟩, |11⟩]
#   index 0 = |q0=0, q1=0⟩
#   index 1 = |q0=0, q1=1⟩
#   index 2 = |q0=1, q1=0⟩
#   index 3 = |q0=1, q1=1⟩
#
# CNOT (controlled-X) truth table:
#   |control, target⟩ → |control, target ⊕ control⟩
#   |00⟩ → |00⟩
#   |01⟩ → |01⟩
#   |10⟩ → |11⟩   (control=1 flips target)
#   |11⟩ → |10⟩   (control=1 flips target)
# ============================================================


# ============================================================
# EXERCISE 1: H on q0, nothing on q1
# ============================================================
# Two qubits, but only apply H to q0. What is the 4-element state vector?
# PREDICT: what are the four amplitudes?
#
# Hint: H|0⟩ ⊗ |0⟩ = (|0⟩+|1⟩)/√2 ⊗ |0⟩ = (|00⟩+|10⟩)/√2.
# So amplitudes at |00⟩ and |10⟩ are 1/√2 ≈ 0.707, rest are 0.

print("=" * 50)
print("EXERCISE 1: H on q0, nothing on q1")
print("=" * 50)
print("PREDICT: what is the 4-element state vector?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: H on both qubits
# ============================================================
# Apply H to both q0 and q1. What is the state vector?
# PREDICT: what are the four amplitudes?
#
# Hint: H|0⟩ ⊗ H|0⟩ = (|0⟩+|1⟩)/√2 ⊗ (|0⟩+|1⟩)/√2
# = (|00⟩+|01⟩+|10⟩+|11⟩) / 2.
# Each amplitude is 1/2 = 0.5.

print("=" * 50)
print("EXERCISE 2: H on both qubits")
print("=" * 50)
print("PREDICT: what are the four amplitudes?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.H(q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 3: CNOT truth table
# ============================================================
# Verify the CNOT truth table by trying each computational basis state.
# Apply X gates to prepare the input, then CNOT, then check the output.
# PREDICT: for each input |q0,q1⟩, what is the output?
#
# Hint: CNOT(control=q0, target=q1) flips q1 when q0=1.
# Test all four inputs: |00⟩, |01⟩, |10⟩, |11⟩.

print("=" * 50)
print("EXERCISE 3: CNOT truth table")
print("=" * 50)
print("PREDICT: what does CNOT output for each basis state?\n")

# q0, q1 = cirq.LineQubit.range(2)

# # Input |00⟩
# circuit_00 = cirq.Circuit([
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_00, label='CNOT on |00⟩')

# # Input |01⟩
# circuit_01 = cirq.Circuit([
#     cirq.X(q1),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_01, label='CNOT on |01⟩')

# # Input |10⟩
# circuit_10 = cirq.Circuit([
#     cirq.X(q0),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_10, label='CNOT on |10⟩')

# # Input |11⟩
# circuit_11 = cirq.Circuit([
#     cirq.X(q0),
#     cirq.X(q1),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_11, label='CNOT on |11⟩')


# ============================================================
# EXERCISE 4: CZ vs CNOT
# ============================================================
# Compare CZ and CNOT when applied to H(q0) ⊗ |1⟩.
# PREDICT: how do the output state vectors differ?
#
# Hint: prepare q0 with H and q1 with X (to get |1⟩).
# CNOT flips the target qubit when control is |1⟩.
# CZ applies a phase of -1 to |11⟩ only (no bit flip).
# The two gates have the same effect on probabilities here,
# but the state vectors are different.

print("=" * 50)
print("EXERCISE 4: CZ vs CNOT")
print("=" * 50)
print("PREDICT: how do CZ and CNOT outputs differ?\n")

# q0, q1 = cirq.LineQubit.range(2)

# circuit_cnot = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q1),
#     cirq.CNOT(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_cnot, label='CNOT on H|0⟩ ⊗ |1⟩')

# circuit_cz = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q1),
#     cirq.CZ(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_cz, label='CZ on H|0⟩ ⊗ |1⟩')


# ============================================================
# EXERCISE 5: SWAP gate
# ============================================================
# Prepare q0 in |1⟩ and q1 in |0⟩, then apply SWAP.
# PREDICT: what is the state vector after SWAP?
#
# Hint: SWAP exchanges the states of two qubits.
# |10⟩ should become |01⟩.
# State vector [0, 1, 0, 0] means |01⟩.

print("=" * 50)
print("EXERCISE 5: SWAP gate")
print("=" * 50)
print("PREDICT: what is the state after swapping |10⟩?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.X(q0),
#     cirq.SWAP(q0, q1),
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 6: Three-qubit equal superposition
# ============================================================
# Apply H to all three qubits. What is the 8-element state vector?
# PREDICT: what is each amplitude?
#
# Hint: H|0⟩ ⊗ H|0⟩ ⊗ H|0⟩ = equal superposition of all 8 basis states.
# Each amplitude is 1/√8 = 1/(2√2) ≈ 0.354.

print("=" * 50)
print("EXERCISE 6: Three-qubit equal superposition")
print("=" * 50)
print("PREDICT: what are the 8 amplitudes?\n")

# q0, q1, q2 = cirq.LineQubit.range(3)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.H(q1),
#     cirq.H(q2),
#     cirq.measure(q0, q1, q2, key='result'),
# ])
# show(circuit)
