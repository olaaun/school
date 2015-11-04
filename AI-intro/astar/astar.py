#Homework
#Illustration of A*-search, compared with Dijkstra and BFS

import math
import heapq
import copy
from PIL import Image
from queue import Queue

class Node():
	parent = None
	x,y = None,None
	g, h, f = None, None, None
	value = None
	iteration = None #Use this to keep track of when node is added to heap. If two nodes have equal f, then FIFO
	children = []
	
	def __init__(self, x, y, value):
		self.x=x
		self.y=y
		self.value=value
	
	def calc_h(self, end):
		self.h = math.fabs(self.x-end.x) + math.fabs(self.y-end.y) #Manhattan distance
		
		
	def find_children(self, board):
		directions = [(-1,0), (1,0),(0,1),(0,-1)] # The four possible directions for children (left, right, down, up)
		children = []
		for direction in directions:
			new_x = self.x+direction[0]
			new_y = self.y+direction[1]
			if 0<=new_x<len(board[0]) and 0<=new_y<len(board) and board[new_y][new_x]!= '#': #If not out of bounds, generate child
				child = Node(new_x,new_y, board[new_y][new_x])
				child.g=self.g+costs[board[child.y][child.x]]
				child.parent = self
				children.append(child)
		return children
	
	#This returns a copy of self. Must be done to avoid children list trouble, i.e. setting two lists as equal and then changing one
	def copy(self):
		node = Node(self.x,self.y, self.value)
		node.children = copy.copy(self.children)
		node.parent = self.parent
		node.g=self.g
		node.h=self.h
		node.f=self.f
		node.iteration=self.iteration
		return node
	
	#Misc operator overloading. Used for e.g. heapq and set in a*
	def __eq__(self, node):
		return self.x==node.x and self.y==node.y		
	def __lt__(self,node):
		if self.f==node.f:
			return self.iteration>node.iteration
		return self.f<node.f
	def __gt__(self,node):
		if self.f==node.f:
			return self.iteration<node.iteration
		return self.f>node.f
	def __str__(self):
		return "x: " +str(self.x) + ", y: "+str(self.y)
	def __hash__(self):
		return int(self.g)
		
def generate_board_from_file(filepath):
	f = open(filepath, 'r')
	board = f.readlines()
	f.close()
	fboard = []
	start = None
	end = None
	for row in range(len(board)):
		fboard.append(list(board[row][:-1]))
		for char in range(len(board[row])):
			if "A" == board[row][char]:
				start = Node(char, row, "A")
				start.g=0
			elif "B" == board[row][char]:
				end = Node(char, row, "B")
	start.calc_h(end)
	start.f = start.h
	return start,end,fboard
	
#Not much worth commenting really. Similar to given pseudo-code
def a_star(start, end, board):
	closed = []
	open = [start]
	nodes = set([start])
	start.iteration=0
	i = 0 #iterator, so we have FIFO at equal f. Improves heuristics
	visited = []
	while open: #while no solution
		parent=heapq.heappop(open)
		closed.append(parent)
		if parent==end:
			end.parent=parent.parent
			break
		children = parent.find_children(board)
		for child in children:
			child.iteration = i+1
			#– If node S* has previously been created, and if state(S*) = state(S), then S <-- S*
			for node in nodes:
				if node==child:
					child = node.copy()			
			nodes.add(child) 
			parent.children.append(child)
			if child not in open and child not in closed:
				attach_and_eval(child,parent, end, board)
				heapq.heappush(open, child)
			elif parent.g+costs[board[child.y][child.x]]<child.g: 
				attach_and_eval(child,parent,end, board)
				if child in closed:
					propagate_path_improvements(child, board)
		i+=1
	return draw_board(start, end, board, closed, open)

def attach_and_eval(child, parent, end, board):
	child.parent=parent
	child.g=parent.g+costs[board[child.y][child.x]]
	child.calc_h(end)
	child.f = child.h + child.g
	
def propagate_path_improvements(parent, board):
	for child in parent.children:
		if parent.g+costs[board[child.y][child.x]]<child.g:
			child.parent=parent
			child.g=parent.g+costs[board[child.y][child.x]]
			child.calc_h(end)
			child.f = child.h + child.g
			propagate_path_improvements(child, board)


def dijkstra(start,end,board):
	open = []
	i = 0 #iterator 
	o = []
	#A heapq of nodes will pop based on f, so we create a tuple where g is first element, and iterator is second. 
	heapq.heappush(open,(0,i,start)) 
	while open:
		node = heapq.heappop(open)[2]
		if node == end:
			end.parent = node.parent
			break
		children = node.find_children(board)
		for child in children:
			child.parent = node
			for q in open:
				o.append(q[2])
			if child not in o:
				heapq.heappush(open,(child.g, i,child))
				i+=1
			else:
				for k in o:
					if k==child and k.g>child.g:
						open.remove(k)
						heapq.heappush(child)
						i+=1
	return draw_board(start,end, board, o, [x[2] for x in open])

def breadth_first_search(start, end, board):
		open = Queue()
		open.put(start)
		visited = [start]
		while not open.empty():
			node = open.get()
			if node == end:
				end.parent=node.parent
				break
			children = node.find_children(board)
			for child in children:
				if child not in visited:
					open.put(child)
					visited.append(child)
		o = []
		while not open.empty():
			o.append(open.get())
		return draw_board(start, end, board, visited, o)

#Take board, add in open/closed nodes and path. Print to console, and return a PILLOW-image		
def draw_board(start, end, board, visited, open):
	for i in visited:
		board[i.y][i.x] = "o" #closed nodes
	for i in open:
		board[i.y][i.x] = "*" #open nodes
	board[start.y][start.x] = "A"
	board[end.y][end.x] = "B"
	parent = end.parent
	while True:
		if parent.parent is not None:
			board[parent.y][parent.x]="x"
			parent=parent.parent
		else:
			break
	for a in board:
		print("".join(a))	
	image = Image.new("RGB", (len(board[0]),len(board)))
	pixels = image.load()
	colors = {"A": (255,0,0), "w":(0,0,255), "g": (0,128,0), "r": (139,69,19), "m": (128,128,128), ".":(255,255,255), "#": (0,0,0),"*":(128,50,128), "B":(0,255,255), "o": (100,200,100), "x": (255,20,100), "f":(0,255,0)}
	for i in range(len(board)):
		for j in range(len(board[0])):
			pixels[j, i] = colors[board[i][j]]
	return image

#Costs, used globally (woops)	
costs = {"w":100, "m": 50, "f": 10, "g": 5, "r": 1, ".": 1, "A": 0, "B": 1}

#Take every board, and save a picture of A*- BFS and Dijkstra-solution
for i in range(1,3):
	for j in range(1,5):
		start, end, board = generate_board_from_file(str(i)+str(j)+".txt")
		a_star(start, end, copy.deepcopy(board)).save("astar"+str(i)+str(j)+".png")
		dijkstra(start, end, copy.deepcopy(board)).save("dijkstra"+str(i)+str(j)+".png")
		breadth_first_search(start, end, copy.deepcopy(board)).save("bfs"+str(i)+str(j)+".png")
