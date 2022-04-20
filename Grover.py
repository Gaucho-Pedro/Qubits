from matplotlib import pyplot
from qiskit import Aer, transpile, assemble, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import RGQFTMultiplier
from qiskit.visualization import plot_histogram


def integerToArray(number):
    arr = []
    i = 0
    while number > 0:
        if (number % 2) > 0:
            arr.append(i)
        number = number // 2
        i += 1
    return arr


def reverseIntegerToArray(number):
    arr = [i for i in range(6)]
    i = 0
    while number > 0:
        if (number % 2) > 0:
            arr.remove(i)
        number = number // 2
        i += 1
    return arr


def getGroverCircuit(a, b):
    arrA = integerToArray(a)
    arrB = reverseIntegerToArray(b)

    # x*a=b
    qX = QuantumRegister(3, name='x')  # x
    qA = QuantumRegister(3, name='a')  # a
    qB = QuantumRegister(6, name='b')  # b
    output = QuantumRegister(1, name='output')  # Оракул
    c = ClassicalRegister(3, name='c')

    grover_circuit = QuantumCircuit(qX, qA, qB, output, c)

    for i in range(3):
        grover_circuit.h(qX[i])

    for i in arrA:
        grover_circuit.x(qA[i])

    circuit = RGQFTMultiplier(num_state_qubits=3, num_result_qubits=6)
    grover_circuit = grover_circuit.compose(circuit)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit.mct(qB, output)

    for i in arrB:
        grover_circuit.x(qB[i])

    grover_circuit = grover_circuit.compose(circuit.reverse_ops())

    for i in range(3):
        grover_circuit.h(qX[i])
        grover_circuit.x(qX[i])

    grover_circuit.h(qX[2])
    grover_circuit.ccx(qX[0], qX[1], qX[2])
    grover_circuit.h(qX[2])

    for i in range(3):
        grover_circuit.x(qX[i])
        grover_circuit.h(qX[i])

    for i in range(3):
        grover_circuit.measure(qX[i], c[i])

    grover_circuit.draw(output='mpl')
    aer_simulator = Aer.get_backend('aer_simulator')
    plot_histogram(aer_simulator.run(assemble(transpile(grover_circuit, aer_simulator))).result().get_counts())
    pyplot.show()


getGroverCircuit(3, 6)
