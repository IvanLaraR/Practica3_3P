# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:06:19 2024

@author: IvanL
"""

import heapq
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

class MapaDijkstra2:
    def __init__(self):
        self.ciudades = {}
        self.grafo = nx.Graph()

    def agregar_ciudad(self, nombre):
        self.ciudades[nombre] = {}
        self.grafo.add_node(nombre)

    def agregar_camino(self, desde, hacia, distancia):
        self.ciudades[desde][hacia] = distancia
        self.ciudades[hacia][desde] = distancia  # Para caminos bidireccionales
        self.grafo.add_edge(desde, hacia, weight=distancia)

    def dijkstra(self, inicio):
        distancias = {ciudad: float('infinity') for ciudad in self.ciudades}
        distancias[inicio] = 0
        pq = [(0, inicio)]
        prev = {ciudad: None for ciudad in self.ciudades}

        while pq:
            distancia_actual, ciudad_actual = heapq.heappop(pq)

            if distancia_actual > distancias[ciudad_actual]:
                continue

            for vecino, distancia in self.ciudades[ciudad_actual].items():
                nueva_distancia = distancia_actual + distancia

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    prev[vecino] = ciudad_actual
                    heapq.heappush(pq, (nueva_distancia, vecino))

        return distancias, prev

    def reconstruir_camino(self, prev, inicio, fin):
        camino = []
        actual = fin
        while actual is not None:
            camino.insert(0, actual)
            actual = prev[actual]
        if camino[0] == inicio:
            return camino
        else:
            return []

    def graficar_caminos(self, distancias, prev, inicio):
        pos = nx.spring_layout(self.grafo)
        plt.figure(figsize=(10, 7))

        # Dibujar el grafo completo
        nx.draw(self.grafo, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=15)
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels, font_size=12)

        for ciudad, distancia in distancias.items():
            if ciudad != inicio and distancia < float('infinity'):
                camino = self.reconstruir_camino(prev, inicio, ciudad)
                path_edges = list(zip(camino, camino[1:]))
                nx.draw_networkx_edges(self.grafo, pos, edgelist=path_edges, edge_color='orange', width=2)
                nx.draw_networkx_nodes(self.grafo, pos, nodelist=camino, node_color='orange', node_size=700)

        plt.title(f'Caminos más cortos desde {inicio}')
        plt.show()

# Ejemplo de uso
mapa = MapaDijkstra2()
mapa.agregar_ciudad('Ciudad1')
mapa.agregar_ciudad('Ciudad2')
mapa.agregar_ciudad('Ciudad3')
mapa.agregar_ciudad('Ciudad4')
mapa.agregar_ciudad('Ciudad5')

mapa.agregar_camino('Ciudad1', 'Ciudad2', 1)
mapa.agregar_camino('Ciudad1', 'Ciudad3', 4)
mapa.agregar_camino('Ciudad2', 'Ciudad3', 2)
mapa.agregar_camino('Ciudad2', 'Ciudad4', 5)
mapa.agregar_camino('Ciudad3', 'Ciudad4', 1)
mapa.agregar_camino('Ciudad4', 'Ciudad5', 3)

distancias, prev = mapa.dijkstra('Ciudad1')

# Mostrar distancias finales en una tabla
df_distancias = pd.DataFrame(list(distancias.items()), columns=['Ciudad', 'Distancia'])
print("Distancias finales desde 'Ciudad1':")
print(df_distancias.to_string(index=False))

# Graficar los caminos más cortos
mapa.graficar_caminos(distancias, prev, 'Ciudad1')

