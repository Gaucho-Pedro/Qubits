from qiskit.visualization import plot_histogram
from qiskit import Aer, transpile, assemble


def plotHistogram(circuit):
    aer_simulator = Aer.get_backend('aer_simulator')
    plot_histogram(aer_simulator.run(assemble(transpile(circuit, aer_simulator))).result().get_counts())
