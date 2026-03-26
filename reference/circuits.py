"""
Notable Quantum Circuit Patterns
=================================
A runnable reference demonstrating key circuit patterns using Cirq.
Each section is self-contained: circuit diagram, state vector, measurements.

Sections:
  1. Bell States
  2. GHZ State
  3. Interference Sandwich
  4. sqrt(X)-CZ-sqrt(X) Circuit
  5. Deutsch's Algorithm
"""

import cirq
import numpy as np

simulator = cirq.Simulator()


# ============================================================
# 1. BELL STATES
# ============================================================
# H + CNOT creates maximally entangled two-qubit states.
# There are four Bell states, each produced by different
# single-qubit preparations before the H-CNOT core.
#
# The recipe: optionally flip q0 and/or q1 with X gates,
# then H on q0, then CNOT(q0, q1).
#
#   |Phi+> = (|00> + |11>) / sqrt(2)   -- no X gates
#   |Phi-> = (|00> - |11>) / sqrt(2)   -- X on q0 before H
#   |Psi+> = (|01> + |10>) / sqrt(2)   -- X on q1 before CNOT
#   |Psi-> = (|01> - |10>) / sqrt(2)   -- X on both

print("=" * 60)
print("1. BELL STATES")
print("=" * 60)
print()
print("H on q0 then CNOT(q0, q1) creates entanglement.")
print("The four Bell states form a complete basis for two-qubit systems.")
print()

q0, q1 = cirq.LineQubit.range(2)

bell_states = [
    ("Phi+", "(|00> + |11>) / sqrt(2)", []),
    ("Phi-", "(|00> - |11>) / sqrt(2)", [cirq.X(q0)]),
    ("Psi+", "(|01> + |10>) / sqrt(2)", [cirq.X(q1)]),
    ("Psi-", "(|01> - |10>) / sqrt(2)", [cirq.X(q0), cirq.X(q1)]),
]

for name, expression, prep_gates in bell_states:
    print(f"--- |{name}> = {expression} ---")
    print()

    circuit_ops = prep_gates + [cirq.H(q0), cirq.CNOT(q0, q1)]
    circuit_no_measure = cirq.Circuit(circuit_ops)
    circuit_with_measure = cirq.Circuit(circuit_ops + [cirq.measure(q0, q1, key='result')])

    print(f"Circuit:")
    print(circuit_with_measure)
    print()

    result = simulator.simulate(circuit_no_measure)
    sv = np.round(result.final_state_vector, 3)
    print(f"State vector: {sv}")

    samples = simulator.run(circuit_with_measure, repetitions=1000)
    print(f"Measurements (1000x): {samples.histogram(key='result')}")
    print()


# ============================================================
# 2. GHZ STATE
# ============================================================
# Generalize Bell to three qubits: H on q0, then CNOT cascade.
# Creates (|000> + |111>) / sqrt(2).
# Named after Greenberger-Horne-Zeilinger.

print("=" * 60)
print("2. GHZ STATE")
print("=" * 60)
print()
print("H on q0, then CNOT(q0,q1), CNOT(q1,q2).")
print("Creates (|000> + |111>) / sqrt(2) -- three-qubit entanglement.")
print()

q0, q1, q2 = cirq.LineQubit.range(3)

ghz_circuit = cirq.Circuit([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.CNOT(q1, q2),
])
ghz_circuit_measure = cirq.Circuit([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.CNOT(q1, q2),
    cirq.measure(q0, q1, q2, key='result'),
])

print(f"Circuit:")
print(ghz_circuit_measure)
print()

# State vector
result = simulator.simulate(ghz_circuit)
sv = np.round(result.final_state_vector, 3)
print(f"State vector (basis order |000>, |001>, ..., |111>):")
print(f"  {sv}")
print()

