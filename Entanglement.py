from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

qc = QuantumCircuit(2, 2) # 量子ビット2つ, 古典ビット2つ(測定結果用)
qc.h(0) # qbit0 にアダマールゲートをかける
qc.cx(0, 1) # qbit0 cnot qbit1
qc.measure([0, 1], [0, 1]) # 測定

simulator = AerSimulator()
shot_count = 500
job = simulator.run(qc, shots=shot_count) # 500ショット繰り返す
result = job.result()

counts = result.get_counts() # 古典ビット#0 の状態がそれぞれ0/1だった回数を辞書で返す
# print("Counts:", counts)
# Normalize
for k, v in counts.items():
	counts[k] = v / float(shot_count)
plot_histogram(counts).show()
plt.show()
