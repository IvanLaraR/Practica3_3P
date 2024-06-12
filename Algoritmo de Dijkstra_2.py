# -*- coding: utf-8 -*-

"""
Created on Wed Jun  5 19:06:19 2024

@author: IvanL
"""

import heapq
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

class MapaDijkstra1:
    def __init__(self):
        self.ciudades = {}

    def agregar_ciudad(self, nombre):
        self.ciudades[nombre] = {}

    def agregar_camino(self, desde, hacia, distancia):
        self.ciudades[desde][hacia] = distancia
        self.ciudades[hacia][desde] = distancia  # Para caminos bidireccionales

    def dijkstra(self, inicio):
        distancias = {ciudad: float('infinity') for ciudad in self.ciudades}
        distancias[inicio] = 0
        pq = [(0, inicio)]
        paso_a_paso = []

        while pq:
            distancia_actual, ciudad_actual = heapq.heappop(pq)

            if distancia_actual > distancias[ciudad_actual]:
                continue

            for vecino, distancia in self.ciudades[ciudad_actual].items():
                nueva_distancia = distancia_actual + distancia

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    heapq.heappush(pq, (nueva_distancia, vecino))

            paso_a_paso.append((ciudad_actual, dict(distancias)))

        return distancias, paso_a_paso

    def graficar_pasos(self, pasos):
        G = nx.Graph()
        for ciudad, caminos in self.ciudades.items():
            for vecino, distancia in caminos.items():
                G.add_edge(ciudad, vecino, weight=distancia)

        pos = nx.spring_layout(G)

        for i, (ciudad, distancias) in enumerate(pasos):
            plt.figure(figsize=(10, 7))
            plt.title(f'Paso {i+1}: Ciudad actual {ciudad}')
            
            # Dibujar ciudades (nodos)
            node_colors = ['lightblue' if node != ciudad else 'orange' for node in G.nodes()]
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700)
            
            # Dibujar caminos (aristas)
            nx.draw_networkx_edges(G, pos)
            
            # Dibujar etiquetas de ciudades (nodos)
            nx.draw_networkx_labels(G, pos, font_size=15)
            
            # Dibujar etiquetas de caminos (aristas)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
            
            # Dibujar distancias
            dist_labels = {k: f'{v:.1f}' if v < float('infinity') else '∞' for k, v in distancias.items()}
            nx.draw_networkx_labels(G, pos, labels=dist_labels, font_color='red', font_size=12)
            
            # Resaltar la ciudad actual y sus vecinos
            vecinos = list(self.ciudades[ciudad].keys())
            nx.draw_networkx_nodes(G, pos, nodelist=[ciudad], node_color='orange', node_size=900)
            nx.draw_networkx_nodes(G, pos, nodelist=vecinos, node_color='yellow', node_size=700)
            
            plt.show()

# Ejemplo de uso
mapa = MapaDijkstra1()
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

distancias, pasos = mapa.dijkstra('Ciudad1')

# Mostrar distancias finales en una tabla
df_distancias = pd.DataFrame(list(distancias.items()), columns=['Ciudad', 'Distancia'])
print("Distancias finales desde 'Ciudad1':")
print(df_distancias.to_string(index=False))

# Mostrar pasos intermedios
print("\nPasos intermedios:")
for i, paso in enumerate(pasos):
    print(f"Paso {i+1}: {paso}")

# Graficar los pasos intermedios
mapa.graficar_pasos(pasos)

