from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import matplotlib.pyplot as plt

def superposition(n):
	# n個の量子ビット, n個の古典ビットを持つ回路を生成する
	# (古典ビットは測定に使う)
	qc = QuantumCircuit(n, n)

	# すべての量子ビットにアダマールゲートをかける
	for i in range(n):
		qc.h(i)

	# 量子ビット(左) を測定し, 結果を古典ビット(右) に格納
	qc.measure(range(n), range(n))

	return qc

def entanglement():
	qc = QuantumCircuit(2, 2)
	qc.h(0)
	qc.cx(0, 1)
	qc.measure([0, 1], [0, 1])
	return qc

# qubit_num: 関数 f がとる量子ビットの数
# oracle: 関数 f を実装したオラクル(入力は qubit_num + 1, 出力も qubit_num + 1)
def deustch_jozsa(qubit_num, oracle):
	qc = QuantumCircuit(qubit_num + 1, qubit_num)
	qc.x(qubit_num)
	qc.h(range(qubit_num + 1))
	subc = oracle()
	qc.append(subc.to_instruction(), range(qubit_num + 1))
	qc.h(range(qubit_num))
	qc.measure(range(qubit_num), range(qubit_num))
	return qc

class Oracle2:

	@classmethod
	def ux0000(cls):
		oracle = QuantumCircuit(3, name='Ux')
		return oracle

	@classmethod
	def ux0011(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.cx(0, 2)
		return oracle

	@classmethod
	def ux0110(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.cx(0, 2)
		oracle.cx(1, 2)
		return oracle

	@classmethod
	def ux0101(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.cx(1, 2)
		return oracle

	@classmethod
	def ux1001(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.x(0)
		oracle.cx(0, 2)
		oracle.x(0)
		oracle.x(1)
		oracle.cx(1, 2)
		oracle.x(1)
		return oracle

	@classmethod
	def ux1010(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.x(0)
		oracle.cx(0, 2)
		oracle.x(0)
		return oracle

	@classmethod
	def ux1100(cls):
		oracle = QuantumCircuit(3, name='ux0011')
		oracle.x(1)
		oracle.cx(1, 2)
		oracle.x(1)
		return oracle

	@classmethod
	def ux1111(cls):
		oracle = QuantumCircuit(3, name='ux1111')
		oracle.x(2)
		return oracle

class Oracle3:

	@classmethod
	def ux00000000(cls):
		# example constant
		oracle = QuantumCircuit(4, name='ux00000000')
		return oracle

	@classmethod
	def ux01101001(cls):
		# example balanced
		oracle = QuantumCircuit(4, name='ux01101001')
		oracle.cx(0, 3)
		oracle.cx(1, 3)
		oracle.cx(2, 3)
		return oracle

	@classmethod
	def ux01100101(cls):
		oracle = QuantumCircuit(4, name='ux01100101')
		oracle.x(0)
		oracle.ccx(0, 1, 2)
		oracle.cx(2, 3)
		oracle.ccx(0, 1, 2)
		oracle.x(0)
		return oracle

	@classmethod
	def ux00111100(cls):
		oracle = QuantumCircuit(4, name='ux00111100')
		oracle.cx(0, 3)
		oracle.cx(1, 3)
		return oracle

	@classmethod
	def ux00010111(cls):
		oracle = QuantumCircuit(4, name='ux00010111')
		oracle.ccx(0, 1, 3)
		oracle.ccx(0, 2, 3)
		oracle.ccx(1, 2, 3)
		return oracle

	@classmethod
	def ux01010110(cls):
		oracle = QuantumCircuit(4, name='ux01010110')
		oracle.ccx(0, 1, 2)
		oracle.cx(2, 3)
		oracle.ccx(0, 1, 2)
		return oracle

	@classmethod
	def ux_ex(cls):
		oracle = QuantumCircuit(4, name='ux_ex')
		oracle.x(0)
		oracle.x(2)
		oracle.cx(0, 3)
		oracle.cx(1, 3)
		oracle.cx(2, 3)
		oracle.x(0)
		oracle.x(2)
		return oracle

def run_by_simulator(qc, shot_count=500):
	simulator = AerSimulator()

	pm = generate_preset_pass_manager(backend=simulator, optimization_level=1)
	isa_circuits = pm.run([qc])

	sampler = Sampler(simulator)
	job = sampler.run(isa_circuits, shots=shot_count)
	print("job_id: {}".format(job.job_id()))
	result = job.result()
	r = result[0]
	d = r.data
	c = next(iter(d.values()))

	counts = c.get_counts()
	# print(counts)
	# Normalize
	for k, v in counts.items():
		counts[k] = v / float(shot_count)
	plot_histogram(counts).show()
	plt.show()

def get_service(token_file):
	service = None
	with open(token_file, "r") as f:
		token = f.readline().strip()
		service = QiskitRuntimeService(channel="ibm_quantum", token=token)
	return service

def run_by_backend(qc, backend, shot_count = 500):

	pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
	isa_circuits = pm.run([qc])

	sampler = Sampler(backend)
	job = sampler.run(isa_circuits, shots=shot_count)
	print("job_id: {}".format(job.job_id()))
	result = job.result()
	r = result[0]
	d = r.data
	c = next(iter(d.values()))
	counts = c.get_counts()

	# Normalize
	for k, v in counts.items():
		counts[k] = v / float(shot_count)
	plot_histogram(counts).show()
	plt.show()

if __name__ == "__main__":
	ux = Oracle3.ux00010111
	qc = deustch_jozsa(3, ux)
	run_by_simulator(qc)
