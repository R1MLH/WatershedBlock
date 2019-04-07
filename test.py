import OOC
import string
import random
from unionfind import UnionFind
import numpy as np

uf = UnionFind()

def nearbyV(Graphe, Vertice, cut = []): # retourne les arc voisins
    rList =[]
    for elt in Graphe.getEdges():
        if Vertice in [elt.getX(), elt.getY()]:
            rList.append(elt) # elt is an edge
    for elt in cut :
        if Vertice in [elt.getX(),elt.getY()]:
            rList.append(elt)
    return rList

def getNeighborVertices(Graphe, Vertice): # retourne les arc voisins
    rList =[] # to be sure that we don't add the same vertice twice
    for elt in Graphe.getEdges():
        if Vertice == elt.getX():
            rList.append(elt.getY()) # elt is a vertice

        if Vertice == elt.getY():
            rList.append(elt.getX()) # elt is a vertice
    return rList

def Fminus(Graphe,cut=[]):
    for elt in Graphe.getVertices():
        elt.setW(min([elt.getW() for elt in nearbyV(Graphe,elt,cut)]))

def localFminus(Graphe,Vertice):
    return min([elt.getW() for elt in nearbyV(Graphe,Vertice)])

def isBorder(edge):
    if(edge.getX().getW()<edge.getW() and edge.getY().getW()== edge.getW()) or (edge.getY().getW()<edge.getW() and edge.getX().getW()== edge.getW()):
        return True
    return False

def isInner(edge):
    if(edge.getX().getW()==edge.getW() and edge.getY().getW()== edge.getW()):
        return True
    return False


def MThinning(Graph,cut=[]):
    step = 0
    #---Step1--- : Minimas
    # for elt in Graph.getEdges():
        # if Rlabels(Graph,elt):
            # elt.getX().setLabel("A")
            # elt.getY().setLabel("A")#a modifier
    #---Step2--- : MThinning
    Fminus(Graph,cut)
    getMinimas(Graph)
    Border = [edge for edge in Graph.getEdges() if (edge.getX().getMinLab() != '0' or edge.getY().getMinLab() != '0')if isBorder(edge)] #get all border edges
    if Border: # if Border not empty
        Border[0].setW(min([Border[0].getX().getW(),Border[0].getY().getW()]))
        MThinning(Graph)
    else :
        return

def BThinning(Graph,cut=[]):
    change = True
    while change == True:
        change = False
        Fminus(Graph,cut)
        for elt in Graph.getEdges():
            if isBorder(elt):
                elt.setW(min(elt.getX().getW(),elt.getY().getW()))
                change = True
                break
    getMinimas(Graph)


def connexeComponent(Graphe):
    nb_comp = 0
    for elt in Graphe.getVertices():
        elt.setLabel("NO_LABEL")
    for x in Graphe.getVertices():
        if x.getLabel() == "NO_LABEL":
            nb_comp = nb_comp +1
            X = [x]
            x.setLabel("IN_X")
            while X:
                y = X[0]
                X.remove(y)
                y.setLabel(nb_comp)
                for z in getNeighborVertices(Graphe,y):
                    if z.getLabel() =="NO_LABEL" and isInner(Graphe.hasEdge(y,z)):
                        X.append(z)
                        z.setLabel("IN_X")
    return

def BlocThinning(B1,B2,cut):
    change = True
    while change == True:
        change = False
        BThinning(B1,cut)
        BThinning(B2,cut)
        for elt in cut :
            if isBorder(elt):
                if B1.hasVertice(elt.getX()):
                    elt.setW(min(localFminus(B1,elt.getX()),localFminus(B2,elt.getY())))
                else :
                    elt.setW(min(localFminus(B2,elt.getX()),localFminus(B1,elt.getY())))
                change = True


def BlocLabelling(B1,B2,cut):
    #connexeComponent(B1)
    #connexeComponent(B2)
    #uniqueLabel([B1,B2])
    changes = 0
    for elt in cut:
        if isInner(elt):
            previousLabel = elt.getY().getLabel()
            newLabel =  elt.getX().getLabel()
            if previousLabel != newLabel:
                changes +=1
                elt.getY().setLabel(newLabel)
                for vertice in B2.getVertices():
                    if vertice.getLabel() == previousLabel :
                        vertice.setLabel(newLabel)
    return changes

def BlocLabelling2(B1,B2,cut):
    connexeComponent(B1)
    connexeComponent(B2)
    uniqueLabel([B1,B2])

    for elt in cut:
        if isInner(elt): # arc interne
            previousLabel = elt.getY().getLabel()
            newLabel =  elt.getX().getLabel()
            elt.getY().setLabel(newLabel)
            for vertice in B2.getVertices():
                if vertice.getLabel() == previousLabel :
                    vertice.setLabel(newLabel)


