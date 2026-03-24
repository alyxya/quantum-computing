import cirq
import numpy as np

# Two qubits for our circuit
a, b = cirq.LineQubit.range(2)
simulator = cirq.Simulator()

# === The circuit: √X → CZ → √X with measurement ===

print("=== √X-CZ-√X Circuit Walkthrough ===\n")


def basic_circuit(measure=True):
    """Returns a simple circuit with √X and CZ gates."""
    sqrt_x = cirq.X**0.5
    cz = cirq.CZ
    yield sqrt_x(a), sqrt_x(b)
    yield cz(a, b)
    yield sqrt_x(a), sqrt_x(b)
    if measure:
        yield cirq.measure(a, b, key='result')


circuit = cirq.Circuit(basic_circuit())
print(f"Full circuit:\n{circuit}\n")

# === Gate matrices ===

print("=== Gate matrices ===\n")

sqrt_x_matrix = cirq.unitary(cirq.X**0.5)
print("Single-qubit √X matrix:")
print(f"  {np.round(sqrt_x_matrix, 3)}")
print("  = (1/2) * [[1+i, 1-i], [1-i, 1+i]]\n")

cz_matrix = cirq.unitary(cirq.CZ)
print("Two-qubit CZ matrix:")
print(f"  {np.round(cz_matrix, 3)}")
print("  = diag(1, 1, 1, -1)  — flips phase of |11> only\n")

# === Step-by-step state evolution ===
# Basis order: |00>, |01>, |10>, |11>

print("=== Step-by-step state evolution ===\n")
print("Basis order: |00>, |01>, |10>, |11>\n")

# Initial state
print("Step 0 — Initial state: |00>")
print("  [1, 0, 0, 0]\n")

# Step 1: √X on qubit a only
step1 = cirq.Circuit([cirq.X(a)**0.5])
result = simulator.simulate(step1)
sv = result.final_state_vector
print("Step 1 — √X on qubit a  (matrix: √X ⊗ I)")
print(f"  {np.round(sv, 3)}")
print("  = [(1+i)/2, 0, (1-i)/2, 0]")
print("  Qubit a in superposition, qubit b still |0>. State is separable.\n")

# Step 2: √X on qubit b
step2 = cirq.Circuit([cirq.X(a)**0.5, cirq.X(b)**0.5])
result = simulator.simulate(step2)
sv = result.final_state_vector
print("Step 2 — √X on qubit b  (matrix: I ⊗ √X)")
print(f"  {np.round(sv, 3)}")
print("  = [i/2, 1/2, 1/2, -i/2]")
print("  Both qubits in superposition. Still separable. All |amplitudes| = 1/2.\n")

# Step 3: CZ
step3 = cirq.Circuit([
    cirq.X(a)**0.5, cirq.X(b)**0.5,
    cirq.CZ(a, b),
])
result = simulator.simulate(step3)
sv = result.final_state_vector
print("Step 3 — CZ on qubits a, b")
print(f"  {np.round(sv, 3)}")
print("  = [i/2, 1/2, 1/2, i/2]")
print("  Only |11> changed: -i/2 -> i/2 (phase flip).")
print("  State is now ENTANGLED — cannot be written as a product of single-qubit states.\n")

# Step 4: √X on qubit a
step4 = cirq.Circuit([
    cirq.X(a)**0.5, cirq.X(b)**0.5,
    cirq.CZ(a, b),
    cirq.X(a)**0.5,
])
result = simulator.simulate(step4)
sv = result.final_state_vector
print("Step 4 — √X on qubit a  (matrix: √X ⊗ I)")
print(f"  {np.round(sv, 3)}")
print("  = [0, (1+i)/2, (1+i)/2, 0]")
print("  DESTRUCTIVE INTERFERENCE kills |00> and |11> completely!")
print("  Example (row 0): (1+i)/2 * (i/2) + (1-i)/2 * (1/2) = (i-1)/4 + (1-i)/4 = 0")
print("  All amplitude concentrated in |01> and |10>.\n")

# Step 5: √X on qubit b
step5 = cirq.Circuit([
    cirq.X(a)**0.5, cirq.X(b)**0.5,
    cirq.CZ(a, b),
    cirq.X(a)**0.5, cirq.X(b)**0.5,
])
result = simulator.simulate(step5)
sv = result.final_state_vector
print("Step 5 — √X on qubit b  (matrix: I ⊗ √X)")
print(f"  {np.round(sv, 3)}")
print("  = [1/2, i/2, i/2, 1/2]")
print("  Amplitude redistributed across all four basis states.\n")

# === Measurement probabilities ===

print("=== Measurement probabilities ===\n")

probs = np.abs(sv)**2
labels = ['|00>', '|01>', '|10>', '|11>']
for label, p in zip(labels, probs):
    print(f"  P({label}) = |{np.round(sv[labels.index(label)], 3)}|^2 = {p:.0%}")

print(f"\n  All outcomes equally likely (25% each).\n")

# === What would happen WITHOUT the CZ gate? ===

print("=== Comparison: without CZ ===\n")
print("Without CZ, the second √X layer completes the rotation (√X * √X = X):")
print("  |00> -> X|0> ⊗ X|0> = |11> with 100% probability.\n")

no_cz = cirq.Circuit([
    cirq.X(a)**0.5, cirq.X(b)**0.5,
    # no CZ
    cirq.X(a)**0.5, cirq.X(b)**0.5,
])
result = simulator.simulate(no_cz)
sv_no_cz = result.final_state_vector
print(f"  State without CZ: {np.round(sv_no_cz, 3)}")
print("  = [0, 0, 0, 1]  (deterministically |11>)\n")

print("The CZ gate breaks the separability by phase-kicking |11>,")
print("which prevents the second √X layer from cleanly refocusing.")
print("Result: uniform distribution instead of deterministic |11>.")

# === Run the actual circuit to verify ===

print("\n=== Running 1000 measurements to verify ===\n")
results = simulator.run(circuit, repetitions=1000)
print(results.histogram(key='result'))
print("\n(Should be roughly 250 each for 0b00, 0b01, 0b10, 0b11)")
