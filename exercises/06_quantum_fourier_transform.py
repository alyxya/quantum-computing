"""Quantum Fourier Transform. The QFT converts phase information into
measurable bit patterns — it's the key subroutine in Shor's algorithm.

The QFT maps computational basis states to frequency basis states:

  |j> --> (1/sqrt(N)) * sum_k  e^(2*pi*i*j*k/N) |k>

For n qubits, N = 2^n. The transform is identical to the classical
Discrete Fourier Transform (DFT), but acts on quantum amplitudes and
can be computed exponentially faster: O(n^2) gates vs O(N*log(N)).

The circuit structure follows a pattern:
  - Apply H to the first qubit
  - Apply controlled phase rotations from all subsequent qubits
  - Repeat for each qubit with decreasing numbers of controlled rotations
  - Reverse the qubit order with SWAPs

The controlled rotation R_k applies a phase of e^(2*pi*i/2^k), which
in Cirq corresponds to ZPowGate(exponent=1/2^(k-1)):
  R_2 = S gate (phase pi/2)
  R_3 = T gate (phase pi/4)
  R_k = ZPowGate(exponent=1/2^(k-1))
"""

from utils import show, simulator
import cirq
import numpy as np


# ============================================================
# EXERCISE 1: QFT on 1 qubit
# ============================================================
# The 1-qubit QFT is just a Hadamard gate!
# For N=2 (one qubit), the QFT matrix is:
#   (1/sqrt(2)) * [[1, 1], [1, -1]]
# which is exactly H.
#
# Verify: apply H to |0> and to |1>.
# PREDICT: what are the state vectors?

print("=" * 50)
print("EXERCISE 1: QFT on 1 qubit")
print("=" * 50)
print("PREDICT: what are the state vectors for QFT|0> and QFT|1>?\n")

q0 = cirq.LineQubit(0)
circuit_0 = cirq.Circuit([
    # YOUR GATES HERE (QFT on |0>)
    cirq.H(q0),
])
show(circuit_0, label="QFT|0> (1 qubit)")

circuit_1 = cirq.Circuit([
    # YOUR GATES HERE (QFT on |1>)
    cirq.X(q0),
    cirq.H(q0),
])
show(circuit_1, label="QFT|1> (1 qubit)")


# ============================================================
# EXERCISE 2: QFT on 2 qubits — build by hand
# ============================================================
# The 2-qubit QFT circuit is:
#   1. H on q0
#   2. Controlled-S on q0, controlled by q1 (this is R_2)
#   3. H on q1
#   4. SWAP q0, q1 (reverse qubit order)
#
# Apply to |00> and |11>.
# PREDICT: what are the amplitudes for QFT|00> and QFT|11>?

print("=" * 50)
print("EXERCISE 2: QFT on 2 qubits — build by hand")
print("=" * 50)
print("PREDICT: what are the amplitudes for QFT|00> and QFT|11>?\n")

q0, q1 = cirq.LineQubit.range(2)

# QFT on |00>
qft2_on_00 = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.S.controlled()(q1, q0),
    cirq.H(q1),
    cirq.SWAP(q0, q1),
])
show(qft2_on_00, label="QFT|00> (2 qubits)")

# QFT on |11>
qft2_on_11 = cirq.Circuit([
    # YOUR GATES HERE (prepare |11> then apply QFT)
    cirq.X(q0),
    cirq.X(q1),
    cirq.H(q0),
    cirq.S.controlled()(q1, q0),
    cirq.H(q1),
    cirq.SWAP(q0, q1),
])
show(qft2_on_11, label="QFT|11> (2 qubits)")


# ============================================================
# EXERCISE 3: QFT on 2 qubits — verify the matrix
# ============================================================
# Build the QFT circuit (without state preparation or measurements)
# and extract its unitary matrix with cirq.unitary().
#
# Compare it to the expected 4x4 DFT matrix:
#   (1/2) * [[1,  1,  1,  1 ],
#             [1,  i, -1, -i ],
#             [1, -1,  1, -1 ],
#             [1, -i, -1,  i ]]
#
# PREDICT: does our hand-built circuit produce the correct DFT matrix?

print("=" * 50)
print("EXERCISE 3: QFT on 2 qubits — verify the matrix")
print("=" * 50)
print("PREDICT: does the circuit unitary match the DFT matrix?\n")

q0, q1 = cirq.LineQubit.range(2)
qft2_circuit = cirq.Circuit([
    # YOUR QFT GATES HERE (no state prep, no measurement)
    cirq.H(q0),
    cirq.S.controlled()(q1, q0),
    cirq.H(q1),
    cirq.SWAP(q0, q1),
])

circuit_unitary = np.round(cirq.unitary(qft2_circuit), 3)

