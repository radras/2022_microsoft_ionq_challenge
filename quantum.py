import random
import numpy as np

from qiskit import QuantumCircuit
from qiskit.opflow import CircuitStateFn
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.opflow import PauliExpectation, CircuitSampler, StateFn
from qiskit.opflow import X, Y, Z, I
from qiskit.circuit import Parameter

def exp_val(params, circ, H, simulation=True, n_shots=1024, backend_name='qasm_simulator'):
    theta = circ.parameters
    circ = circ.bind_parameters({theta[i]: params[i] for i in range(len(params))})
    psi = CircuitStateFn(circ)
    
    if simulation:
        return psi.adjoint().compose(H).compose(psi).eval().real
    else:
        backend = Aer.get_backend(backend_name) 
        q_instance = QuantumInstance(backend, shots=n_shots)
        measurable_expression = StateFn(H, is_measurement=True).compose(psi) 
        expectation = PauliExpectation().convert(measurable_expression)  
        sampler = CircuitSampler(q_instance).convert(expectation) 

        return sampler.eval().real

def hamiltonian(n_qubits):
    if n_qubits == 2:
        return ((5 * I^I) + (-1 * X^X) + (-3 * Y^Y) + (1 * Z^Z)) / 8
    if n_qubits == 3:
        return (I^I^I + I^Z^Z + Z^I^Z + Z^Z^I + X^X^X - X^Y^Y - Y^X^Y - Y^Y^X) / 8

def pqc(n_qubits):
    theta = [Parameter('θ_' + str(i)) for i in range(n_qubits)]

    circ = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        circ.rx(theta[i], i)
    circ.h(0)
    for i in range(n_qubits - 1):
        circ.cx(i, i + 1)
    
    return circ