def uniqueLabel(list_of_blocs):
    alphabet = string.ascii_uppercase

    for i in range (0,len(list_of_blocs)):
        bloc = list_of_blocs[i]
        letter = alphabet[i]
        for vertice in bloc.getVertices():
            label = letter + str(vertice.getLabel())
            uf.makeSet(label) # we use this oportunity to initialize the sets for the UnionFind
            vertice.setLabel(label)


def reLabel(list_of_blocs):
    for bloc in list_of_blocs:
        for vertice in bloc.getVertices():
            label = uf.find(vertice.getLabel())
            vertice.setLabel(label)



def getMinimas(Graph):
    numero = 0
    for x in Graph.getVertices():
        x.setMinLab("UNKNOWN")


    Y = [] # have been explored
    X = [] #to explore

    for x in Graph.getVertices():

        if x.getMinLab() == "UNKNOWN":
            Y.clear()
            X = [x] #X.append(x)
            altitude = x.getW()#weight of each vertice has been calculated in the previous MThinning Step #altitude = F-(x)
            x.setMinLab("EXPLORED")
        while X: #While X is not empty
            y = X[0] # y is a vertice
            X.remove(y)
            Y.append(y)

            #minVerticeNeighborW = min([elt2.getW() for elt2 in nearbyV(Graph,elt)])
            VerticeNeighbors = getNeighborVertices(Graph,y) #VerticeNeighbors = getNeighborVertices(Graph,x)
            # minVerticeNeighborsW = min([neighbor.getW() for neighbor in VerticeNeighbors])

            if ( y.getW() < altitude): # if ( W-(y) < altitude): poids noeuds voisins
                x.setMinLab("NOT_MIN")
                x.setMinLab("NOT_MIN")
            for z in VerticeNeighbors : #for z tq (z,y) € E(G): for z tq (z,y) € E(G)
                if z.getMinLab() == "UNKNOWN": #les points précédents étudiés sont "sautés"
                    edgeZY = Graph.hasEdge(z,y)

                    if edgeZY == None :
                        return "Edge does not exist."
                    # Problème ici : au 2ème tour de boucle, edgeZY == None -> return
                    # if edgeZY.getW() < altitude :# aucun sens, changer
                        # x.setMinLab("NOT_MIN")
                    if (z.getW() == altitude and z.getMinLab()== "UNKNOWN" and edgeZY.getW() == altitude):#edgeZY.getW() == altitude):#if edgeZY.getW() == altitude : #if W({z,y}) == altitude : # MEME PLATEAU
                        X.append(z)
                        z.setMinLab("EXPLORED")
        if len(Y)==1:
            x.setMinLab("NOT_MIN")
        # Ici, Y contient tous les noeuds d'un même plateau
        # X est vide
        if x.getMinLab() != "NOT_MIN":
            if(x.getMinLab() == "EXPLORED"):
                numero = numero +1
            while Y:
                y = Y[0]
                Y.remove(y)
                y.setMinLab(numero)
        else :
            while Y:
                y = Y[0]
                Y.remove(y)
                y.setMinLab(str(0))



def create_graph(X,Y):
    """
    Returns a graph of dimensions X and Y with random weights.
    """
    #tab_vertices[X][Y]

    tab_vertices = [[0 for x in range(Y)] for y in range(X)]
    new_graph = OOC.Graph()
    new_graph.dim_x = X
    new_graph.dim_y = Y

    #creating the vertices
    for i in range (X):
        for j in range (Y):
            tab_vertices[i][j] = OOC.Vertice(str(i)+str(j))
            new_graph.addVertice(tab_vertices[i][j])

    # creating horizontal edges
    for i in range (X):
        for j in range (Y-1):
            weight = random.randint(0,5)
            new_graph.addEdge(OOC.Edge(tab_vertices[i][j],tab_vertices[i][j+1],weight))

    # creating vertical edges
    for j in range (Y):
        for i in range (X-1):
            weight = random.randint(0,5)
            new_graph.addEdge(OOC.Edge(tab_vertices[i][j],tab_vertices[i+1][j],weight))

    return new_graph


def create_graph_file(graph, filename):
    """
    Parameters :
    - The graph that we want to save the information in a file.

    Returns a file containing all the information of the graph given in parameters.
    """
    with open(filename, mode='w+', encoding='utf8') as f:

        f.write("#rs "+str(graph.dim_x)+" cs "+ str(graph.dim_y) + "\n")
        f.write(str(len(graph.vertices)) + " " + str(len(graph.edges)) + "\n")

        f.write("val sommets\n")
        for vertice in graph.vertices:
            f.write(vertice.name + " 1" +"\n")

        f.write("arcs values\n")
        for edge in graph.edges:
            f.write(edge.x.name + " " + edge.y.name + " " + str(edge.weight)+ "\n")

