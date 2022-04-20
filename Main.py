from matplotlib import pyplot

import Grover
import Utils

grover_circuit = Grover.getGroverCircuit(2, 4)
grover_circuit.draw(output='mpl')
Utils.plotHistogram(grover_circuit)
pyplot.show()
