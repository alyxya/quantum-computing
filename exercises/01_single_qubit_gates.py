"""Single-qubit gates and measurement. Learn how individual gates transform qubit states."""

from utils import show, simulator
import cirq
import numpy as np

# ============================================================
# REFERENCE: Single-qubit gate actions
# ============================================================
# H (Hadamard):
#   |0⟩ → (|0⟩ + |1⟩) / √2
#   |1⟩ → (|0⟩ - |1⟩) / √2
#
# X (NOT / Pauli-X):
#   |0⟩ → |1⟩
#   |1⟩ → |0⟩
#
# Z (Pauli-Z):
#   |0⟩ → |0⟩
#   |1⟩ → -|1⟩
#
# S (quarter-turn / √Z):
#   |0⟩ → |0⟩
#   |1⟩ → i|1⟩
# ============================================================


# ============================================================
# EXERCISE 1: X then H
# ============================================================
# Apply X to flip |0⟩ to |1⟩, then apply H.
# What does H do to |1⟩?
# PREDICT: what is the state vector?

print("=" * 50)
print("EXERCISE 1: X then H")
print("=" * 50)
print("PREDICT: what is the state vector after X then H?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.X(q0),
    cirq.H(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 2: H then X
# ============================================================
# Now reverse the order: apply H first, then X.
# Does the order matter? Compare with Exercise 1.
# PREDICT: what is the state vector?

print("=" * 50)
print("EXERCISE 2: H then X")
print("=" * 50)
print("PREDICT: what is the state vector after H then X?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.X(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 3: H then Z then measure
# ============================================================
# Apply H to create a superposition, then Z to flip the phase of |1⟩.
# Does the phase change affect measurement probabilities?
# PREDICT: what will the measurement histogram look like?

print("=" * 50)
print("EXERCISE 3: H then Z then measure")
print("=" * 50)
print("PREDICT: what are the measurement probabilities?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.Z(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 4: H-Z-H sandwich
# ============================================================
# Apply H, then Z, then H again. This is the H-Z-H "sandwich".
# PREDICT: what is the final state? Is it deterministic or random?

print("=" * 50)
print("EXERCISE 4: H-Z-H sandwich")
print("=" * 50)
print("PREDICT: what state does H-Z-H produce from |0⟩?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.Z(q0),
    cirq.H(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 5: H then S then H then measure
# ============================================================
# Replace Z (half-turn) with S (quarter-turn) in the sandwich.
# Z gave deterministic |1⟩. What does S give?
# PREDICT: what are the measurement probabilities?

print("=" * 50)
print("EXERCISE 5: H then S then H then measure")
print("=" * 50)
print("PREDICT: what are the measurement probabilities?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.S(q0),
    cirq.H(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)


# ============================================================
# EXERCISE 6: Create the |−⟩ state
# ============================================================
# The |−⟩ state is (|0⟩ - |1⟩) / √2.
# Starting from |0⟩, construct this state and verify.
# PREDICT: what gates do you need? What is the state vector?

print("=" * 50)
print("EXERCISE 6: Create the |−⟩ state")
print("=" * 50)
print("PREDICT: what gates produce (|0⟩ - |1⟩)/√2?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
circuit = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.Z(q0),
    cirq.measure(q0, key='result'),
])
show(circuit)
