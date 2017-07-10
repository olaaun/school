import random, operator
from math import log

class Node:
	children = None
	parent = None
	data = None
	leaf = None

	def __init__(self, data, leaf):
		self.data = data
		self.children = {}
		self.leaf = leaf

	def add_child(self, child, value):
		self.children[value] = child

#Entropy
def B(positive, negative):
	if positive == 0:
		return 0
	q = positive/(positive+negative)
	if(q<0 or q>=1):
		return 0
	return -(q*log(q,2)+(1-q)*log(1-q, 2))

#Returns most often occuring class
def plurality_value(data):
	counter = {}
	for occ in data:
		try:
			counter[occ[-1]] +=1
		except:
			counter[occ[-1]] = 0
	max_val = 0
	preferred_key = 0
	for key, val in counter.items():
		if val > max_val:
			preferred_key = key
	return preferred_key

#Check if every sample is of same class
def same_class(examples):
	first_class = examples[0][-1]
	for i in examples:
		if first_class != i[-1]:
			return False
	return True


def choose_attribute(attributes, examples, random_importance, pv):
	if random_importance:
		index = random.randint(0, len(attributes)-1)
		return index, attributes[index]
	# Find attribute with highest expected information gain. Based on the equations in the book.
	n = len(examples)
	positive_occurences = len([i for i in examples if pv==i[-1]])
	negative_occurences = n - positive_occurences	
	entropy = B(positive_occurences, negative_occurences)
	max_gain = -1
	index = 0
	for attribute in attributes:
		attribute_is_one = [i for i in examples if i[attribute] == 1]	
		posistive_ones = [i for i in attribute_is_one if i[-1] == pv]
		attribute_is_two = [i for i in examples if i[attribute] == 2]
		posistive_twos = [i for i in attribute_is_two if i[-1] == pv]
		remainder = (len(attribute_is_one)/n)*B(len(posistive_ones), len(attribute_is_one)-len(posistive_ones))
		remainder += (len(attribute_is_two)/n)*B(len(posistive_twos), len(attribute_is_two)-len(posistive_twos))
		gain = entropy - remainder
		if gain > max_gain:
			max_gain = gain
			preferred_attribute = index
		index+=1
	return preferred_attribute, attributes[preferred_attribute]

#Returns percentage of correct classifications
def test_tree(tree, attributes, test_set):
	correct_classifications = 0
	for test in test_set:
		node = tree
		#Traverse the tree using the attributes of test
		while not node.leaf:
			node = node.children[test[node.data]]
		if node.data == test[-1]:
			correct_classifications+=1
	return 100.0*correct_classifications/len(test_set)

#Based on pseudo code in the book
def DTL(examples, attributes, parent_example, random_importance=False):
	pv = plurality_value(examples)
	if not examples:
		return Node(plurality_value(parent_example), True)
	elif same_class(examples):
		return Node(examples[0][-1], True)
	elif not attributes:
		return Node(pv, True)
	else:
		best, data = choose_attribute(attributes, examples, random_importance, pv)
		root = Node(data, False)
		for v in range(1,3):
			ex = [i for i in examples if i[best] == v]
			subtree = DTL(ex, list(attributes[:best])+list(attributes[best+1:]), examples, random_importance)
			root.children[v] = subtree
	#Check if both subtrees are leaf nodes. If they are, and have same class, then set current tree as a leaf node with that class.
	#Removes redundancy in tree
	if root.children[1].leaf and root.children[2].leaf and root.children[1].data==root.children[2].data:
		root = Node(root.children[1].data, True)
	return root


def print_tree(tree):
	text_tree = ""
	queue = [(tree, ["root"])]
	while queue:
		node, depth = queue.pop(0)
		q = str(node.data)
		l = " leaf" if node.leaf else ""
		for key, child in node.children.items():
			queue.append((child, depth + [str(key)]))
		text_tree += str(" -> ".join(depth))+ ": " + str(q) + l + "\n"
	return text_tree


f = open('data\\training.txt', 'r')
data_set = [''.join(i.split()) for i in f.readlines()]
f.close()
examples = []
for data in data_set:
	examples.append(list(map(int,data)))

#Construct trees
random_tree = DTL(examples, list(range(0,7)), 1, True)
non_random_tree = DTL(examples, list(range(0,7)), 1, False)

f = open('data\\test.txt', 'r')
test_read = [''.join(i.split()) for i in f.readlines()]
f.close()
test_set = []
for test in test_read:
	test_set.append(list(map(int, test)))

#Test both trees
random_result = test_tree(random_tree, list(range(0,7)), test_set)
non_random_result = test_tree(non_random_tree, list(range(0,7)), test_set)
print("Results using random splits: " + "{0:.2f}".format(random_result) +"%")
print("Results using non-random attribute splits: " + "{0:.2f}".format(non_random_result) + "%")

#Print the trees, and write to file for easy copy to PDF
non_random_print = print_tree(non_random_tree)
random_print = print_tree(random_tree)
print("\nStructure of non-random tree: \n" +non_random_print)
print("\nStructure of random tree;\n" +random_print)

f = open("write_tree.txt", "w")
f.write(non_random_print + "\n")
f.write(random_print)