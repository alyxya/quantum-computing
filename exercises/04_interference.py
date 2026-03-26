"""Interference patterns. How amplitudes add and cancel to produce deterministic outcomes."""

from utils import show, simulator
import cirq
import numpy as np

# ============================================================
# REFERENCE: Interference in quantum computing
# ============================================================
# Quantum gates manipulate amplitudes, not probabilities.
# Amplitudes can be positive, negative, or complex.
# When paths recombine:
#   - Same sign → constructive interference (amplitudes add)
#   - Opposite sign → destructive interference (amplitudes cancel)
# This is the key to quantum speedups: arrange circuits so that
# wrong answers cancel and correct answers reinforce.
# ============================================================


# ============================================================
# EXERCISE 1: Double Hadamard (H·H = Identity)
# ============================================================
# Apply H twice to |0⟩. What happens?
# PREDICT: what is the final state?

print("=" * 50)
print("EXERCISE 1: Double Hadamard (H·H = Identity)")
print("=" * 50)
print("PREDICT: what state does H·H produce from |0⟩?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
# circuit = cirq.Circuit([
#     # YOUR GATES HERE
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: H-Z-H equals X
# ============================================================
# We saw in Exercise 01-4 that H-Z-H on |0⟩ gives |1⟩.
# Is H·Z·H actually the same as the X gate for ANY input?
# Test on both |0⟩ and |1⟩ and compare with X.
# PREDICT: are the state vectors identical?

print("=" * 50)
print("EXERCISE 2: H-Z-H equals X")
print("=" * 50)
print("PREDICT: does H·Z·H give the same result as X?\n")

q0 = cirq.LineQubit(0)

# H-Z-H on |0⟩
# circuit_hzh_0 = cirq.Circuit([
#     # YOUR CIRCUIT HERE
# ])
# show(circuit_hzh_0, label='H-Z-H on |0⟩')

# X on |0⟩
# circuit_x_0 = cirq.Circuit([
#     # YOUR CIRCUIT HERE
# ])
# show(circuit_x_0, label='X on |0⟩')

# H-Z-H on |1⟩
# circuit_hzh_1 = cirq.Circuit([
#     # YOUR CIRCUIT HERE
# ])
# show(circuit_hzh_1, label='H-Z-H on |1⟩')

# X on |1⟩
# circuit_x_1 = cirq.Circuit([
#     # YOUR CIRCUIT HERE
# ])
# show(circuit_x_1, label='X on |1⟩')


# ============================================================
# EXERCISE 3: H-S-H — quarter-turn interference
# ============================================================
# Replace Z (half-turn, phase of -1) with S (quarter-turn, phase of i).
# PREDICT: what is the state vector after H-S-H on |0⟩?
# Is the result deterministic, 50/50, or something else?

print("=" * 50)
print("EXERCISE 3: H-S-H — quarter-turn interference")
print("=" * 50)
print("PREDICT: what is the state vector after H-S-H?\n")

q0 = cirq.LineQubit(0)
# Build your circuit here:
# circuit = cirq.Circuit([
#     # YOUR GATES HERE
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 4: √X-CZ-√X circuit
# ============================================================
# Two qubits. Apply √X to both, then CZ, then √X to both again.
# √X is a "half NOT" gate: applying it twice gives X.
# PREDICT: what are the measurement probabilities?
#
# Compare both circuits to see the effect of CZ.

print("=" * 50)
print("EXERCISE 4: √X-CZ-√X circuit")
print("=" * 50)
print("PREDICT: what are the probabilities with and without CZ?\n")

q0, q1 = cirq.LineQubit.range(2)

# Without CZ: √X √X = X on each qubit → what state?
# circuit_no_cz = cirq.Circuit([
#     # YOUR CIRCUIT HERE
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_no_cz, label='Without CZ: √X·√X = X on each qubit')

# With CZ: interference is disrupted
# circuit_with_cz = cirq.Circuit([
#     # YOUR CIRCUIT HERE
#     cirq.measure(q0, q1, key='result'),
# ])
# show(circuit_with_cz, label='With CZ: interference disrupted')


# ============================================================
# EXERCISE 5: Deutsch's algorithm — constant function f(x) = 0
# ============================================================
# Deutsch's algorithm determines if a function f:{0,1}→{0,1} is
# constant (f(0)=f(1)) or balanced (f(0)≠f(1)) with ONE query.
#
# Setup: two qubits. q_in is the input, q_out is the output.
#   1. Prepare q_out in |1⟩ (apply X)
#   2. Apply H to both qubits
#   3. Apply the oracle U_f: |x,y⟩ → |x, y⊕f(x)⟩
#   4. Apply H to q_in
#   5. Measure q_in: 0 = constant, 1 = balanced
#
# Oracle for f(x) = 0: the identity (do nothing). y⊕0 = y.
# PREDICT: what does q_in measure?

print("=" * 50)
print("EXERCISE 5: Deutsch's algorithm — f(x) = 0 (constant)")
print("=" * 50)
print("PREDICT: what does q_in measure? (0=constant, 1=balanced)\n")

q_in, q_out = cirq.LineQubit.range(2)
# Build your circuit here:
# circuit = cirq.Circuit([
#     # Step 1: prepare |01⟩
#     # Step 2: apply H to both
#     # Step 3: oracle for f(x) = 0
#     # Step 4: apply H to q_in
#     # Step 5: measure q_in
#     # YOUR CIRCUIT HERE
# ])
# show(circuit)


# ============================================================
# EXERCISE 6: Deutsch's algorithm — balanced function f(x) = x
# ============================================================
# Oracle for f(x) = x: apply CNOT(q_in, q_out).
# When q_in=0, target unchanged. When q_in=1, target flips.
# This implements |x,y⟩ → |x, y⊕x⟩.
# PREDICT: what does q_in measure?

print("=" * 50)
print("EXERCISE 6: Deutsch's algorithm — f(x) = x (balanced)")
print("=" * 50)
print("PREDICT: what does q_in measure? (0=constant, 1=balanced)\n")

q_in, q_out = cirq.LineQubit.range(2)
# Build your circuit here:
# circuit = cirq.Circuit([
#     # Step 1: prepare |01⟩
#     # Step 2: apply H to both
#     # Step 3: oracle for f(x) = x
#     # Step 4: apply H to q_in
#     # Step 5: measure q_in
#     # YOUR CIRCUIT HERE
# ])
# show(circuit)


# ============================================================
# EXERCISE 7: Deutsch's algorithm — f(x) = NOT(x)
# ============================================================
# f(x) = 1-x: f(0)=1, f(1)=0. Is this constant or balanced?
# Design the oracle yourself.
# PREDICT: what does q_in measure?

print("=" * 50)
print("EXERCISE 7: Deutsch's algorithm — f(x) = NOT(x)")
print("=" * 50)
print("PREDICT: what does q_in measure? (0=constant, 1=balanced)\n")

q_in, q_out = cirq.LineQubit.range(2)
# Build your circuit here:
# circuit = cirq.Circuit([
#     # Step 1: prepare |01⟩
#     # Step 2: apply H to both
#     # Step 3: oracle for f(x) = 1-x
#     # Step 4: apply H to q_in
#     # Step 5: measure q_in
#     # YOUR CIRCUIT HERE
# ])
# show(circuit)
