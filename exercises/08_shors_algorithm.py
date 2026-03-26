"""Shor's Algorithm. Factor integers using quantum period finding.
This is the capstone -- combining everything from exercises 01-07.

The algorithm:
  1. Choose random a < N, check gcd(a, N) = 1 (otherwise we already found a factor).
  2. Use QPE to find the period r of f(x) = a^x mod N.
     The quantum circuit encodes modular exponentiation as a unitary and
     uses phase estimation to extract the period from its eigenvalues.
  3. If r is even and a^(r/2) != -1 mod N, then:
       gcd(a^(r/2) + 1, N) and gcd(a^(r/2) - 1, N)
     give non-trivial factors of N.

Why it works: the eigenvalues of the modular exponentiation unitary
U_a|y> = |a*y mod N> are e^(2*pi*i*s/r) for s = 0, 1, ..., r-1.
QPE estimates s/r, and from this rational fraction we extract r
using continued fractions. Once we have r, the rest is classical.

This exercise focuses on N=15 (the smallest interesting case).
Factors: 3 x 5. We'll use a=7 (period 4) and a=11 (period 2).
"""

from utils import show, simulator
import cirq
import numpy as np
import math
from fractions import Fraction


# ================================================================
# HELPER FUNCTIONS (provided -- the learner uses these, not derives)
# ================================================================
# Building modular exponentiation circuits from scratch requires
# advanced circuit synthesis. These helpers construct the oracles
# for N=15 so the exercises can focus on the algorithm structure.

def mod_mult_matrix(a, N=15):
    """Build the permutation matrix for |y> -> |a*y mod N>.

    For values y coprime to N, maps y -> a*y mod N.
    For y=0 or y not coprime to N, acts as identity (these states
    are never reached when starting from |1>).
    """
    dim = 2 ** int(np.ceil(np.log2(N)))
    matrix = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y == 0 or y >= N:
            # Identity for out-of-range values
            matrix[y, y] = 1
        else:
            target = (a * y) % N
            if target >= dim:
                matrix[y, y] = 1
            else:
                matrix[target, y] = 1
    return matrix


def controlled_mod_mult(a, N, control_qubit, target_qubits):
    """Create a controlled modular multiplication gate.

    Implements controlled-|y> -> |a*y mod N> on the target qubits,
    controlled by control_qubit.
    """
    matrix = mod_mult_matrix(a, N)
    gate = cirq.MatrixGate(matrix)
    return gate.on(*target_qubits).controlled_by(control_qubit)


def verify_mod_mult(a, N=15):
    """Print the multiplication table to verify the oracle."""
    print(f"  Modular multiplication by {a} mod {N}:")
    val = 1
    for i in range(10):
        next_val = (val * a) % N
        print(f"    {a}^{i} mod {N} = {val}" +
              (" <-- period!" if i > 0 and val == 1 else ""))
        if i > 0 and val == 1:
            break
        val = next_val


# ============================================================
# EXERCISE 1: Classical parts of Shor's algorithm
# ============================================================
# Before running any quantum circuit, implement the classical
# subroutines. These are NOT commented out since they're pure
# Python -- run them to see the results.
#
# Functions:
#   - mod_exp(base, exp, mod): compute base^exp mod mod
#   - find_period_classical(a, N): brute force smallest r where a^r mod N = 1
#   - extract_factors(a, r, N): given period r, compute gcd(a^(r/2)+/-1, N)
#
# Test with N=15:
#   a=7:  period r=4, 7^2 mod 15 = 4,  gcd(4+1,15)=5, gcd(4-1,15)=3
#   a=11: period r=2, 11^1 mod 15 = 11, gcd(11+1,15)=3, gcd(11-1,15)=5

print("=" * 50)
print("EXERCISE 1: Classical parts of Shor's algorithm")
print("=" * 50)
print("Testing classical period finding and factor extraction.\n")


