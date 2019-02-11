#Code for a simple union find implementation with path compression
#implemented from pseudocode on wikipedia
class UnionFind:
	def __init__(self):
		self._parent = {}
		self._rank = {}
		
	def union(self,x,y):
		xRoot = find(x)
		yRoot = find(y)
		if xRoot != yRoot:
			if self._rank[xRoot] < self._rank[yRoot]:
				self._parent[xRoot] = yRoot
			else
				self._parent[yRoot] = xRoot
				if self._rank[xRoot] == self._rank[yRoot]:
					self._rank[xRoot] = self._rank[xRoot] +1
		pass
		
	def find(self,x):
		if self._parent[x] != x:
			self._parent[x] = find(self._parent[x])
		return self._parent[x]
		
	
	def makeSet(self,x):
		self._parent[x] = x
		self._rank[x] = 0
		pass
		