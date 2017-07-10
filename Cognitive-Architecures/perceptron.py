import random, copy

class Perceptron():
	weights = [100,100]
	old_weights = [200,200]
	y = None
	learning_rate = None
	theta = None
	delta = [None, None]
	x = [None, None]
	error = 100

	def __init__(self, learning_rate):
			self.weights = [0.1, 0.2]
			self.theta = 0.2
			self.learning_rate=learning_rate

	def train_weights(self):
		for i in range(len(self.delta)):
			self.delta[i] = self.learning_rate*self.x[i]*self.error
			self.weights[i] += self.delta[i]


	def activation(self):
		sum = 0
		for i in range(len(self.weights)):
			sum+=self.weights[i]*self.x[i]
		return 1 if (sum>=self.theta) else 0

	def train_perceptron(self, inputs, outputs):
		self.old_weights = copy.deepcopy(self.weights)
		for i in range(len(inputs)):
			self.x = inputs[i]
			self.y = self.activation()
			self.error = outputs[i]-self.y
			self.train_weights()

	def test_perceptron(self, inputs):
		self.x=inputs
		return self.activation()

	def weights_converged(self):
		for i in range(len(self.weights)):
			if self.weights[i] != self.old_weights[i]:
				return False
		return True

inputs = [[0,0], [0,1], [1,0], [1,1]]
output_and = [0,0,0,1]
output_or =[0,1,1,1]

perceptron = Perceptron(0.1)

while not perceptron.weights_converged():
	perceptron.train_perceptron(inputs, output_or)

print(perceptron.weights)
for i in range(len(inputs)):
	print(perceptron.test_perceptron(inputs[i])==output_or[i])