expected_dft = 0.5 * np.array([
    [1,  1,  1,  1],
    [1,  1j, -1, -1j],
    [1, -1,  1, -1],
    [1, -1j, -1, 1j],
])
expected_dft = np.round(expected_dft, 3)

print(f"Circuit unitary:\n{circuit_unitary}\n")
print(f"Expected DFT matrix:\n{expected_dft}\n")
print(f"Matrices match: {np.allclose(circuit_unitary, expected_dft)}\n")


# ============================================================
# EXERCISE 4: QFT on 3 qubits
# ============================================================
# Extend the pattern to 3 qubits:
#   1. H on q0, controlled-S(q0) from q1, controlled-T(q0) from q2
#   2. H on q1, controlled-S(q1) from q2
#   3. H on q2
#   4. SWAP q0, q2 (reverse qubit order)
#
# Apply to |000> and |001>.
# PREDICT: what are the amplitudes for QFT|000> and QFT|001>?

print("=" * 50)
print("EXERCISE 4: QFT on 3 qubits")
print("=" * 50)
print("PREDICT: what are the amplitudes for QFT|000> and QFT|001>?\n")

q0, q1, q2 = cirq.LineQubit.range(3)

# QFT on |000>
qft3_on_000 = cirq.Circuit([
    # YOUR GATES HERE
    cirq.H(q0),
    cirq.S(q0).controlled_by(q1),
    cirq.T(q0).controlled_by(q2),
    cirq.H(q1),
    cirq.S(q1).controlled_by(q2),
    cirq.H(q2),
    cirq.SWAP(q0, q2),
])
show(qft3_on_000, label="QFT|000> (3 qubits)")

# QFT on |001>
qft3_on_001 = cirq.Circuit([
    # YOUR GATES HERE (prepare |001> then apply QFT)
    cirq.X(q2),
    cirq.H(q0),
    cirq.S(q0).controlled_by(q1),
    cirq.T(q0).controlled_by(q2),
    cirq.H(q1),
    cirq.S(q1).controlled_by(q2),
    cirq.H(q2),
    cirq.SWAP(q0, q2),
])
show(qft3_on_001, label="QFT|001> (3 qubits)")


# ============================================================
# EXERCISE 5: Inverse QFT
# ============================================================
# Build QFT† (inverse QFT) by reversing the circuit:
#   - Reverse the gate order
#   - Replace S with S† (cirq.S**-1) and T with T† (cirq.T**-1)
#
# Apply QFT then QFT† to |01> and verify you get back |01>.
# PREDICT: what is the final state after QFT then QFT†?

print("=" * 50)
print("EXERCISE 5: Inverse QFT")
print("=" * 50)
print("PREDICT: what state do you get after QFT then QFT†?\n")

# q0, q1 = cirq.LineQubit.range(2)
#
# # Prepare |01>
# prep = cirq.Circuit([cirq.X(q1)])
#
# # QFT
# qft = cirq.Circuit([
#     # YOUR QFT GATES HERE
# ])
#
# # Inverse QFT (reverse order, adjoint gates)
# qft_inv = cirq.Circuit([
#     # YOUR INVERSE QFT GATES HERE
# ])
#
# # Round trip: prepare |01>, apply QFT, then QFT†
# full_circuit = prep + qft + qft_inv
# show(full_circuit, label="QFT then QFT† on |01>")


# ============================================================
# EXERCISE 6: QFT reveals periodicity
# ============================================================
# The QFT detects periodic patterns — this is how Shor's
# algorithm finds prime factors.
#
# Create the state (|0> + |2>)/sqrt(2) on 2 qubits. This
# state has period 2 in a 4-element space (non-zero at
# positions 0 and 2, which are spaced 2 apart).
#
# To create |0> + |2>: apply H to q0 (most significant bit),
# leave q1 as |0>. This gives (|00> + |10>)/sqrt(2)
# = (|0> + |2>)/sqrt(2).
#
# Apply QFT. The output should concentrate on |0> and |2>,
# revealing that the period is 2 (= N/2 = 4/2).
# PREDICT: where does the probability concentrate after QFT?

print("=" * 50)
print("EXERCISE 6: QFT reveals periodicity")
print("=" * 50)
print("PREDICT: which states have non-zero probability after QFT?\n")

# q0, q1 = cirq.LineQubit.range(2)
#
# # Create (|0> + |2>)/sqrt(2) = (|00> + |10>)/sqrt(2)
# state_prep = cirq.Circuit([
#     # YOUR GATES HERE
# ])
#
# # Show the periodic input state
# show(state_prep, label="Input: (|0> + |2>)/sqrt(2)")
#
# # Apply QFT
# qft = cirq.Circuit([
#     # YOUR QFT GATES HERE
# ])
#
# full_circuit = state_prep + qft
# show(full_circuit, label="After QFT: periodicity revealed")
