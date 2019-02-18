import OOC
import string
import random

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
            if previousLabel != newLabel
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
    i = 0 ;
    for i in range (0,len(list_of_blocs)):
        bloc = list_of_blocs[i]
        letter = alphabet[i]
        for vertice in bloc.getVertices():
            vertice.setLabel(letter + str(vertice.getLabel()))
        i+=1

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
    # X = imsize.len_x
    # Y = imsize.len_y

    new_graph = OOC.Graph()
    n =  X*Y

    for i in range (X):
        for j in range(Y):
            new_graph.addVertice(OOC.Vertice(str(i)+str(j)))


    for i in range (X):
        for j in range(1,Y):
            # print("i :",i,"\n");
            # print("j :",j,"\n");
            weight = random.randint(0,5)
            new_graph.addEdge(OOC.Edge(new_graph.vertices[i*Y+j-1],new_graph.vertices[i*Y+j],weight))

            #vertices = new_graph.getVertices()
            #[vertice[i] if vertice[i] == ]


            if i is not 0:
                weight = random.randint(0,5)
                new_graph.addEdge(OOC.Edge(new_graph.vertices[(i-1)*Y+j],new_graph.vertices[i*Y+j],weight))
                # print("i :",i,"\n");
                # print("j :",j,"\n");
            #else :






        # for k in range(1,Y):
            # weight = random.randint(0,5)
            # new_graph.addEdge(OOC.Edge(new_graph.vertices[k-1],new_graph.vertices[k],weight))

    return new_graph



# def create_graph(X,Y):
    # # X = imsize.len_x
    # # Y = imsize.len_y

    # new_graph = OOC.Graph()

    # edges = []
    # for y in range(Y):
        # for x in range(X):
            # pos = x + y * X
            # eq1 = x + 1 + y * X
            # if x + 1 < X:
                # weight = random.randint(0,5)
                # new_graph.addEdge(OOC.Edge(new_graph.vertices[pos],new_graph.vertices[eq1],weight))
            # eq2 = x + (y + 1) * X
            # if y + 1 < Y:
                # edges.append((pos, eq2))
                # weight = random.randint(0,5)
                # new_graph.addEdge(OOC.Edge(new_graph.vertices[pos],new_graph.vertices[eq2],weight))
     # #weights = [abs(int(i)) for i in np.random.normal(110, 40, len(edges))]

    # #graph1 = Graph(n_vertices=X * Y, edges=edges, weights=weights)
    # return new_graph



# def cut_graph(graph,dimensions,nb_x,nb_y):
    # for nb_x
    # return cuts




def label_composante_connexe(graphe,taille_bloc):
    blocs,cuts = cut_graph(graphe,taille_bloc)
    for i in blocs:
        connexeComponent(i)
    uniqueLabel(blocs)
    changes = 1
    while(changes !=0):
        changes = 0
        for i in range(0,len(blocs)):
            for j in range(0,len(blocs)):
                changes += BlocLabelling(blocs[i],blocs[j],cuts[i][j])








