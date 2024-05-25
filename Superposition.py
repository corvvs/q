from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

qc = QuantumCircuit(1, 1) # 量子ビット1つ, 古典ビット1つ(測定結果用)
qc.h(0) # アダマールゲートを1つかます
qc.measure([0], [0]) # 量子ビット(左) を測定し, 結果を古典ビット(右) に格納

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
