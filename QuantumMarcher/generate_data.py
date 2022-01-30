from stat import filemode
import numpy as np
from quantum import exp_val, hamiltonian, pqc

grid_size = 10

for n_qubits in [2, 3]:
    circ = pqc(n_qubits)
    circ.draw(output='latex', filename="QuantumMarcher/pqc_" + str(n_qubits) + ".png")

    H = hamiltonian(n_qubits)

    E = np.zeros(tuple([grid_size for i in range(n_qubits)]))
    p = np.linspace(0, 1, grid_size)

    if n_qubits == 2:
        for i in range(grid_size):
            for j in range(grid_size):
                E[i, j] = exp_val(np.pi * np.array([p[i], p[j]]), circ, H)
    else:
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    E[i, j, k] = exp_val(np.pi * np.array([p[i], p[j], p[k]]), 
                                            circ, H, simulation=True)

    np.save("QuantumMarcher/data_" + str(n_qubits) + "_qubits.npy", E)


import sympy
sympy.preview(r'$$H = \frac{5}{8} - \frac{1}{8}X_1X_2 - \frac{3}{8}Y_1Y_2 + \frac{1}{8}Z_1Z_2$$', 
                viewer='file', filename='QuantumMarcher/hamiltonian_2.png', 
                euler=False, dvioptions=['-D','120'])

sympy.preview(r'$$H = Z_1Z_2 + Z_2Z_3 + X_1 + X_2 + X_3$$', 
                viewer='file', filename='QuantumMarcher/hamiltonian_3.png', 
                euler=False, dvioptions=['-D','120'])