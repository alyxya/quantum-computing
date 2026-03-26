"""Quantum Phase Estimation (QPE). Given a unitary U and its eigenstate |psi>,
QPE estimates the phase phi where U|psi> = e^(2*pi*i*phi)|psi>. This is the
core subroutine of Shor's algorithm.

The QPE circuit:
  1. n counting qubits initialized to |0>, target qubit(s) in eigenstate |psi>.
  2. Apply H to all counting qubits (create uniform superposition).
  3. Apply controlled-U^(2^k) from counting qubit k to target:
     - c0 (MSB) controls U^(2^(n-1))
     - c1 controls U^(2^(n-2))
     - ...
     - c_{n-1} (LSB) controls U^(2^0) = U
  4. Apply inverse QFT on the counting qubits.
  5. Measure counting qubits -> binary approximation of phi.

Why it works: after step 3, the counting register is in the state
  (1/sqrt(2^n)) * sum_k e^(2*pi*i*phi*k) |k>
which is exactly the QFT of |phi>. The inverse QFT in step 4 undoes this,
collapsing the counting register to |phi> (in binary).

Phase kickback (exercise 05) is the engine: each controlled-U^(2^k) kicks
the phase e^(2*pi*i*phi*2^k) onto counting qubit k, encoding phi bit by bit.
"""

from utils import show, simulator
import cirq
import numpy as np


# ============================================================
# EXERCISE 1: Estimate phase of Z
# ============================================================
# Z|1> = -|1> = e^(2*pi*i*0.5)|1>, so phi = 0.5 = 0.1 in binary.
#
# With 1 counting qubit, we can represent phi = 0.b1 (1 binary digit).
# Circuit:
#   - X(q1) to prepare eigenstate |1>
#   - H(q0) to create superposition on counting qubit
#   - CZ(q0, q1): this is controlled-Z, i.e., controlled-U^1
#   - H(q0): inverse QFT on 1 qubit is just H
#   - Measure q0
#
# Trace through:
#   |0>|1>  --H(q0)-->  (|0>+|1>)/sqrt(2) |1>
#           --CZ----->  (|0> - |1>)/sqrt(2) |1>   (phase -1 kicks back)
#           --H(q0)-->  |1>|1>
#
# PREDICT: q0 always measures 1 (binary 0.1 = 0.5).