def mod_exp(base, exp, mod):
    """Compute base^exp mod mod using repeated squaring."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result


def find_period_classical(a, N):
    """Find the smallest r > 0 such that a^r mod N = 1."""
    r = 1
    while r < N:
        if mod_exp(a, r, N) == 1:
            return r
        r += 1
    return None


def extract_factors(a, r, N):
    """Given period r of a mod N, attempt to extract factors."""
    if r % 2 != 0:
        return None, None
    x = mod_exp(a, r // 2, N)
    if x == N - 1:  # a^(r/2) = -1 mod N
        return None, None
    f1 = math.gcd(x + 1, N)
    f2 = math.gcd(x - 1, N)
    return f1, f2


# Test with a=7, N=15
print("--- a=7, N=15 ---")
r = find_period_classical(7, 15)
print(f"  Period: r = {r}")
print(f"  7^(r/2) mod 15 = 7^{r//2} mod 15 = {mod_exp(7, r//2, 15)}")
f1, f2 = extract_factors(7, r, 15)
print(f"  Factors: gcd({mod_exp(7, r//2, 15)}+1, 15) = {f1}")
print(f"           gcd({mod_exp(7, r//2, 15)}-1, 15) = {f2}")
print(f"  Verification: {f1} x {f2} = {f1 * f2}\n")

# Test with a=11, N=15
print("--- a=11, N=15 ---")
r = find_period_classical(11, 15)
print(f"  Period: r = {r}")
print(f"  11^(r/2) mod 15 = 11^{r//2} mod 15 = {mod_exp(11, r//2, 15)}")
f1, f2 = extract_factors(11, r, 15)
print(f"  Factors: gcd({mod_exp(11, r//2, 15)}+1, 15) = {f1}")
print(f"           gcd({mod_exp(11, r//2, 15)}-1, 15) = {f2}")
print(f"  Verification: {f1} x {f2} = {f1 * f2}\n")


# ============================================================
# EXERCISE 2: Modular exponentiation oracle for N=15, a=7
# ============================================================
# The quantum oracle implements |x>|y> -> |x>|y * a^x mod N>.
# For N=15 we need 4 work qubits (to represent values 0-15).
#
# For a=7, N=15, the powers cycle with period 4:
#   7^1 = 7,  7^2 = 4,  7^3 = 13,  7^4 = 1 (mod 15)
#
# The oracle is decomposed into controlled multiplications:
#   - Counting qubit c_k controls "multiply by a^(2^k) mod N"
#   - For a=7: a^1=7, a^2=4, a^4=1 (identity), a^8=1, ...
#   - So we only need controlled-x7 and controlled-x4; higher
#     powers are identity and can be skipped.
#
# The helper functions above build these as permutation matrices.
# Verify the oracle is correct by checking the multiplication table.
#
# PREDICT: the oracle maps work register |1> through the cycle
# 1 -> 7 -> 4 -> 13 -> 1.

print("=" * 50)
print("EXERCISE 2: Modular exponentiation oracle (a=7, N=15)")
print("=" * 50)
print("PREDICT: |1> -> |7> -> |4> -> |13> -> |1> (cycle of 4)\n")

# # Verify multiplication tables for the powers we need
# verify_mod_mult(7, 15)   # a^1 = 7
# print()
# verify_mod_mult(4, 15)   # a^2 = 4 (since 7^2 mod 15 = 4)
# print()
#
# # Demonstrate the oracle on a single work register
# # Apply multiply-by-7 to |0001> (representing value 1)
# work = cirq.LineQubit.range(4)
# circuit = cirq.Circuit([
#     cirq.X(work[3]),  # Set work register to |0001> = value 1
# ])
# print("Work register initialized to |1>:")
# show(circuit)
#
# # Apply multiply-by-7 (uncontrolled, for testing)
# gate = cirq.MatrixGate(mod_mult_matrix(7, 15))
# circuit = cirq.Circuit([
#     cirq.X(work[3]),          # |0001> = 1
#     gate.on(*work),           # multiply by 7: 1 -> 7 = |0111>
#     cirq.measure(*work, key='result'),
# ])
# print("After multiply by 7:")
# show(circuit)
#
# # Apply multiply-by-7 twice (should give 7*7 mod 15 = 4)
# circuit = cirq.Circuit([
#     cirq.X(work[3]),          # |0001> = 1
#     gate.on(*work),           # 1 -> 7
#     gate.on(*work),           # 7 -> 49 mod 15 = 4 = |0100>
#     cirq.measure(*work, key='result'),
# ])
# print("After multiply by 7 twice (should be 4):")
# show(circuit)


# ============================================================
# EXERCISE 3: Period finding circuit (QPE + oracle, a=7, N=15)
# ============================================================
# Combine QPE with the modular exponentiation oracle.
# Use 4 counting qubits (c0-c3) and 4 work qubits (w0-w3).
# Total: 8 qubits.
#
# Circuit:
#   1. Initialize work register to |1> (X on least significant bit)
#   2. H on all counting qubits
#   3. Controlled modular multiplications:
#      - c0 (MSB) controls x(7^8 mod 15) = x1 = identity (skip)
#      - c1 controls x(7^4 mod 15) = x1 = identity (skip)
#      - c2 controls x(7^2 mod 15) = x4
#      - c3 (LSB) controls x(7^1 mod 15) = x7
#   4. Inverse QFT on counting qubits
#   5. Measure counting qubits
#
# The period is r=4. With 4 counting qubits (2^4=16 values),
# the peaks should appear at multiples of 16/4 = 4:
#   0, 4, 8, 12 (representing phases 0/16, 4/16, 8/16, 12/16)
#
# PREDICT: histogram shows 4 peaks at measured values 0, 4, 8, 12
# (each with roughly equal probability ~25%).

print("=" * 50)
print("EXERCISE 3: Period finding circuit (a=7, N=15)")
print("=" * 50)
print("PREDICT: peaks at 0, 4, 8, 12 (multiples of 16/r = 16/4 = 4)\n")

# def inverse_qft(qubits):
#     """Inverse QFT on a list of qubits."""
#     n = len(qubits)
#     ops = []
#     # Reverse qubit order
#     for i in range(n // 2):
#         ops.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
#     # Apply H and controlled rotations from last qubit to first
#     for i in range(n - 1, -1, -1):
#         for j in range(n - 1, i, -1):
#             angle = -2 * np.pi / (2 ** (j - i + 1))
#             ops.append(
#                 cirq.ZPowGate(exponent=angle / np.pi).on(qubits[i]).controlled_by(qubits[j])
#             )
#         ops.append(cirq.H(qubits[i]))
#     return ops
#
#
# # Build the circuit
# counting = cirq.LineQubit.range(4)        # c0 (MSB) to c3 (LSB)
# work = cirq.LineQubit.range(4, 8)         # w0 to w3
# c0, c1, c2, c3 = counting
#
# circuit = cirq.Circuit()
# # 1. Initialize work register to |1>
# circuit.append(cirq.X(work[3]))  # |00000001> in work register = value 1
# # 2. Hadamard on counting qubits
# circuit.append(cirq.H.on_each(*counting))
# # 3. Controlled modular multiplications
# # c0: 7^(2^3) mod 15 = 7^8 mod 15 = 1 (identity, skip)
# # c1: 7^(2^2) mod 15 = 7^4 mod 15 = 1 (identity, skip)
# # c2: 7^(2^1) mod 15 = 7^2 mod 15 = 4
# circuit.append(controlled_mod_mult(4, 15, c2, work))
# # c3: 7^(2^0) mod 15 = 7^1 mod 15 = 7
# circuit.append(controlled_mod_mult(7, 15, c3, work))
# # 4. Inverse QFT on counting qubits
# circuit.append(inverse_qft(counting))
# # 5. Measure
# circuit.append(cirq.measure(*counting, key='result'))
#
# show(circuit, repetitions=1000)


# ============================================================
# EXERCISE 4: Classical post-processing
# ============================================================
# Take the measured values from exercise 3 and extract factors.
# For each measured value m:
#   1. Compute phase estimate: phi = m / 2^n (n=4 counting qubits)
#   2. Use continued fractions to find best rational p/r with r < N
#   3. r is the candidate period
#   4. Check if a^r mod N = 1
#   5. If r is even, compute gcd(a^(r/2) +/- 1, N)
#
# Expected values for a=7, N=15:
#   m=0:  phi=0/16=0      -> 0/1, period r=1 (trivial, discard)
#   m=4:  phi=4/16=1/4    -> 1/4, period r=4, 7^2=4, gcd(5,15)=5, gcd(3,15)=3
#   m=8:  phi=8/16=1/2    -> 1/2, period r=2, 7^1=7, gcd(8,15)=1 (fail)
#                            but we can also try r=4 as a multiple
#   m=12: phi=12/16=3/4   -> 3/4, period r=4, same as m=4
#
# PREDICT: m=4 and m=12 directly give r=4, yielding factors 3 and 5.

print("=" * 50)
print("EXERCISE 4: Classical post-processing")
print("=" * 50)
print("PREDICT: continued fractions on m=4,12 give r=4, factors 3 x 5\n")

# def post_process(measured_values, n_counting, a, N):
#     """Classical post-processing of QPE measurement results."""
#     n_qubits = n_counting
#     factors_found = set()
#
#     for m in sorted(set(measured_values)):
#         if m == 0:
#             print(f"  m={m}: phase=0, trivial (skip)")
#             continue
#
#         # Phase estimate
#         phase = m / (2 ** n_qubits)
#         # Continued fraction approximation
#         frac = Fraction(phase).limit_denominator(N)
#         r_candidate = frac.denominator
#
#         print(f"  m={m}: phase={m}/{2**n_qubits}={phase:.4f} "
#               f"-> fraction {frac} -> candidate r={r_candidate}")
#
#         # Check if this is a valid period
#         if mod_exp(a, r_candidate, N) != 1:
#             # Try multiples of the candidate
#             found = False
#             for mult in range(2, N):
#                 r_try = r_candidate * mult
#                 if r_try >= N:
#                     break
#                 if mod_exp(a, r_try, N) == 1:
#                     r_candidate = r_try
#                     print(f"    Adjusted to r={r_candidate} (multiple)")
#                     found = True
#                     break
#             if not found:
#                 print(f"    a^{r_candidate} mod {N} != 1, not a valid period")
#                 continue
#
#         # Extract factors
#         f1, f2 = extract_factors(a, r_candidate, N)
#         if f1 and f2 and f1 != 1 and f2 != 1 and f1 != N and f2 != N:
#             print(f"    r={r_candidate}: factors {f1} x {f2}")
#             factors_found.add((min(f1, f2), max(f1, f2)))
#         else:
#             print(f"    r={r_candidate}: failed to extract non-trivial factors")
#
#     return factors_found
#
#
# # Simulate what we'd get from exercise 3
# # (Run this after uncommenting exercise 3, or use these known peak values)
# print("Post-processing for a=7, N=15:")
# measured = [0, 4, 8, 12]  # The four expected peaks
# factors = post_process(measured, 4, 7, 15)
# print(f"\nFactors found: {factors}")
# print(f"15 = {list(factors)[0][0]} x {list(factors)[0][1]}" if factors else "No factors found")


# ============================================================
# EXERCISE 5: Full Shor's algorithm for N=15
# ============================================================
# Tie everything together: pick a, build the quantum circuit,
# run it, post-process, and extract factors.
#
# For N=15, the valid values of a (coprime to 15) are:
#   a=2 (period 4), a=4 (period 2), a=7 (period 4),
#   a=8 (period 4), a=11 (period 2), a=13 (period 4), a=14 (period 2)
#
# We demonstrate with a=7 (full quantum circuit) and also verify
# classically with a=11 (period 2):
#   11^1 = 11 mod 15, 11^2 = 121 = 1 mod 15 -> r=2
#   gcd(11^1 + 1, 15) = gcd(12, 15) = 3
#   gcd(11^1 - 1, 15) = gcd(10, 15) = 5
#   15 = 3 x 5
#
# PREDICT: the algorithm outputs 15 = 3 x 5.

print("=" * 50)
print("EXERCISE 5: Full Shor's algorithm for N=15")
print("=" * 50)
print("PREDICT: 15 = 3 x 5\n")

# def shors_circuit(a, N=15, n_counting=4):
#     """Build the full Shor's circuit for factoring N with base a.
#
#     Args:
#         a: The base for modular exponentiation (must be coprime to N).
#         N: The number to factor.
#         n_counting: Number of counting qubits for QPE.
#
#     Returns:
#         A cirq.Circuit implementing the quantum part of Shor's algorithm.
#     """
#     n_work = int(np.ceil(np.log2(N)))  # 4 qubits for N=15
#     counting = cirq.LineQubit.range(n_counting)
#     work = cirq.LineQubit.range(n_counting, n_counting + n_work)
#
#     circuit = cirq.Circuit()
#     # Initialize work register to |1>
#     circuit.append(cirq.X(work[-1]))
#     # Hadamard on counting qubits
#     circuit.append(cirq.H.on_each(*counting))
#
#     # Controlled modular multiplications
#     # counting qubit k controls multiplication by a^(2^(n_counting-1-k)) mod N
#     for k, c_qubit in enumerate(counting):
#         power = 2 ** (n_counting - 1 - k)
#         a_power = pow(a, power, N)
#         if a_power == 1:
#             continue  # Identity, skip
#         circuit.append(controlled_mod_mult(a_power, N, c_qubit, work))
#
#     # Inverse QFT
#     circuit.append(inverse_qft(counting))
#     # Measure
#     circuit.append(cirq.measure(*counting, key='result'))
#     return circuit
#
#
# def shors_algorithm(N, a=None, n_counting=4, shots=1000):
#     """Run Shor's algorithm to factor N.
#
#     Args:
#         N: The integer to factor.
#         a: Base for modular exponentiation (random if None).
#         n_counting: Number of counting qubits.
#         shots: Number of circuit repetitions.
#
#     Returns:
#         Tuple of factors, or None if unsuccessful.
#     """
#     if a is None:
#         # Pick random a coprime to N
#         while True:
#             a = np.random.randint(2, N)
#             if math.gcd(a, N) == 1:
#                 break
#             else:
#                 # Lucky! gcd itself is a factor
#                 other = N // math.gcd(a, N)
#                 return math.gcd(a, N), other
#
#     print(f"Factoring N={N} with a={a}")
#     print(f"  gcd({a}, {N}) = {math.gcd(a, N)} (confirmed coprime)\n")
#
#     # Build and run quantum circuit
#     circuit = shors_circuit(a, N, n_counting)
#     print(f"Circuit ({n_counting} counting + {int(np.ceil(np.log2(N)))} work qubits):")
#     show(circuit, repetitions=shots)
#
#     # Collect measurement results
#     result = simulator.run(circuit, repetitions=shots)
#     counts = result.histogram(key='result')
#
#     print("Measurement histogram:")
#     for val, count in sorted(counts.items()):
#         phase = val / (2 ** n_counting)
#         print(f"  {val:4d} (binary {val:0{n_counting}b}) "
#               f"-> phase {phase:.4f}  (count: {count})")
#
#     # Post-process
#     print("\nPost-processing:")
#     factors = post_process(list(counts.keys()), n_counting, a, N)
#
#     if factors:
#         f1, f2 = list(factors)[0]
#         print(f"\n>>> {N} = {f1} x {f2} <<<")
#         return f1, f2
#     else:
#         print("\nFailed to find factors with this a. Try a different a.")
#         return None
#
#
# # Run Shor's algorithm with a=7
# print("=" * 40)
# print("Shor's algorithm: a=7, N=15")
# print("=" * 40 + "\n")
# shors_algorithm(15, a=7)
#
# print("\n" + "=" * 40)
# print("Verification: a=11, N=15 (classical)")
# print("=" * 40 + "\n")
# # a=11 has period 2: 11^2 = 121 = 1 mod 15
# r = find_period_classical(11, 15)
# print(f"a=11, N=15: period r={r}")
# print(f"  11^(r/2) mod 15 = 11^{r//2} mod 15 = {mod_exp(11, r//2, 15)}")
# f1, f2 = extract_factors(11, r, 15)
# print(f"  gcd({mod_exp(11, r//2, 15)}+1, 15) = gcd(12, 15) = {f1}")
# print(f"  gcd({mod_exp(11, r//2, 15)}-1, 15) = gcd(10, 15) = {f2}")
# print(f"  15 = {f1} x {f2}")
