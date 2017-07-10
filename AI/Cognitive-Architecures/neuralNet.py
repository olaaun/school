from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import TanhLayer

ds = SupervisedDataSet(1,1)
for i in range(1,9):
	ds.addSample(i, i)

neural_network = buildNetwork(1,3,1, hiddenclass=TanhLayer)
trainer = BackpropTrainer(neural_network, ds)
trainer.trainUntilConvergence(verbose=False, validationProportion=0.15, maxEpochs=1000, continueEpochs=10)
for i in range(1,9):
	print(int(round(neural_network.activate([i]))))

print("50 som input: "+str(int(round(neural_network.activate([50])))))
print("-5 som input: "+str(int(round(neural_network.activate([-5])))))
print("5.3 som input: "+str(int(round(neural_network.activate([5.3])))))
