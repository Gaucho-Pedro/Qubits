from matplotlib import pyplot

import Grover
import Multiplier
import Utils

grover_circuit = Grover.getGroverCircuit(a=7, b=21)
grover_circuit.draw(output='mpl')
Utils.plotHistogram(grover_circuit)
pyplot.show()

circuit = Multiplier.QFTMultiplier(num_state_qubits=3, num_result_qubits=6, a=2, b=3)
circuit.draw(output="mpl", filename="img")
print(Utils.getStateVector(circuit))
