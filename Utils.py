from qiskit.visualization import plot_histogram
from qiskit import Aer, transpile, assemble, execute, QuantumCircuit


def plotHistogram(circuit):
    aer_simulator = Aer.get_backend('aer_simulator')
    plot_histogram(aer_simulator.run(assemble(transpile(circuit, aer_simulator))).result().get_counts())


def getStateVector(circuit: QuantumCircuit):
    aer_simulator = Aer.get_backend('statevector_simulator')
    return execute(circuit, aer_simulator).result().get_counts()


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
