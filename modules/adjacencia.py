from itertools import product
from collections import defaultdict
import numpy as np
import random

class AdjacencyList(object):
    def __init__(self, size):
        self._data = defaultdict(list)
        self.size = size
        self.Time = 0

    def conectar(self, nodo_origem, nodo_destino):
        self._data[nodo_origem].append(nodo_destino)

    def remover(self, nodo_origem, nodo_destino):
        self._data[nodo_origem].remove(nodo_destino)

    def DFSUtil(self,v,visited):
        visited[v]= True
        print(chr(v + 65))
        for i in self._data[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited)

    def fillOrder(self,v,visited, stack):
        visited[v]= True
        for i in self._data[v]:
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        stack = stack.append(v)

    def getTranspose(self):
        g = AdjacencyList(self.size)
        for i in self._data:
            for j in self._data[i]:
                g.conectar(j,i)
        return g

    def printSCCs(self):
        stack = []
        visited =[False]*(self.size)
        for i in range(self.size):
            if visited[i]==False:
                self.fillOrder(i, visited, stack)
        gr = self.getTranspose()
        visited =[False]*(self.size)
        while stack:
            i = stack.pop()
            if visited[i]==False:
                gr.DFSUtil(i, visited)
                print("")

    def vizinhos(self, nodo):
        return self._data[nodo]
  
    def isBCUtil(self,u, visited, parent, low, disc):
        children = 0

        visited[u] = True
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        for v in self._data[u]:
            if visited[v] == False:
                parent[v] = u
                children += 1

                if self.isBCUtil(v, visited, parent, low, disc):
                    return True

                low[u] = min(low[u], low[v])

                if parent[u] != -1 and low[v] >= disc[u]:
                    return True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
        return False

    def isBC(self):
        visited = [False] * (self.size)
        disc = [float("Inf")] * (self.size)
        low = [float("Inf")] * (self.size)
        parent = [-1] * (self.size)

        if self.isBCUtil(0, visited, parent, low, disc):
            return False

        if any(i == False for i in visited):
            return False

        return True



    def isReachable(self, s, d):
        visited =[False]*(self.size)


        queue=[]
  

        queue.append(s)
        visited[s] = True
  
        while queue:
 

            n = queue.pop(0)
             

            if n == d:
                return True
 
            for i in self._data[n]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True

        return False  

    def verificar_ciclos(self, nodo_inicial):
        nodos_visitados = set()
        nodos_restantes = [nodo_inicial]
        while nodos_restantes:
            nodo_atual = nodos_restantes.pop()
            nodos_visitados.add(nodo_atual)
            for vizinho in self.vizinhos(nodo_atual):
                if vizinho in nodos_visitados:
                    return True
                nodos_restantes.append(vizinho)
        return False

    def RF012(self,graph): # gera uma árvore geradora mínima (incompleto)
        AGM = AdjacencyList(graph["size"])
        weights = []
        for i in graph["edges"]:
            weights.append(i["weight"])

        counter = 0

        while True:
            if graph["weigthed"] == True:
                value = max(weights)
                for i in graph["edges"]:
                    if i["weight"] == value:
                        AGM.conectar(i["start"],i["end"])
                        weights.remove(value)
                        # testar se criou ciclo
                        # if teste_ciclo == True:
                        #AGM.remover(i["start"],i["end"])
            else:
                edge = graph["edges"][counter]
                AGM.conectar(edge["start"],edge["end"])
                counter +=1
                # testar se criou ciclo
                # if teste_ciclo == True:
                    #AGM.remover(edge["start"],edge["end"])

        # testar se AGM é conexo
        # if teste_conexo == True:
            # return AGM