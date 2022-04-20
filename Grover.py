from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import RGQFTMultiplier


def __integerToArray(number):
    arr = []
    i = 0
    while number > 0:
        if (number % 2) > 0:
            arr.append(i)
        number = number // 2
        i += 1
    return arr


def __reverseIntegerToArray(number):
    arr = [i for i in range(6)]
    i = 0
    while number > 0:
        if (number % 2) > 0:
            arr.remove(i)
        number = number // 2
        i += 1
    return arr


def getGroverCircuit(a, b):
    arrA = __integerToArray(a)
    arrB = __reverseIntegerToArray(b)

    # x*a=b
    qX = QuantumRegister(3, name='x')  # x
    qA = QuantumRegister(3, name='a')  # a
    qB = QuantumRegister(6, name='b')  # b
    output = QuantumRegister(1, name='output')  # Оракул
    c = ClassicalRegister(3, name='c')

    grover_circuit = QuantumCircuit(qX, qA, qB, output, c)

    grover_circuit.h(qX)

    for i in arrA:
        grover_circuit.x(qA[i])

    grover_circuit.x(output)
    grover_circuit.h(output)
    # First iteration
    circuit = RGQFTMultiplier(num_state_qubits=3, num_result_qubits=6)
    grover_circuit = grover_circuit.compose(circuit)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit.mct(qB, output)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit = grover_circuit.compose(circuit.reverse_ops())

    grover_circuit.h(qX)
    grover_circuit.x(qX)

    grover_circuit.h(qX[2])
    grover_circuit.ccx(qX[0], qX[1], qX[2])
    grover_circuit.h(qX[2])

    grover_circuit.x(qX)
    grover_circuit.h(qX)

    # Second iteration
    circuit = RGQFTMultiplier(num_state_qubits=3, num_result_qubits=6)
    grover_circuit = grover_circuit.compose(circuit)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit.mct(qB, output)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit = grover_circuit.compose(circuit.reverse_ops())

    grover_circuit.h(qX)
    grover_circuit.x(qX)

    grover_circuit.h(qX[2])
    grover_circuit.ccx(qX[0], qX[1], qX[2])
    grover_circuit.h(qX[2])

    grover_circuit.x(qX)
    grover_circuit.h(qX)
    #
    for i in range(3):
        grover_circuit.measure(qX[i], c[i])

    return grover_circuit
