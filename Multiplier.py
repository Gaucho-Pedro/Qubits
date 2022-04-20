import numpy
from numpy import pi
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from qiskit.circuit.library import PhaseGate

import Utils


def QFTMultiplier(num_state_qubits, num_result_qubits, a, b):
    qr_a = QuantumRegister(num_state_qubits, name="a")
    qr_b = QuantumRegister(num_state_qubits, name="b")
    qr_out = QuantumRegister(num_result_qubits, name="out")
    qr_c_out = ClassicalRegister(num_result_qubits, name="c_out")

    circuit = QuantumCircuit(qr_out, qr_a, qr_b, qr_c_out, name="name")

    for i in Utils.integerToArray(a):
        circuit.x(qr_a[i])
    for i in Utils.integerToArray(b):
        circuit.x(qr_b[i])

    qft(circuit, num_result_qubits)

    for j in range(1, num_state_qubits + 1):
        for i in range(1, num_state_qubits + 1):
            for k in range(1, num_result_qubits + 1):
                lam = (2 * numpy.pi) / (2 ** (i + j + k - 2 * num_state_qubits))
                circuit.append(
                    PhaseGate(lam).control(2),
                    [qr_a[num_state_qubits - j], qr_b[num_state_qubits - i], qr_out[k - 1]],
                )

    circuit = inverse_qft(circuit, num_result_qubits)

    for i in [i for i in range(num_result_qubits)]:
        circuit.measure(qr_out[i], qr_c_out[i])

    return circuit


def qft(circuit, n):
    qft_rotations(circuit, n)
    return circuit


def qft_rotations(circuit, n):
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi / 2 ** (n - qubit), qubit, n)
    qft_rotations(circuit, n)


def inverse_qft(circuit, n):
    qft_circ = qft(QuantumCircuit(n), n)
    invqft_circ = qft_circ.inverse()
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose()
