from collections import defaultdict

class Graph():

	def __init__(self, vertices):
		self.graph = defaultdict(list)
		self.V = vertices

	def addEdge(self, u, v):
		self.graph[u].append(v)

	def isCyclicUtil(self, v, visited, Stack):
		visited[v], Stack[v] = True, True
		#recur for all neighbours, if any neighbour is visited and in stack then graph is cyclic
		for neighbour in self.graph[v]:
			if visited[neighbour] == False:
				if self.isCyclicUtil(neighbour, visited, Stack) == True:
					return True
			elif Stack[neighbour] == True:
				return True

		Stack[v] = False
		return False

	def isCyclic(self):
		visited = [False] * self.V
		Stack = [False] * self.V
		for node in range(self.V):
			if visited[node] == False:
				if self.isCyclicUtil(node, visited, Stack) == True:
					return True
		return False