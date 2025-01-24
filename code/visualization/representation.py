import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

class Station:
    """
    Initializing the stations with their coördinates
    """
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x

class Connection:
    """
    Initializing the connections with their stations
    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time


def load_station_short_names(filepath):
    """
    Loading the short names from the uid.csv file
    """

    station_names = {}

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            # expecting two columns
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            name, short_name = row

            # stripping extra spaces to make sure the names are in the same format
            station_names[name.strip()] = short_name.strip()


    return station_names


def load_stations(filepath):
    """
    Loading the stations from the StationsHolland.csv file
    """

    stations = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            name, y, x = row

            # filling the stations list with the name, x and y for each station
            stations.append(Station(name, float(y), float(x)))

    return stations



def load_connections(filepath):
    """
    Loading the connections with their stations and the travel time
    """
    connections = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            station1, station2, travel_time = row

            # filling the connections list
            connections.append(Connection(station1, station2, int(travel_time)))
    return connections


if __name__ == "__main__":

    # in de juiste mappen de juiste data vinden als input voor de functies die deze inladen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = os.path.join(script_dir, "../../data/StationsHolland.csv")
    connections_path = os.path.join(script_dir, "../../data/ConnectiesHolland.csv")
    uid_path = os.path.join(script_dir, "../../data/uid.csv")

    # de data inladen vanuit de voorgaande csv files
    station_names = load_station_short_names(uid_path)
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)

    # een graph aanmaken
    G = nx.DiGraph()

    # een dictionary aanmaken voor de posities
    pos = {}

    # de stations toevoegen met de afkortingen in de figuur
    for station in stations:
        short_name = station_names.get(station.name, station.name)
        G.add_node(short_name)
        pos[short_name] = (station.x, station.y)


    # verbindingen toevoegen
    for connection in connections:
        station1_short = station_names.get(connection.station1, connection.station1)
        station2_short = station_names.get(connection.station2, connection.station2)
        G.add_edge(station1_short, station2_short)


    # visualisatie
    fig, ax = plt.subplots(figsize=(8, 10))

    image_path = os.path.join(script_dir, "../../data/Nederland_kaart.png")
    country_map = plt.imread(image_path)

    ax.imshow(country_map, extent=[min(pos[k][0] for k in pos), max(pos[k][0] for k in pos),
                                   min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)],
              aspect='auto', zorder=0)

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue", edgecolors="black", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black", ax=ax)


    def update(frame):
        

        # de titels en de assen definiëren
        ax.set_title("Stations and connections with their coordinates", fontsize=16)
        ax.set_xlabel("x - coordinate")
        ax.set_ylabel("y - coordinate")
        ax.axis("equal")

        ax.imshow(country_map, extent=[min(pos[k][0] for k in pos), max(pos[k][0] for k in pos),
                                       min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)],
                 aspect='auto', zorder=0)


        stations_to_draw = list(G.nodes)[:frame + 1]

        edges_to_draw = [(u, v) for u, v in G.edges if u in stations_to_draw and v in stations_to_draw]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color="gray", arrows=False)

        nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)


    ani = FuncAnimation(fig, update, frames=len(G.nodes), interval=500, repeat=False)

    plt.tight_layout()
    plt.show()



    #
    # nx.draw_networkx_nodes(
    #     G,
    #     pos,
    #     node_size=300,
    #     node_color="lightblue",
    #     edgecolors="black",
    # )
    # nx.draw_networkx_labels(G, pos, font_size=4, font_color="black")
    # nx.draw_networkx_edges(
    #     G,
    #     pos,
    #     edge_color="gray",
    #     arrows = False
    # )
    #
    # # Toon gewichten op randen
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    #
    # # Titel en assen
    # ax.set_title("Stations en verbindingen met geografische coördinaten", fontsize=16)
    # plt.axis("equal")
    # plt.xlabel("Longitude (x)")
    # plt.ylabel("Latitude (y)")
    # plt.tight_layout()
    # plt.show()
