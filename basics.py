import cirq
import numpy as np

# Create two qubits
q0, q1 = cirq.LineQubit.range(2)

# Build a circuit step by step
circuit = cirq.Circuit([
    cirq.H(q0),          # Step 1: Hadamard on q0 — put it in superposition
    cirq.CNOT(q0, q1),   # Step 2: CNOT — entangle q0 and q1
    cirq.measure(q0, q1, key='result'),  # Step 3: Measure both
])

print("Circuit:")
print(circuit)
print()

# Simulate and show the state vector BEFORE measurement
simulator = cirq.Simulator()

# Walk through each step and show the state
print("=== State after each step ===\n")

# Initial state
print("Initial state: |00⟩")
print("  Amplitudes: [1, 0, 0, 0]  (meaning: 100% |00⟩)\n")

# After step 1: Hadamard on q0
partial = cirq.Circuit([cirq.H(q0)])
result = simulator.simulate(partial)
print("After Hadamard on q0:")
print(f"  State vector: {np.round(result.final_state_vector, 3)}")
print("  = (|00⟩ + |10⟩) / √2")
print("  → 50% chance of q0=0, 50% chance of q0=1. q1 is still definitely 0.\n")

# After step 2: CNOT
partial = cirq.Circuit([cirq.H(q0), cirq.CNOT(q0, q1)])
result = simulator.simulate(partial)
print("After CNOT(q0 → q1):")
print(f"  State vector: {np.round(result.final_state_vector, 3)}")
print("  = (|00⟩ + |11⟩) / √2")
print("  → This is a Bell state! q0 and q1 are now entangled.")
print("  → 50% chance of |00⟩, 50% chance of |11⟩, NOTHING else.")
print("  → They always agree: if q0=0, q1=0. If q0=1, q1=1.\n")

# Run the full circuit many times to see the measurement results
print("=== Running 1000 measurements ===\n")
results = simulator.run(circuit, repetitions=1000)
print(results.histogram(key='result'))
