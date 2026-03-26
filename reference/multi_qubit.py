"""Multi-qubit quantum gates and tensor products using Cirq."""

import cirq
import numpy as np

sim = cirq.Simulator()

# =============================================================================
# 1. CNOT (Controlled-X)
#    Flips target qubit if control qubit is |1>.
#    Control: q0, Target: q1
# =============================================================================
print("=" * 60)
print("1. CNOT (Controlled-X)")
print("=" * 60)

q0, q1 = cirq.LineQubit.range(2)
print("Matrix:")
print(cirq.unitary(cirq.CNOT))

# Truth table: apply CNOT to each computational basis state
print("\nTruth table (control=q0, target=q1):")
for i in range(2):
    for j in range(2):
        circuit = cirq.Circuit([
            cirq.X(q0) ** i,
            cirq.X(q1) ** j,
            cirq.CNOT(q0, q1),
            cirq.measure(q0, q1, key="result"),
        ])
        measurements = sim.run(circuit, repetitions=1).measurements["result"][0]
        print(f"  |{i}{j}> -> |{measurements[0]}{measurements[1]}>")

# =============================================================================
# 2. CZ (Controlled-Z)
#    Applies Z to target if control is |1>.
#    Symmetric: no distinct control/target. Only |11> gets a phase flip.
# =============================================================================
print("\n" + "=" * 60)
print("2. CZ (Controlled-Z)")
print("=" * 60)

print("Matrix:")
print(cirq.unitary(cirq.CZ))

print("\nComparison to CNOT:")
print("  CNOT flips the target bit: |10> -> |11>, |11> -> |10>")
print("  CZ only adds phase: |11> -> -|11>  (no bit flips)")
print("  CZ is symmetric: CZ(q0,q1) == CZ(q1,q0)")

# Verify symmetry
assert np.allclose(
    cirq.unitary(cirq.Circuit([cirq.CZ(q0, q1)])),
    cirq.unitary(cirq.Circuit([cirq.CZ(q1, q0)])),
), "CZ should be symmetric"
print("  Symmetry verified: CZ(q0,q1) == CZ(q1,q0)")

# =============================================================================
# 3. SWAP
#    Exchanges the states of two qubits.
# =============================================================================
print("\n" + "=" * 60)
print("3. SWAP")
print("=" * 60)

print("Matrix:")
print(cirq.unitary(cirq.SWAP))

# Demonstrate: prepare |10>, apply SWAP, expect |01>
print("\nDemo: SWAP |10> -> |01>")
circuit = cirq.Circuit([
    cirq.X(q0),
    cirq.SWAP(q0, q1),
    cirq.measure(q0, q1, key="result"),
])
measurements = sim.run(circuit, repetitions=1).measurements["result"][0]
print(f"  |10> -> |{measurements[0]}{measurements[1]}>")

# =============================================================================
# 4. Toffoli / CCNOT (3-qubit gate)
#    Flips target if BOTH controls are |1>.
# =============================================================================
print("\n" + "=" * 60)
print("4. Toffoli / CCNOT")
print("=" * 60)

q0, q1, q2 = cirq.LineQubit.range(3)
print("8x8 Matrix:")
print(cirq.unitary(cirq.TOFFOLI).astype(int))

print("\nTruth table (controls=q0,q1; target=q2):")
for i in range(2):
    for j in range(2):
        for k in range(2):
            circuit = cirq.Circuit([
                cirq.X(q0) ** i,
                cirq.X(q1) ** j,
                cirq.X(q2) ** k,
                cirq.TOFFOLI(q0, q1, q2),
                cirq.measure(q0, q1, q2, key="result"),
            ])
            m = sim.run(circuit, repetitions=1).measurements["result"][0]
            marker = " <-- flipped" if m[2] != k else ""
            print(f"  |{i}{j}{k}> -> |{m[0]}{m[1]}{m[2]}>{marker}")

# =============================================================================
# 5. Tensor Products
#    H on q0 in a 2-qubit system is H (x) I (Kronecker product).
# =============================================================================
print("\n" + "=" * 60)
print("5. Tensor Products: H(q0) in 2-qubit system = H (x) I")
print("=" * 60)

q0, q1 = cirq.LineQubit.range(2)

# Get 4x4 unitary from circuit with H on q0 only
circuit_h_q0 = cirq.Circuit([cirq.H(q0)])
# unitary() on a circuit uses all qubits in the circuit; add an identity op
# on q1 to ensure it's included in the unitary
circuit_h_q0_2qubit = cirq.Circuit([cirq.H(q0), cirq.I(q1)])
u_circuit = cirq.unitary(circuit_h_q0_2qubit)

# Build H (x) I manually
H_matrix = cirq.unitary(cirq.H)
I_matrix = np.eye(2)
u_kron = np.kron(H_matrix, I_matrix)

print("4x4 unitary from cirq.Circuit([H(q0), I(q1)]):")
print(np.round(u_circuit, 4))

print("\nnp.kron(H, I):")
print(np.round(u_kron, 4))

assert np.allclose(u_circuit, u_kron), "Should match"
print("\nVerified: circuit unitary matches np.kron(H, I)")

# =============================================================================
# 6. Controlled-U Pattern
#    Make a controlled version of any gate using .controlled()
# =============================================================================
print("\n" + "=" * 60)
print("6. Controlled-U Pattern: gate.controlled()")
print("=" * 60)

q0, q1 = cirq.LineQubit.range(2)

# Controlled-S (S = phase gate, pi/2 rotation)
cs_gate = cirq.S.controlled()
print("Controlled-S gate:")
circuit = cirq.Circuit([cs_gate(q0, q1)])
print(circuit)
print("\nMatrix:")
print(np.round(cirq.unitary(circuit), 4))

# Controlled-H
ch_gate = cirq.H.controlled()
print("\nControlled-H gate:")
circuit = cirq.Circuit([ch_gate(q0, q1)])
print(circuit)
print("\nMatrix:")
print(np.round(cirq.unitary(circuit), 4))

# Arbitrary controlled gate with num_controls > 1
q0, q1, q2 = cirq.LineQubit.range(3)
ccz_gate = cirq.Z.controlled(num_controls=2)
print("\nDouble-controlled Z (CCZ) gate:")
circuit = cirq.Circuit([ccz_gate(q0, q1, q2)])
print(circuit)
print("\n8x8 Matrix (only |111> gets phase flip):")
print(np.round(cirq.unitary(circuit).real, 4).astype(int))
