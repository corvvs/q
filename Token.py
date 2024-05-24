from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler

token_file = ".token"
with open(token_file, "r") as f:
	token = f.readline().strip()
	service = QiskitRuntimeService(channel="ibm_quantum", token=token)

	backends = service.backends()

	print("Real quantum computers:")
	for be in backends:
		bs = be.status()
		print("\t{}\t has {:4d} queues with {:3d} qubits".format(be.name, bs.pending_jobs, be.num_qubits))
