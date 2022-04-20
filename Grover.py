from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import RGQFTMultiplier

import Utils


# Функция для поиска корня уравнения вида x*a=b. x и a - по три кубита, b - шесть кубитов
def getGroverCircuit(a, b):
    arrA = Utils.integerToArray(a)
    arrB = Utils.reverseIntegerToArray(b)

    # x*a=b
    qX = QuantumRegister(3, name='x')  # x
    qA = QuantumRegister(3, name='a')  # a
    qB = QuantumRegister(6, name='b')  # b
    output = QuantumRegister(1, name='output')  #
    c = ClassicalRegister(3, name='c')

    grover_circuit = QuantumCircuit(qX, qA, qB, output, c)

    grover_circuit.h(qX)

    for i in arrA:
        grover_circuit.x(qA[i])

    grover_circuit.x(output)
    grover_circuit.h(output)
    # Первая итерация
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

    # Вторая итерация
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
