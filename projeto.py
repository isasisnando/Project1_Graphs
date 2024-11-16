import networkx as nx
from scipy.io import mmread
import matplotlib.pyplot as plt
import matplotlib

#Criando grafo a partir das informações dadas no arquivo
file = mmread('soc-dolphins.mtx')
graph = nx.Graph(file)
edges = graph.edges()
n = len(graph.nodes())
# print(n)
grafo = [[] for x in range(n)]
for edge in edges:
    node1 = edge[0]
    node2 = edge[1]
    grafo[node1].append(node2)
    grafo[node2].append(node1)

R = []
X = []
P = list(nx.nodes(graph))
colors = list((matplotlib.colors.CSS4_COLORS).keys())
colors.remove('black')

    
#Exercício 1
#Para cada vértice no grafo a função printa o número do vértice e a quantidade de vizinhos
def print_vertices_e_graus():  
    global grafo
    for i in range(len(grafo)):
        node = i
        grau = len(grafo[i])
        print("Nó:", node, " Grau:", grau)

#Exercício 2
#Função realiza o algoritmo de Bron-Kerbosch para encontrar os cliques maximais e vai adicionando-os na lista de cliques maximais
maximais = []
def cliques_maximais(R,P,X, grafo):
    global maximais
    # print(R,P,X)
    if not P and not X:
        if len(R) >= 2:
            maximais.append(R)
        return
    
    copia = P[::]
    for v in copia:
        aux_r = R[::]
        aux_p = P[::]
        aux_x = X[::]
        aux_r.append(v)
        for y in aux_p[::]:
            if y not in grafo[v]:
                aux_p.remove(y)
        for y in aux_x[::]:
            if y not in grafo[v]:
                aux_x.remove(y)
        cliques_maximais(aux_r,aux_p, aux_x, grafo)
        try:
            P.remove(v)
        except:
            print(P, "v:", v)
        X.append(v)

#Exercício 3
#Para cada vértice se calcula o coeficiente de aglomeração com base nas adjacências existentes
# entre seus vizinhos e todas as possíves
def coeficientes_vertices(grafo):
    C = []
    for vertice in range(len(grafo)):
        t = 0
        for viz in grafo[vertice]:
            for viz2 in grafo[viz]:
                if viz2 in grafo[vertice]:
                    t+=1
        
        t /= 2
        n = len(grafo[vertice])
        if n > 1:
            ans = (2*t)/(n*(n-1))
        else:
            ans = 0
        C.append(ans)
    return C
#Exercício 4
# Calcula a média de todos os coeficientes 
def coeficiente_medio(n, coeficientes):
    ans = 0
    for c in coeficientes:
        ans += c 
    ans = ans/n
    return ans

#Exercício 5
#A partir da biblioteca networkx , desenha-se o grafo com os vértices coloridos
# correspondendo a cada clique maximal
def vizualize():
    i = 0
    global n
    global graph
    cores = [-1] * (n+1)
    for vertices in maximais:
        for v in vertices:
            if cores[v+1] == -1:
                cores[v+1] = colors[i]
        i+=1
    for v in range(n):
        if cores[v+1] == -1:
            cores[v+1] = colors[i]
        i += 1
    pos = nx.spring_layout(graph, k = 1)
    nx.draw(graph,pos, with_labels = True, node_color = cores[1:], edge_color = 'grey')             
    
print_vertices_e_graus()
cliques_maximais(R, P, X, grafo)
print(maximais)
C = coeficientes_vertices(grafo)
C_medio = coeficiente_medio(n,C)

vizualize()

plt.axis("on")
plt.gca().set_facecolor('black')
plt.show()