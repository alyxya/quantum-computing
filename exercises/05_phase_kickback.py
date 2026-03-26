"""Phase kickback. The mechanism that makes most quantum algorithms work:
controlled gates kick phases back to the control qubit.

Key concept: when you apply a controlled-U gate where the target qubit is
in an eigenstate |psi> of U with eigenvalue e^(i*phi), the target stays
unchanged but the control qubit picks up the phase e^(i*phi). This is
called phase kickback.

Why? The controlled-U acts as:
  |0>|psi> -> |0>|psi>           (U not applied)
  |1>|psi> -> |1> U|psi>         (U applied)
           =  |1> e^(i*phi)|psi> (eigenstate property)
           =  e^(i*phi)|1>|psi>  (scalar floats to the front)

So if the control is in superposition (|0> + |1>)/sqrt(2):
  (|0> + |1>)/sqrt(2) |psi>  ->  (|0> + e^(i*phi)|1>)/sqrt(2) |psi>

The target is untouched, but the control now carries the phase!
This is the engine behind quantum phase estimation, Shor's algorithm,
and Grover's algorithm.
"""

from utils import show, simulator
import cirq
import numpy as np


# ============================================================
# EXERCISE 1: CZ kickback
# ============================================================
# Put q0 (control) in superposition with H. Prepare q1 (target) in |1>.
# Apply CZ. Then apply H to q0 and measure.
#
# CZ flips the phase when BOTH qubits are |1>. Since |1> is an
# eigenstate of Z with eigenvalue -1, the phase -1 kicks back
# to the control qubit:
#   (|0> + |1>)/sqrt(2) |1>  -->  (|0> - |1>)/sqrt(2) |1>
#
# After H on q0: H(|0> - |1>)/sqrt(2) = |1>.
# PREDICT: what does q0 measure? Always 0, always 1, or 50/50?

print("=" * 50)
print("EXERCISE 1: CZ kickback")
print("=" * 50)
print("PREDICT: what does q0 measure after CZ kickback + H?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q1),
#     cirq.CZ(q0, q1),
#     cirq.H(q0),
#     cirq.measure(q0, key='q0'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 2: CNOT kickback
# ============================================================
# Prepare target q1 in |-> = (|0> - |1>)/sqrt(2), which is an
# eigenstate of X with eigenvalue -1. Put q0 in superposition.
# Apply CNOT(q0, q1). Then H on q0 and measure.
#
# CNOT applies X to the target. Since |-> is an eigenstate of X
# with eigenvalue -1, the phase -1 kicks back to the control:
#   (|0> + |1>)/sqrt(2) |->  -->  (|0> - |1>)/sqrt(2) |->
#
# After H on q0: |1>. Same result as CZ kickback!
# PREDICT: what does q0 measure?

print("=" * 50)
print("EXERCISE 2: CNOT kickback")
print("=" * 50)
print("PREDICT: what does q0 measure after CNOT kickback + H?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.X(q1),
#     cirq.H(q1),
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
#     cirq.H(q0),
#     cirq.measure(q0, key='q0'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 3: S gate kickback
# ============================================================
# Prepare q1 in |1> (eigenstate of S with eigenvalue i = e^(i*pi/2)).
# Put q0 in superposition. Apply controlled-S.
#
# The phase i kicks back to q0:
#   (|0> + |1>)/sqrt(2) |1>  -->  (|0> + i|1>)/sqrt(2) |1>
#
# Look at the state vector — the i phase should appear on the
# |11> amplitude (the component where q0=1, q1=1).
# PREDICT: what does the state vector look like?

print("=" * 50)
print("EXERCISE 3: S gate kickback")
print("=" * 50)
print("PREDICT: what phase appears on the control qubit?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q1),
#     cirq.S(q1).controlled_by(q0),
#     cirq.measure(q0, key='q0'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 4: T gate kickback
# ============================================================
# Same setup but with a T gate. T has eigenvalue e^(i*pi/4)
# for |1>. The phase e^(i*pi/4) = (1+i)/sqrt(2) should appear
# on the control qubit's |1> component.
#
# Compare the state vector with Exercise 3. The phase is
# smaller (pi/4 vs pi/2), which you can see in the complex
# amplitudes.
# PREDICT: what does the state vector look like?

print("=" * 50)
print("EXERCISE 4: T gate kickback")
print("=" * 50)
print("PREDICT: what phase appears on the control qubit?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.X(q1),
#     cirq.T(q1).controlled_by(q0),
#     cirq.measure(q0, key='q0'),
# ])
# show(circuit)


# ============================================================
# EXERCISE 5: Why eigenstates matter
# ============================================================
# What happens if the target is NOT in an eigenstate of the
# controlled gate? Put q0 in superposition with H. Leave q1
# in |0> (which is NOT an eigenstate of X). Apply CNOT.
#
# Instead of a clean phase on q0, the qubits become entangled!
# The state vector shows (|00> + |11>)/sqrt(2) — a Bell state.
# No single qubit carries a phase; the information is shared.
#
# This is why kickback requires eigenstates: without them,
# you get entanglement instead of a clean phase transfer.
# PREDICT: what does the state vector look like?

print("=" * 50)
print("EXERCISE 5: Why eigenstates matter")
print("=" * 50)
print("PREDICT: what happens when the target is NOT an eigenstate?\n")

# q0, q1 = cirq.LineQubit.range(2)
# circuit = cirq.Circuit([
#     cirq.H(q0),
#     cirq.CNOT(q0, q1),
# ])
# show(circuit)


# ============================================================
# EXERCISE 6: Kickback with arbitrary angle
# ============================================================
# Use ZPowGate(exponent=t) to explore how different phases
# kick back. ZPowGate applies e^(i*pi*t) to |1>.
#
# For t=0.25: phase = e^(i*pi/4), same as T gate
# For t=0.5:  phase = e^(i*pi/2) = i, same as S gate
# For t=0.75: phase = e^(i*3*pi/4)
#
# Look at the state vector each time. The |11> amplitude
# should show the kicked-back phase e^(i*pi*t).
# PREDICT: how do the amplitudes change as t increases?

print("=" * 50)
print("EXERCISE 6: Kickback with arbitrary angle")
print("=" * 50)
print("PREDICT: how does the phase on q0 change with t?\n")

# q0, q1 = cirq.LineQubit.range(2)
# for t in [0.25, 0.5, 0.75]:
#     circuit = cirq.Circuit([
#         cirq.H(q0),
#         cirq.X(q1),
#         cirq.ZPowGate(exponent=t).on(q1).controlled_by(q0),
#     ])
#     show(circuit, label=f"ZPowGate(exponent={t}), phase = e^(i*pi*{t})")