# Show which amplitudes are nonzero
labels = [format(i, '03b') for i in range(8)]
for i, (label, amp) in enumerate(zip(labels, sv)):
    if abs(amp) > 0.001:
        print(f"  |{label}> : amplitude = {amp:.3f}, probability = {abs(amp)**2:.1%}")
print()
print("Only |000> and |111> have nonzero amplitude -- maximally entangled.")
print()

# Measurements
samples = simulator.run(ghz_circuit_measure, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print("(Only 0b000=0 and 0b111=7 appear -- all three qubits always agree.)")
print()


# ============================================================
# 3. INTERFERENCE SANDWICH
# ============================================================
# Two examples showing how gates between Hadamards steer interference.
#
# Example A: H-H = identity (destructive interference on |1>)
# Example B: H-Z-H = X (phase flip redirects interference)

print("=" * 60)
print("3. INTERFERENCE SANDWICH")
print("=" * 60)
print()

q0 = cirq.LineQubit(0)

# --- Example A: H then H ---

print("--- Example A: H then H = identity ---")
print()

circuit_hh = cirq.Circuit([cirq.H(q0), cirq.H(q0)])
circuit_hh_measure = cirq.Circuit([cirq.H(q0), cirq.H(q0), cirq.measure(q0, key='result')])

print(f"Circuit:")
print(circuit_hh_measure)
print()

result = simulator.simulate(circuit_hh)
sv = np.round(result.final_state_vector, 3)
print(f"Final state: {sv}")
print()

print("Amplitude evolution step by step:")
print()
print("  Start:           1.000|0> + 0.000|1>")
print()
print("  After first H:   0.707|0> + 0.707|1>")
print("    H sends |0> -> (|0>+|1>)/sqrt(2)")
print()
print("  After second H:  1.000|0> + 0.000|1>")
print("    H on the |0> part: 0.707 * (|0> + |1>) / sqrt(2) = 0.5|0> + 0.5|1>")
print("    H on the |1> part: 0.707 * (|0> - |1>) / sqrt(2) = 0.5|0> - 0.5|1>")
print("    Sum: (0.5+0.5)|0> + (0.5-0.5)|1> = 1|0> + 0|1>")
print()
print("  The |1> amplitudes destructively interfere (cancel to zero).")
print("  The |0> amplitudes constructively interfere (add to one).")
print("  Result: always measures |0>.")
print()

samples = simulator.run(circuit_hh_measure, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print()

# --- Example B: H-Z-H = X ---

print("--- Example B: H-Z-H = X (phase flip redirects interference) ---")
print()

circuit_hzh = cirq.Circuit([cirq.H(q0), cirq.Z(q0), cirq.H(q0)])
circuit_hzh_measure = cirq.Circuit([
    cirq.H(q0), cirq.Z(q0), cirq.H(q0),
    cirq.measure(q0, key='result'),
])

print(f"Circuit:")
print(circuit_hzh_measure)
print()

result = simulator.simulate(circuit_hzh)
sv = np.round(result.final_state_vector, 3)
print(f"Final state: {sv}")
print()

print("Amplitude evolution step by step:")
print()
print("  Start:           1.000|0> + 0.000|1>")
print()
print("  After H:         0.707|0> + 0.707|1>")
print()
print("  After Z:         0.707|0> - 0.707|1>")
print("    Z flips the sign of |1> only: |1> -> -|1>")
print()
print("  After second H:")
print("    H on the |0> part:  0.707 * (|0> + |1>) / sqrt(2) =  0.5|0> + 0.5|1>")
print("    H on the |1> part: -0.707 * (|0> - |1>) / sqrt(2) = -0.5|0> + 0.5|1>")
print("    Sum: (0.5-0.5)|0> + (0.5+0.5)|1> = 0|0> + 1|1>")
print()
print("  The Z gate reversed which component interferes destructively.")
print("  Now |0> cancels and |1> reinforces. Always measures |1>.")
print()

samples = simulator.run(circuit_hzh_measure, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print()


# ============================================================
# 4. sqrt(X)-CZ-sqrt(X) CIRCUIT
# ============================================================
# Two qubits: apply sqrt(X) to both, then CZ, then sqrt(X) to both.
# Without CZ: sqrt(X) * sqrt(X) = X, so |00> -> |11> deterministically.
# With CZ: the phase kick on |11> entangles the qubits and prevents
# the second sqrt(X) layer from cleanly recombining. Result: uniform
# distribution over all four basis states.

print("=" * 60)
print("4. sqrt(X)-CZ-sqrt(X) CIRCUIT")
print("=" * 60)
print()

a, b = cirq.LineQubit.range(2)
sqrt_x = cirq.X**0.5

# --- Without CZ: deterministic |11> ---

print("--- Without CZ: sqrt(X) sqrt(X) = X, so |00> -> |11> ---")
print()

no_cz_circuit = cirq.Circuit([
    sqrt_x(a), sqrt_x(b),
    # no CZ
    sqrt_x(a), sqrt_x(b),
])
no_cz_circuit_measure = cirq.Circuit([
    sqrt_x(a), sqrt_x(b),
    sqrt_x(a), sqrt_x(b),
    cirq.measure(a, b, key='result'),
])

print(f"Circuit:")
print(no_cz_circuit_measure)
print()

result = simulator.simulate(no_cz_circuit)
sv = np.round(result.final_state_vector, 3)
print(f"State vector: {sv}")
print("  = |11> with 100% probability (sqrt(X) * sqrt(X) = X on each qubit)")
print()

samples = simulator.run(no_cz_circuit_measure, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print()

# --- With CZ: uniform distribution ---

print("--- With CZ: phase kick creates entanglement, blocks recombination ---")
print()

cz_circuit = cirq.Circuit([
    sqrt_x(a), sqrt_x(b),
    cirq.CZ(a, b),
    sqrt_x(a), sqrt_x(b),
])
cz_circuit_measure = cirq.Circuit([
    sqrt_x(a), sqrt_x(b),
    cirq.CZ(a, b),
    sqrt_x(a), sqrt_x(b),
    cirq.measure(a, b, key='result'),
])

print(f"Circuit:")
print(cz_circuit_measure)
print()

# Step-by-step evolution
print("Step-by-step state evolution (basis order |00>, |01>, |10>, |11>):")
print()

print("  Step 0 -- Initial: |00>")
print("    [1, 0, 0, 0]")
print()

step1 = cirq.Circuit([sqrt_x(a), sqrt_x(b)])
r = simulator.simulate(step1)
sv1 = np.round(r.final_state_vector, 3)
print(f"  Step 1 -- sqrt(X) on both qubits:")
print(f"    {sv1}")
print("    All |amplitudes| = 0.5. State is separable (product of two single-qubit states).")
print()

step2 = cirq.Circuit([sqrt_x(a), sqrt_x(b), cirq.CZ(a, b)])
r = simulator.simulate(step2)
sv2 = np.round(r.final_state_vector, 3)
print(f"  Step 2 -- CZ:")
print(f"    {sv2}")
print("    CZ flips the phase of |11> only. State is now ENTANGLED.")
print()

r = simulator.simulate(cz_circuit)
sv_final = np.round(r.final_state_vector, 3)
print(f"  Step 3 -- sqrt(X) on both qubits again:")
print(f"    {sv_final}")
print()

# Probabilities
probs = np.abs(sv_final)**2
labels = ['|00>', '|01>', '|10>', '|11>']
for label, p in zip(labels, probs):
    print(f"    P({label}) = {p:.0%}")
print()
print("  All outcomes equally likely (25% each).")
print("  The CZ gate broke separability -- the second sqrt(X) layer")
print("  could not cleanly undo the first. Entanglement prevents recombination.")
print()

samples = simulator.run(cz_circuit_measure, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print("(Roughly 250 each for 0=|00>, 1=|01>, 2=|10>, 3=|11>)")
print()


# ============================================================
# 5. DEUTSCH'S ALGORITHM
# ============================================================
# The simplest quantum speedup.
#
# Problem: given a black-box function f: {0,1} -> {0,1},
# determine if f is constant (f(0)=f(1)) or balanced (f(0)!=f(1)).
# Classically: must query f twice. Quantumly: one query suffices.
#
# Circuit:
#   1. Prepare input qubit in |+> and output qubit in |->
#   2. Apply oracle (encodes f)
#   3. Apply H to input qubit and measure
#
# If f is constant: input measures |0>
# If f is balanced: input measures |1>
#
# Oracle for f(x)=0 (constant): identity gate (do nothing)
# Oracle for f(x)=x (balanced): CNOT(input, output)

print("=" * 60)
print("5. DEUTSCH'S ALGORITHM")
print("=" * 60)
print()
print("Problem: is f(x) constant or balanced? Determine with ONE query.")
print()
print("Constant: f(0) = f(1)  (same output for both inputs)")
print("Balanced: f(0) != f(1) (different outputs)")
print()

q_in, q_out = cirq.LineQubit.range(2)


def make_deutsch_circuit(oracle_gate, label):
    """Build Deutsch's algorithm circuit with the given oracle."""
    return cirq.Circuit([
        # Prepare: input in |+>, output in |->
        cirq.X(q_out),           # output -> |1>
        cirq.H(q_in),           # input -> |+> = (|0>+|1>)/sqrt(2)
        cirq.H(q_out),          # output -> |-> = (|0>-|1>)/sqrt(2)

        # Oracle
        oracle_gate,

        # Interfere and measure input qubit
        cirq.H(q_in),
        cirq.measure(q_in, key='result'),
    ])


# --- Case 1: f(x) = 0 for all x (constant) ---
# Oracle = identity (f does nothing to the output)

print("--- Case 1: f(x) = 0 (constant), oracle = I ---")
print()

circuit_const = make_deutsch_circuit(cirq.I(q_in), "constant")
print(f"Circuit:")
print(circuit_const)
print()

# Show state just before measurement
circuit_const_no_measure = cirq.Circuit([
    cirq.X(q_out),
    cirq.H(q_in),
    cirq.H(q_out),
    cirq.I(q_in),
    cirq.H(q_in),
])
r = simulator.simulate(circuit_const_no_measure)
sv = np.round(r.final_state_vector, 3)
print(f"State before measurement: {sv}")
print("  Input qubit (q0) is in |0> -- constant function detected.")
print()

samples = simulator.run(circuit_const, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print("Always 0 --> f is constant.")
print()

# --- Case 2: f(x) = x (balanced) ---
# Oracle = CNOT(input, output)

print("--- Case 2: f(x) = x (balanced), oracle = CNOT ---")
print()

circuit_bal = make_deutsch_circuit(cirq.CNOT(q_in, q_out), "balanced")
print(f"Circuit:")
print(circuit_bal)
print()

# Show state just before measurement
circuit_bal_no_measure = cirq.Circuit([
    cirq.X(q_out),
    cirq.H(q_in),
    cirq.H(q_out),
    cirq.CNOT(q_in, q_out),
    cirq.H(q_in),
])
r = simulator.simulate(circuit_bal_no_measure)
sv = np.round(r.final_state_vector, 3)
print(f"State before measurement: {sv}")
print("  Input qubit (q0) is in |1> -- balanced function detected.")
print()

samples = simulator.run(circuit_bal, repetitions=1000)
print(f"Measurements (1000x): {samples.histogram(key='result')}")
print("Always 1 --> f is balanced.")
print()

print("One query determined the answer with 100% certainty.")
print("The oracle's effect on phases either cancels (constant)")
print("or reinforces (balanced) when the final Hadamard creates interference.")
