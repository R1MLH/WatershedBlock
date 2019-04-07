#Code for a simple union find implementation with path compression
#implemented from pseudocode on wikipedia
class UnionFind:
	def __init__(self):
		self._parent = {}
		self._rank = {}

	def find(self,x):
		if self._parent[x] != x:
			self._parent[x] = self.find(self._parent[x])
		return self._parent[x]

	def makeSet(self,x):
		self._parent[x] = x
		self._rank[x] = 0
		pass

	def union(self,x,y):
		xRoot = self.find(x)
		yRoot = self.find(y)
		if xRoot != yRoot:
			if self._rank[xRoot] < self._rank[yRoot]:
					self._parent[xRoot] = yRoot
			else:
				self._parent[yRoot] = xRoot
				if self._rank[xRoot] == self._rank[yRoot]:
					self._rank[xRoot] = self._rank[xRoot] +1
		pass