def fill_graph_with_file(filename):

    """
    Parameters :
    - The name of the file that contains all the information to produce a given graph. The file must hast a particular structure

    Returns a graph filled with the information available in the file given in parameters.
    """
    new_graph = OOC.Graph() #Graph to fill

    with open(filename, mode = "r", encoding = "utf8") as f :
        lines = f.read().splitlines() #list of string containing all lines of the file

        #1st line : get nb columns/nb rows of the graph
        rs_cs = lines[0]
        rs_cs = rs_cs.replace("#rs","").replace("cs"," ")
        new_graph.dim_x, new_graph.dim_y = [int(x) for x in rs_cs.split()]

        #2nd line : get nb vertices/nb edges
        nb_v_e = lines[1]
        nb_vertices, nb_edges = [int(x) for x in nb_v_e.split()]

        # Check consistency with previous data
        m = new_graph.dim_x
        n = new_graph.dim_y
        if nb_vertices != m*n:
            print('Incoherent nb vertices and dimensions')
            return

        if nb_edges != (m-1)*n +(n-1)*m:
            print("Incoherent nb edges and dimensions")
            return

        #3rd line : get interesting indexes
        index1 = lines.index("val sommets")
        index2 = lines.index("arcs values")

        #get "val sommets" : name of vertices
        vals_sommets = [x.split() for x in lines[index1+1:index2]]
        new_graph.vertices.extend([OOC.Vertice(sommet[0]) for sommet in vals_sommets])

        #get "arcs values" : edges
        arcs_values = [x.split() for x in lines[index2+1:]]
        new_graph.edges.extend([OOC.Edge(OOC.Vertice(edge[0]),OOC.Vertice(edge[1]),int(edge[2])) for edge in arcs_values])

        # Check consistency with previous data
        if nb_vertices != len(new_graph.vertices) or nb_edges != len(new_graph.edges):
            print('Incoherent X or Y dimensions')
            return

        return new_graph

def divide_blocks(Graph, nrows, ncols):

    """
    Parameters :
    - Graph to cut
    - size of the blocks (nb of rows and cols)

    Returns a list of graphs. The graphs are subgraphs/blocks of the initial graph given in parameters.
    The cut attribute (graph.cut) contains a list of all adjacent edges.

    """

    sub_graphs = [] # list containing all the blocs (sub graphs)
    Graph.vertices = np.array(Graph.vertices)
    B = np.reshape(Graph.vertices, (-1, Graph.dim_y))

    h, w = B.shape
    C = B.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols)

    print("B =\n",B) # "grid" initial graph
    print("C =\n",C) # "grid" subgraphs/blocks

    for block in C:
        new_graph = OOC.Graph()
        new_graph.dim_x = nrows
        new_graph.dim_y = ncols

        for line in block:
            for vertice in line:
                new_graph.addVertice(vertice) # add each element to the list of vertices
                sg_edges,sg_cut_edges = Graph.adjacentEdge(vertice, new_graph.vertices)

                new_graph.edges.extend(sg_edges)
                new_graph.cut.extend(sg_cut_edges)

        new_graph.edges = list(set (new_graph.edges))
        new_graph.cut = set(new_graph.cut).difference(new_graph.edges)
        sub_graphs.append(new_graph)

    #print(sub_graphs[1].edges)
    #print("\n",sub_graphs[1].cut)
    return sub_graphs




def label_composante_connexe(graphe,taille_bloc):
    blocs = divide_blocks(graphe,taille_bloc,taille_bloc)
    for i in blocs:
        connexeComponent(i)
    uniqueLabel(blocs)
    for i in blocs:
        for edge in i.cut:
            if isInner(edge):
                uf.union(edge.x.label,edge.y.label)
    reLabel(blocs)
    return blocs




def main():

    graph1 = create_graph(9,9) #create a random graph

    print("----- PRINT GRAPH 1 -----")
    graph1.affiche()

    create_graph_file(graph1, "file.graph") #save it in a file


    graph2 = fill_graph_with_file("file.graph") #read this file save it in another graph
    print("----- PRINT GRAPH 2 -----")
    graph2.affiche() # should have graph1 = graph2

    print("----- DIVIDE BLOCKS -----")
    divide_blocks(graph1,3,3)

    print("----- test label---------")
    for b in label_composante_connexe(graph1,3):
        b.affiche()


if __name__ == '__main__':
    main()