print("=" * 50)
print("EXERCISE 1: Estimate phase of Z")
print("=" * 50)
print("PREDICT: q0 always measures 1 (binary 0.1 = phi = 0.5)\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.X(q1),
#     cirq.H(q0),
#     cirq.CZ(q0, q1),
#     cirq.H(q0),
#     cirq.measure(q0, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: Estimate phase of S
# ============================================================
# S|1> = i|1> = e^(2*pi*i*0.25)|1>, so phi = 0.25 = 0.01 in binary.
#
# With 2 counting qubits we can represent phi = 0.b1b2 (2 binary digits).
# Qubits: c0 (MSB), c1 (LSB), t (target).
# Circuit:
#   - X(t) to prepare eigenstate |1>
#   - H(c0), H(c1)
#   - controlled-S^2 from c0 to t: S^2 = Z, so this is CZ(c0, t)
#     (c0 is MSB, controls U^(2^1) = S^2 = Z)
#   - controlled-S from c1 to t: S(t).controlled_by(c1)
#     (c1 is LSB, controls U^(2^0) = S)
#   - Inverse QFT on c0, c1:
#       QFT_2: H(c0), cS(c0 controlled by c1), H(c1), SWAP(c0,c1)
#       QFT_2_inv: SWAP(c0,c1), H(c1), cS_dag(c0 controlled by c1), H(c0)
#   - Measure c0, c1
#
# PREDICT: counting qubits measure |01> (c0=0, c1=1),
# reading as binary: 0.01 = 1/4 = 0.25. Matches phi!

print("=" * 50)
print("EXERCISE 2: Estimate phase of S")
print("=" * 50)
print("PREDICT: c0,c1 = |01> (binary 0.01 = phi = 0.25)\n")

# c0, c1, t = cirq.LineQubit.range(3)
# circuit = cirq.Circuit([
#     # Prepare eigenstate
#     cirq.X(t),
#     # Hadamard on counting qubits
#     cirq.H(c0),
#     cirq.H(c1),
#     # Controlled-U^(2^k): c0 (MSB) gets S^2=Z, c1 (LSB) gets S
#     cirq.CZ(c0, t),
#     cirq.S(t).controlled_by(c1),
#     # Inverse QFT on c0, c1
#     cirq.SWAP(c0, c1),
#     cirq.H(c1),
#     (cirq.S**-1)(c0).controlled_by(c1),
#     cirq.H(c0),
#     # Measure
#     cirq.measure(c0, c1, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 3: Estimate phase of T
# ============================================================
# T|1> = e^(i*pi/4)|1> = e^(2*pi*i*0.125)|1>, so phi = 0.125 = 0.001
# in binary. We need 3 counting qubits.
#
# Qubits: c0 (MSB), c1, c2 (LSB), t (target).
# Controlled powers:
#   - c0 controls U^(2^2) = T^4 = Z    -> CZ(c0, t)
#   - c1 controls U^(2^1) = T^2 = S    -> S(t).controlled_by(c1)
#   - c2 controls U^(2^0) = T          -> T(t).controlled_by(c2)
#
# Inverse QFT on 3 qubits (c0, c1, c2):
#   QFT_3: H(c0), cS(c0,c1), cT(c0,c2), H(c1), cS(c1,c2), H(c2), swaps
#   QFT_3_inv: reverse the QFT circuit (swap order, dagger each gate)
#
# PREDICT: counting qubits measure |001> (binary 0.001 = 1/8 = 0.125).

print("=" * 50)
print("EXERCISE 3: Estimate phase of T")
print("=" * 50)
print("PREDICT: c0,c1,c2 = |001> (binary 0.001 = phi = 0.125)\n")

# c0, c1, c2, t = cirq.LineQubit.range(4)
# circuit = cirq.Circuit([
#     # Prepare eigenstate
#     cirq.X(t),
#     # Hadamard on counting qubits
#     cirq.H(c0),
#     cirq.H(c1),
#     cirq.H(c2),
#     # Controlled-U^(2^k)
#     cirq.CZ(c0, t),                   # c0: T^4 = Z
#     cirq.S(t).controlled_by(c1),      # c1: T^2 = S
#     cirq.T(t).controlled_by(c2),      # c2: T^1 = T
#     # Inverse QFT on c0, c1, c2
#     # Step 1: SWAP to reverse bit order
#     cirq.SWAP(c0, c2),
#     # Step 2: H(c2), then controlled rotations, working from LSB to MSB
#     cirq.H(c2),
#     (cirq.S**-1)(c1).controlled_by(c2),
#     cirq.H(c1),
#     (cirq.T**-1)(c0).controlled_by(c2),
#     (cirq.S**-1)(c0).controlled_by(c1),
#     cirq.H(c0),
#     # Measure
#     cirq.measure(c0, c1, c2, key='result'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 4: Generic QPE function
# ============================================================
# Build a reusable QPE circuit for any single-qubit phase gate.
# The function constructs:
#   1. Target qubit prepared in |1> (eigenstate of Z-type gates)
#   2. Counting qubits in superposition
#   3. Controlled-U^(2^k) applications
#   4. Inverse QFT on counting qubits
#   5. Measurement
#
# Test by reproducing exercises 1-3: QPE on Z (1 qubit), S (2 qubits),
# T (3 qubits). Results should match.
#
# PREDICT: does the generic function give the same results as above?

print("=" * 50)
print("EXERCISE 4: Generic QPE function")
print("=" * 50)
print("PREDICT: same results as exercises 1-3?\n")

# def inverse_qft(qubits):
#     """Build the inverse QFT circuit on the given qubits."""
#     n = len(qubits)
#     ops = []
#     # Reverse qubit order
#     for i in range(n // 2):
#         ops.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
#     # Apply H and controlled rotations from last qubit to first
#     for i in range(n - 1, -1, -1):
#         # Controlled phase rotations from higher-index qubits
#         for j in range(n - 1, i, -1):
#             angle = -2 * np.pi / (2 ** (j - i + 1))
#             ops.append(cirq.ZPowGate(exponent=angle / np.pi).on(qubits[i]).controlled_by(qubits[j]))
#         ops.append(cirq.H(qubits[i]))
#     return ops
#
#
# def qpe_circuit(gate, n_counting):
#     """Build QPE circuit for a single-qubit gate.
#
#     Args:
#         gate: A single-qubit cirq gate (e.g., cirq.Z, cirq.S, cirq.T).
#         n_counting: Number of counting qubits.
#
#     Returns:
#         A cirq.Circuit implementing QPE.
#     """
#     counting = cirq.LineQubit.range(n_counting)
#     target = cirq.LineQubit(n_counting)
#     circuit = cirq.Circuit()
#     # Prepare eigenstate |1>
#     circuit.append(cirq.X(target))
#     # Hadamard on all counting qubits
#     circuit.append(cirq.H.on_each(*counting))
#     # Controlled-U^(2^k): qubit k (MSB first) controls gate^(2^(n-1-k))
#     for k, qubit in enumerate(counting):
#         power = 2 ** (n_counting - 1 - k)
#         controlled_gate = (gate**power).on(target).controlled_by(qubit)
#         circuit.append(controlled_gate)
#     # Inverse QFT on counting qubits
#     circuit.append(inverse_qft(counting))
#     # Measure counting qubits
#     circuit.append(cirq.measure(*counting, key='result'))
#     return circuit
#
#
# # Test: reproduce exercises 1-3
# for gate, n, name in [(cirq.Z, 1, "Z"), (cirq.S, 2, "S"), (cirq.T, 3, "T")]:
#     print(f"--- QPE on {name} with {n} counting qubit(s) ---")
#     c = qpe_circuit(gate, n)
#     show(c)


# ============================================================
# EXERCISE 5: Imperfect phase estimation
# ============================================================
# What happens when phi cannot be represented exactly in n bits?
# Use ZPowGate(exponent=0.3). Since ZPow(t)|1> = e^(i*pi*t)|1>
# = e^(2*pi*i*(t/2))|1>, we have phi = 0.3/2 = 0.15.
#
# With 4 counting qubits we have 16 possible outcomes (0..15).
# The exact value 0.15 * 16 = 2.4, which falls between 2 and 3.
# So the measurement distribution should peak at:
#   - 2 (binary 0010, representing 2/16 = 0.125)
#   - 3 (binary 0011, representing 3/16 = 0.1875)
# with smaller probabilities on nearby values.
#
# This demonstrates QPE's behavior for non-exact phases: you get
# a probability distribution peaked near the true value, not a
# single deterministic outcome.
#
# PREDICT: histogram peaks at values 2 and 3 (nearest to 2.4).

print("=" * 50)
print("EXERCISE 5: Imperfect phase estimation")
print("=" * 50)
print("PREDICT: peaks at 2 (0.125) and 3 (0.1875), true phi = 0.15\n")

# gate = cirq.ZPowGate(exponent=0.3)
# c = qpe_circuit(gate, 4)
# show(c, repetitions=1000)
#
# # Show what the measured values mean as phase estimates
# result = simulator.run(c, repetitions=1000)
# counts = result.histogram(key='result')
# print("Phase estimates from measurement outcomes:")
# for measured_val, count in sorted(counts.items()):
#     phase_estimate = measured_val / 16
#     print(f"  measured {measured_val:4d} (binary {measured_val:04b}) "
#           f"-> phi ~ {phase_estimate:.4f}  (count: {count})")
# print(f"  True phase: 0.15")