def main():
    # MGraph = OOC.Graph()
    B1 = OOC.Graph()
    B2 = OOC.Graph()
    cut = []

    # Point1= OOC.Vertice("A",0)
    # Point2= OOC.Vertice("B",0)
    # Point3= OOC.Vertice("C",0)
    # Point4= OOC.Vertice("D",0)
    # Point5= OOC.Vertice("E",0)
    # Point6= OOC.Vertice("F",0)
    # Point7= OOC.Vertice("G",0)
    # Point8= OOC.Vertice("H",0)
    # Point9= OOC.Vertice("I",0)
    # Edge1 = OOC.Edge(Point1,Point2,0)
    # Edge2 = OOC.Edge(Point2,Point3,2)
    # Edge3 = OOC.Edge(Point1,Point4,0)
    # Edge4 = OOC.Edge(Point2,Point5,1)
    # Edge5 = OOC.Edge(Point3,Point6,2)
    # Edge6 = OOC.Edge(Point4,Point5,1)
    # Edge7 = OOC.Edge(Point5,Point6,2)
    # Edge8 = OOC.Edge(Point4,Point7,1)
    # Edge9 = OOC.Edge(Point5,Point8,2)
    # Edge10 = OOC.Edge(Point6,Point9,1)
    # Edge11 = OOC.Edge(Point7,Point8,2)
    # Edge12 = OOC.Edge(Point8,Point9,1)

    # MGraph.addVertice(Point1)
    # MGraph.addVertice(Point2)
    # MGraph.addVertice(Point3)
    # MGraph.addVertice(Point4)
    # MGraph.addVertice(Point5)
    # MGraph.addVertice(Point6)
    # MGraph.addVertice(Point7)
    # MGraph.addVertice(Point8)
    # MGraph.addVertice(Point9)

    # MGraph.addEdge(Edge1)
    # MGraph.addEdge(Edge2)
    # MGraph.addEdge(Edge3)
    # MGraph.addEdge(Edge4)
    # MGraph.addEdge(Edge5)
    # MGraph.addEdge(Edge6)
    # MGraph.addEdge(Edge7)
    # MGraph.addEdge(Edge8)
    # MGraph.addEdge(Edge9)
    # MGraph.addEdge(Edge10)
    # MGraph.addEdge(Edge11)
    # MGraph.addEdge(Edge12)

    PointA= OOC.Vertice("A",0)
    PointB= OOC.Vertice("B",0)
    PointC= OOC.Vertice("C",0)
    PointD= OOC.Vertice("D",0)
    PointE= OOC.Vertice("E",0)
    PointF= OOC.Vertice("F",0)
    PointG= OOC.Vertice("G",0)
    PointH= OOC.Vertice("H",0)
    PointI= OOC.Vertice("I",0)
    PointJ= OOC.Vertice("J",0)
    PointK= OOC.Vertice("K",0)
    PointL= OOC.Vertice("L",0)
    PointM= OOC.Vertice("M",0)
    PointN= OOC.Vertice("N",0)
    PointO= OOC.Vertice("O",0)
    PointP= OOC.Vertice("P",0)

    Edge1 = OOC.Edge(PointA,PointB,0)
    Edge2 = OOC.Edge(PointB,PointC,0)
    Edge3 = OOC.Edge(PointC,PointD,0)
    Edge4 = OOC.Edge(PointA,PointE,1)
    Edge5 = OOC.Edge(PointB,PointF,4)
    Edge6 = OOC.Edge(PointC,PointG,3)
    Edge7 = OOC.Edge(PointD,PointH,2)
    Edge8 = OOC.Edge(PointE,PointF,3)
    Edge9 = OOC.Edge(PointF,PointG,5)
    Edge10 = OOC.Edge(PointG,PointH,3)
    Edge11 = OOC.Edge(PointE,PointI,1)
    Edge12 = OOC.Edge(PointF,PointJ,2)
    Edge13 = OOC.Edge(PointG,PointK,0)
    Edge14 = OOC.Edge(PointH,PointL,0)
    Edge15 = OOC.Edge(PointI,PointJ,5)
    Edge16 = OOC.Edge(PointJ,PointK,0)#test : poid = 2
    Edge17 = OOC.Edge(PointK,PointL,0)
    Edge18 = OOC.Edge(PointI,PointM,5)
    Edge19 = OOC.Edge(PointJ,PointN,3)
    Edge20 = OOC.Edge(PointK,PointO,0)
    Edge21 = OOC.Edge(PointL,PointP,4)
    Edge22 = OOC.Edge(PointM,PointN,0)
    Edge23 = OOC.Edge(PointN,PointO,1)
    Edge24 = OOC.Edge(PointO,PointP,3)




    B1.addVertice(PointA)
    B1.addVertice(PointB)
    B2.addVertice(PointC)
    B2.addVertice(PointD)
    B1.addVertice(PointE)
    B1.addVertice(PointF)
    B2.addVertice(PointG)
    B2.addVertice(PointH)
    B1.addVertice(PointI)
    B1.addVertice(PointJ)
    B2.addVertice(PointK)
    B2.addVertice(PointL)
    B1.addVertice(PointM)
    B1.addVertice(PointN)
    B2.addVertice(PointO)
    B2.addVertice(PointP)

    B1.addEdge(Edge1)
    # MGraph.addEdge(Edge2)
    cut.append(Edge2)
    B2.addEdge(Edge3)
    B1.addEdge(Edge4)
    B1.addEdge(Edge5)
    B2.addEdge(Edge6)
    B2.addEdge(Edge7)
    B1.addEdge(Edge8)
    # MGraph.addEdge(Edge9)
    cut.append(Edge9)
    B2.addEdge(Edge10)
    B1.addEdge(Edge11)
    B1.addEdge(Edge12)
    B2.addEdge(Edge13)
    B2.addEdge(Edge14)
    B1.addEdge(Edge15)
    # MGraph.addEdge(Edge16)
    cut.append(Edge16)
    B2.addEdge(Edge17)
    B1.addEdge(Edge18)
    B1.addEdge(Edge19)
    B2.addEdge(Edge20)
    B2.addEdge(Edge21)
    B1.addEdge(Edge22)
    # MGraph.addEdge(Edge23)
    cut.append(Edge23)
    B2.addEdge(Edge24)

    # for elt in MGraph.getVertices()[:int(len(MGraph.getVertices())/2)]:
    # Fminus(MGraph)
    # getMinimas(MGraph)
    # MThinning(MGraph)
    # BThinning(MGraph)
    BlocThinning(B1,B2,cut)



    # connexeComponent(MGraph)
    # B1.affiche()
    # print()
    # B2.affiche()

    connexeComponent(B1)
    connexeComponent(B2)

    BlocLabelling(B1,B2,cut)

    # for vertice in MGraph.getVertices():
        # print(vertice.getName(), " = ", vertice.getMinLab())
    # print()
    for vertice in B1.getVertices():
        print(vertice.getName(), " = ", vertice.getLabel())
    B1.affiche()
    print()
    for vertice in B2.getVertices():
        print(vertice.getName(), " = ", vertice.getLabel())
    B2.affiche()
    #print(hasEdge(MGraph,Point2,Point1))
    # MGraph.affiche()


    print("teeeeeeeeeeeeeest")
    testgraph = create_graph(3,4)
    testgraph.affiche()
    pass

if __name__ == '__main__':
    main()

# parametre : le graphe et la taille des blocs
