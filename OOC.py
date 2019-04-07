import collections

class Graph:
    def __init__(self):
        self.vertices=[]
        self.edges= []
        self.dim_x = None
        self.dim_y = None

        self.cut = []

    def addVertice(self,V):
        self.vertices.append(V)

    def addEdge(self,edge):
        # un edge doit lier deux vertices
        self.edges.append(edge)

    def delEdge(self, edge):
        self.edges.remove(edge)

    def getVertices(self):
        return self.vertices

    def getEdges(self):
        return self.edges

    def affiche(self):
        print("Vertices :")
        print("[ ",end='')
        for vert in self.vertices:
            print(str(vert) +':' + vert.label+" ",end = '')
        print(']')
        print("Edges : ")
        print("[ ",end='')
        for edg in self.edges:
            print(str(edg)+' ',end ='')
        print(']')

    def hasEdge(self,x,y):
        for edge in self.getEdges():
            if edge.getX() == x and edge.getY() == y :
                return edge
            elif edge.getX() == y and edge.getY() == x :
                return edge
        return None

    def adjacentEdge(self,x, list_vertices):
        sg_edges = []
        sg_cut_edges = []
        for edge in self.getEdges():
            if edge.getX() == x :
                if edge.getY() in list_vertices: # edge of the subgraph
                    sg_edges.append(edge)
                else:  #cut edge
                    sg_cut_edges.append(edge)
            elif edge.getY() == x :
                if edge.getX() in list_vertices: # edge of the subgraph
                    sg_edges.append(edge)
                else:  #cut edge
                    sg_cut_edges.append(edge)
        return sg_edges,sg_cut_edges

    def hasVertice(self,x):
        for vert in self.getVertices():
            if vert == x:
                return True
        return False


class Edge:
    def __init__(self,a,b,w):
        self.x = a
        self.y = b
        self.weight =w
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getW(self):
        return self.weight
    def setW(self,w):
        self.weight = w
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")(w = "+str(self.weight)+')'+"\n"
    def __repr__(self):
        return self.__str__()


class Vertice:
    def __init__(self,x,y = 0):
        self.name = x
        self.weight = y
        self.label = ""
        self.min_lab = ""
    def getLabel(self):
        return self.label
    def setW(self,w):
        self.weight = w
    def getW(self):
        return self.weight
    def setLabel(self,str):
        self.label = str
    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return self.__str__()

    def getName(self):
        return self.name
    def getMinLab(self):
        return self.min_lab

    def setMinLab(self,ml):
        self.min_lab = ml

    # def isVerticeOf(self, edge):
        # if (edge.getX() == self) or (edge.getY() == self):
            # return True
