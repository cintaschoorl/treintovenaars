import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

class Station:
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x

class Connection:
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time


def load_stations(filepath):
    stations = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name, y, x = row
            stations.append(Station(name, float(y), float(x)))
    return stations


def load_connections(filepath):
    connections = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            station1, station2, travel_time = row
            connections.append(Connection(station1, station2, int(travel_time)))
    return connections


if __name__ == "__main__":
    # dynamic input paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = os.path.join(script_dir, "../../data/StationsHolland.csv")
    connections_path = os.path.join(script_dir, "../../data/ConnectiesHolland.csv")
    
    # load the data from the paths
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)

    # Directed graph maken
    G = nx.DiGraph()

    # Voeg stations als knopen toe met coördinaten
    pos = {}

    for station in stations:
        G.add_node(station.name)
        pos[station.name] = (station.x, station.y)


    # Voeg verbindingen toe
    for connection in connections:
        G.add_edge(connection.station1, connection.station2)

    # Visualisatie
    fig, ax = plt.subplots(figsize=(12, 12))
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=300,
        node_color="lightblue",
        edgecolors="black",
    )
    nx.draw_networkx_labels(G, pos, font_size=4, font_color="black")
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="gray",
        arrows = False
    )

    # Toon gewichten op randen
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    # Titel en assen
    ax.set_title("Stations en verbindingen met geografische coördinaten", fontsize=16)
    plt.axis("equal")
    plt.xlabel("Longitude (x)")
    plt.ylabel("Latitude (y)")
    plt.tight_layout()
    plt.show()
