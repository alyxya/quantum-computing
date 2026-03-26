"""
Single-qubit quantum gates reference.
Run: python -m reference.gates
"""
import cirq
import numpy as np

q = cirq.LineQubit(0)
sim = cirq.Simulator()

def show_gate(name, gate, description):
    """Print gate info: matrix, effect on |0⟩ and |1⟩, description."""
    print(f"{'=' * 60}")
    print(f"  {name}")
    print(f"  {description}")
    print(f"{'=' * 60}")

    # Unitary matrix
    U = cirq.unitary(gate)
    print(f"\n  Syntax: {gate}")
    print(f"  Unitary matrix:")
    for row in np.round(U, 3):
        print(f"    {row}")

    # Apply to |0⟩
    circuit_0 = cirq.Circuit([gate.on(q)])
    result_0 = sim.simulate(circuit_0, initial_state=0)
    sv0 = np.round(result_0.final_state_vector, 3)

    # Apply to |1⟩
    circuit_1 = cirq.Circuit([gate.on(q)])
    result_1 = sim.simulate(circuit_1, initial_state=1)
    sv1 = np.round(result_1.final_state_vector, 3)

    print(f"\n  |0⟩ → {format_state(sv0)}")
    print(f"  |1⟩ → {format_state(sv1)}")
    print()

def format_state(sv):
    """Format a single-qubit state vector as a readable ket expression."""
    a, b = sv[0], sv[1]
    parts = []
    for amp, label in [(a, "|0⟩"), (b, "|1⟩")]:
        if np.abs(amp) < 1e-6:
            continue
        coeff = format_amplitude(amp)
        if parts and not coeff.startswith("-"):
            coeff = "+ " + coeff
        elif parts and coeff.startswith("-"):
            coeff = "- " + coeff[1:]
        parts.append(f"{coeff}{label}")
    return " ".join(parts) if parts else "0"

def format_amplitude(amp):
    """Format a complex amplitude as a readable string."""
    r, i = np.real(amp), np.imag(amp)
    if abs(i) < 1e-6:
        # Pure real
        if abs(r - 1) < 1e-6:
            return ""
        if abs(r + 1) < 1e-6:
            return "-"
        return f"({r:.3f})"
    if abs(r) < 1e-6:
        # Pure imaginary
        if abs(i - 1) < 1e-6:
            return "i"
        if abs(i + 1) < 1e-6:
            return "-i"
        return f"({i:.3f}i)"
    # General complex
    sign = "+" if i >= 0 else "-"
    return f"({r:.3f}{sign}{abs(i):.3f}i)"


# ─── Standard Pauli + common gates ───────────────────────────

print("\n  SINGLE-QUBIT QUANTUM GATES REFERENCE")
print("  =====================================\n")

show_gate(
    "I — Identity",
    cirq.I,
    "Does nothing. Useful as a placeholder / no-op.",
)

show_gate(
    "X — Pauli-X (NOT gate)",
    cirq.X,
    "Bit flip: swaps |0⟩ and |1⟩.",
)

show_gate(
    "Y — Pauli-Y",
    cirq.Y,
    "Bit flip + phase flip. Introduces imaginary amplitudes.",
)

show_gate(
    "Z — Pauli-Z",
    cirq.Z,
    "Phase flip: |0⟩ unchanged, |1⟩ gets a minus sign.",
)

show_gate(
    "H — Hadamard",
    cirq.H,
    "Creates/destroys superposition. Maps computational ↔ diagonal basis.",
)

show_gate(
    "S — Phase gate (√Z)",
    cirq.S,
    "Quarter turn around Z-axis: |1⟩ → i|1⟩.",
)

show_gate(
    "T gate (⁴√Z)",
    cirq.T,
    "Eighth turn around Z-axis: |1⟩ → e^(iπ/4)|1⟩.",
)

show_gate(
    "√X — sqrt(X)  [cirq.X**0.5]",
    cirq.X**0.5,
    "Half-X rotation. Apply twice to get X.",
)


# ─── Continuous rotation gates ────────────────────────────────

print(f"{'=' * 60}")
print("  Rx(θ), Ry(θ), Rz(θ) — Continuous rotations")
print("  Rotation by θ radians around the X, Y, Z axes.")
print(f"  Syntax: cirq.rx(θ), cirq.ry(θ), cirq.rz(θ)")
print(f"{'=' * 60}")

theta = np.pi / 4
print(f"\n  Example with θ = π/4 ≈ {theta:.4f}\n")

for axis, gate_fn in [("X", cirq.rx), ("Y", cirq.ry), ("Z", cirq.rz)]:
    gate = gate_fn(theta)
    U = cirq.unitary(gate)

    print(f"  R{axis.lower()}(π/4):")
    print(f"    Unitary matrix:")
    for row in np.round(U, 3):
        print(f"      {row}")

    circuit_0 = cirq.Circuit([gate.on(q)])
    result_0 = sim.simulate(circuit_0, initial_state=0)
    sv0 = np.round(result_0.final_state_vector, 3)

    circuit_1 = cirq.Circuit([gate.on(q)])
    result_1 = sim.simulate(circuit_1, initial_state=1)
    sv1 = np.round(result_1.final_state_vector, 3)

    print(f"    |0⟩ → {format_state(sv0)}")
    print(f"    |1⟩ → {format_state(sv1)}")
    print()

print("  TIP: Rx(π) = X,  Ry(π) = Y,  Rz(π) = Z  (up to global phase)")
print("  TIP: Any single-qubit gate = Rz(α) Ry(β) Rz(γ) × global phase")
print()
