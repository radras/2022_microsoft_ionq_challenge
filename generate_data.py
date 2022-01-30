from stat import filemode
import numpy as np
from quantum import exp_val, hamiltonian, pqc

grid_size = 10

for n_qubits in [2, 3]:
    circ = pqc(n_qubits)
    circ.draw(output='latex', filename="pqc_" + str(n_qubits) + ".png")

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
                                            circ, H, simulation=False)

    np.save("data_" + str(n_qubits) + "_qubits.npy", E)


import sympy
sympy.preview(r'$$H = \frac{5}{8} - \frac{1}{8}XX - \frac{3}{8}YY + \frac{1}{8}ZZ$$', 
                viewer='file', filename='hamiltonian_2.png', 
                euler=False, dvioptions=['-D','120'])

sympy.preview(r'$$H = \frac{1}{8} + \frac{1}{8}IZZ + \frac{1}{8}ZIZ + \frac{1}{8}ZZI + \dots$$', 
                viewer='file', filename='hamiltonian_3.png', 
                euler=False, dvioptions=['-D','120'])