import cirq
import numpy as np

q0 = cirq.LineQubit(0)
simulator = cirq.Simulator()

# === Example 1: Constructive and destructive interference ===
# Apply Hadamard twice. The amplitudes interfere:
# - |0⟩ amplitudes ADD (constructive) → probability goes to 1
# - |1⟩ amplitudes CANCEL (destructive) → probability goes to 0

print("=== Double Hadamard (interference cancels out) ===\n")

circuit = cirq.Circuit([cirq.H(q0), cirq.H(q0)])
result = simulator.simulate(circuit)
print(f"Circuit: {circuit}")
print(f"Final state: {np.round(result.final_state_vector, 3)}")
print("Back to |0⟩ — the |1⟩ parts cancelled out.\n")

# Let's see why, step by step:
print("Step by step:")
print("  Start:       1|0⟩ + 0|1⟩")
print("  After H:     0.707|0⟩ + 0.707|1⟩")
print("  H on |0⟩ part gives: 0.707 * (|0⟩ + |1⟩)/√2 = 0.5|0⟩ + 0.5|1⟩")
print("  H on |1⟩ part gives: 0.707 * (|0⟩ - |1⟩)/√2 = 0.5|0⟩ - 0.5|1⟩")
print("  Sum:         (0.5+0.5)|0⟩ + (0.5-0.5)|1⟩ = 1|0⟩ + 0|1⟩")
print("  The |1⟩ amplitudes destructively interfered!\n")

# === Example 2: A phase flip BETWEEN the Hadamards changes everything ===
# H → Z → H: the Z gate flips the phase of |1⟩, changing which parts cancel

print("=== H → Z → H (phase flip redirects interference) ===\n")

circuit = cirq.Circuit([cirq.H(q0), cirq.Z(q0), cirq.H(q0)])
result = simulator.simulate(circuit)
print(f"Circuit: {circuit}")
print(f"Final state: {np.round(result.final_state_vector, 3)}")
print("Now it's |1⟩ with 100% certainty!\n")

print("Step by step:")
print("  Start:       1|0⟩ + 0|1⟩")
print("  After H:     0.707|0⟩ + 0.707|1⟩")
print("  After Z:     0.707|0⟩ - 0.707|1⟩   (Z flipped the sign of |1⟩)")
print("  H on |0⟩ part gives:  0.5|0⟩ + 0.5|1⟩")
print("  H on |1⟩ part gives: -0.5|0⟩ + 0.5|1⟩  (note: -0.707 * (|0⟩-|1⟩)/√2)")
print("  Sum:         (0.5-0.5)|0⟩ + (0.5+0.5)|1⟩ = 0|0⟩ + 1|1⟩")
print("  Now |0⟩ cancelled and |1⟩ reinforced — the phase flip reversed the outcome!\n")

# === Example 3: Deutsch's algorithm — the simplest quantum speedup ===
# Problem: you have a function f(x) that takes 0 or 1 and returns 0 or 1.
# Is f constant (f(0)=f(1)) or balanced (f(0)≠f(1))?
# Classically: must evaluate f twice. Quantumly: once.

print("=== Deutsch's Algorithm ===\n")
print("Problem: determine if f(x) is constant or balanced with ONE query.\n")

q_input, q_output = cirq.LineQubit.range(2)

def make_deutsch_circuit(f_gate):
    """Build Deutsch's algorithm circuit with the given oracle."""
    return cirq.Circuit([
        # Prepare: input in |+⟩, output in |−⟩
        cirq.X(q_output),         # output → |1⟩
        cirq.H(q_input),          # input → |+⟩ = (|0⟩+|1⟩)/√2
        cirq.H(q_output),         # output → |−⟩ = (|0⟩-|1⟩)/√2

        # Apply oracle (f_gate)
        f_gate,

        # Interfere and measure input qubit
        cirq.H(q_input),
        cirq.measure(q_input, key='result'),
    ])

# Case 1: f(x) = 0 (constant) — oracle does nothing
print("f(x) = 0 for all x (constant):")
circuit = make_deutsch_circuit(cirq.I(q_input))  # identity = do nothing
print(circuit)
result = simulator.run(circuit, repetitions=100)
print(f"Measured: {result.histogram(key='result')}")
print("Always 0 → constant!\n")

# Case 2: f(x) = x (balanced) — oracle is CNOT
print("f(x) = x (balanced):")
circuit = make_deutsch_circuit(cirq.CNOT(q_input, q_output))
print(circuit)
result = simulator.run(circuit, repetitions=100)
print(f"Measured: {result.histogram(key='result')}")
print("Always 1 → balanced!\n")

print("One query told us the answer with 100% certainty.")
print("This works because the oracle's effect on phases")
print("either cancels (constant) or reinforces (balanced)")
print("when the final Hadamard creates interference.")
