import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import json
import itertools


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


def load_routes(filepath):

    with open(filepath, 'r') as file:

        data = json.load(file)

    return data["routes"]



def create_graph(stations, connections, station_names):
    G = nx.DiGraph()
    pos = {}
    for station in stations:
        short_name = station_names.get(station.name, station.name)
        G.add_node(short_name)
        pos[short_name] = (station.x, station.y)

    for connection in connections:
        station1_short = station_names.get(connection.station1, connection.station1)
        station2_short = station_names.get(connection.station2, connection.station2)
        G.add_edge(station1_short, station2_short)

    return G, pos

def visualize_map():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = os.path.join(script_dir, "../../data/StationsNationaal.csv")
    connections_path = os.path.join(script_dir, "../../data/ConnectiesNationaal.csv")
    uid_path = os.path.join(script_dir, "../../data/uid_NL.csv")
    routes_path = os.path.join(script_dir, "../../output/best_railmap_random_heuristic.json")
    image_path = os.path.join(script_dir, "../../data/Nederland_kaart.png")

    station_names = load_station_short_names(uid_path)
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)
    routes = load_routes(routes_path)

    G, pos = create_graph(stations, connections, station_names)

    colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "brown", "pink", "cyan"])
    train_colors = {train: next(colors) for train in routes}

    fig, ax = plt.subplots(figsize=(8, 10))
    country_map = plt.imread(image_path)

def update(frame, ax, G, pos, country_map, routes, station_names, train_colors):

    ax.clear()
    x_min, x_max = min(pos[k][0] for k in pos), max(pos[k][0] for k in pos)
    y_min, y_max = min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.imshow(country_map, extent=[x_min - 0.4, x_max + 0.2, y_min - 0.2, y_max + 0.2], aspect='auto', zorder=0)

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue", edgecolors="black", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black", ax=ax)

    for train, route in routes.items():
        edges = [(station_names.get(route[i], route[i]), station_names.get(route[i + 1], route[i + 1]))
                 for i in range(min(frame, len(route) - 1))]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=train_colors[train], width=2, ax=ax)

    ax.set_title("Animated Railmap in The Netherlands", fontsize=14)
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    ax.set_aspect('auto')
    plt.tight_layout()

    #
    # def update(frame, ax, G, pos, country_map, routes, station_names, train_colors):
    #     ax.clear()
    #     x_min, x_max = min(pos[k][0] for k in pos), max(pos[k][0] for k in pos)
    #     y_min, y_max = min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)
    #
    #     ax.set_xlim(x_min, x_max)
    #     ax.set_ylim(y_min, y_max)
    #     ax.imshow(country_map, extent=[x_min - 0.4, x_max + 0.2, y_min - 0.2, y_max + 0.2], aspect='auto', zorder=0)
    #
    #     nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue", edgecolors="black", ax=ax)
    #     nx.draw_networkx_labels(G, pos, font_size=8, font_color="black", ax=ax)
    #
    #     for train, route in routes.items():
    #         edges = [(station_names.get(route[i], route[i]), station_names.get(route[i + 1], route[i + 1]))
    #                  for i in range(min(frame, len(route) - 1))]
    #         nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=train_colors[train], width=2, ax=ax)
    #
    #     ax.set_title("Animated Railmap in The Netherlands", fontsize=14)
    #     ax.set_xlabel("x coordinate")
    #     ax.set_ylabel("y coordinate")
    #     ax.set_aspect('auto')
    #     plt.tight_layout()

    # max_frames = max(len(r) for r in routes.values())
    # ani = FuncAnimation(fig, update, frames=len(G.nodes), interval=500, repeat=False)
    #
    # plt.tight_layout()
    # plt.show()


#
#
# if __name__ == "__main__":
#
#     # from the right folders, finding the right data as input for the functions
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     stations_path = os.path.join(script_dir, "../../data/StationsNationaal.csv")
#     connections_path = os.path.join(script_dir, "../../data/ConnectiesNationaal.csv")
#     uid_path = os.path.join(script_dir, "../../data/uid_NL.csv")
#     routes_path = os.path.join(script_dir, "../../output/best_railmap_random_heuristic.json")
#     image_path = os.path.join(script_dir, "../../data/Nederland_kaart.png")
#
#
#     # loading in the data from the previous csv files
#     station_names = load_station_short_names(uid_path)
#     stations = load_stations(stations_path)
#     connections = load_connections(connections_path)
#     routes = load_routes(routes_path)
#
#
#     # creating a graph
#     G = nx.DiGraph()
#
#     # creating a dictionary for the positions
#     pos = {}
#
#     # addign the stations with their shortnames in the figure
#     for station in stations:
#         short_name = station_names.get(station.name, station.name)
#         G.add_node(short_name)
#         pos[short_name] = (station.x, station.y)
#     print(f"Stations in pos: {list(pos.keys())}")
#
#
#     # adding the connections
#     for connection in connections:
#         station1_short = station_names.get(connection.station1, connection.station1)
#         station2_short = station_names.get(connection.station2, connection.station2)
#         G.add_edge(station1_short, station2_short)
#
#
#     # assigning colors to each route
#     colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "brown", "pink", "cyan"])
#     train_colors = {train: next(colors) for train in routes}
#
#
#     # visualisatie
#     fig, ax = plt.subplots(figsize=(8, 10))
#
#     #image_path = os.path.join(script_dir, "../../data/Nederland_kaart.png")
#     country_map = plt.imread(image_path)
#
#
#     def update(frame):
#         """
#         Updating function for the animation
#
#         Input:
#
#         Returns:
#         """
#         ax.clear()
#
#         x_min, x_max = min(pos[k][0] for k in pos), max(pos[k][0] for k in pos)
#         y_min, y_max = min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)
#
#         # giving the limits for the axes
#         ax.set_xlim(x_min, x_max)
#         ax.set_ylim(y_min, y_max)
#         ax.imshow(country_map, extent=[x_min - 0.4, x_max + 0.2, y_min - 0.2, y_max + 0.2], aspect='auto', zorder=0)
#
#         # drawing the stations
#         nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue", edgecolors="black", ax=ax)
#         nx.draw_networkx_labels(G, pos, font_size=8, font_color="black", ax=ax)
#
#         # drawing the routes
#         for train, route in routes.items():
#             # updating the edges using short names
#             edges = [(station_names.get(route[i], route[i]), station_names.get(route[i + 1], route[i + 1]))
#                      for i in range(min(frame, len(route) - 1))]
#
#
#             # Now draw the edges using the correct node names (short names)
#             nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=train_colors[train], width=2, ax=ax)
#
#
#         # labels and axis settings
#         ax.set_title("Animated Railmap in The Netherlands", fontsize=14)
#         ax.set_xlabel("x coördinate")
#         ax.set_ylabel("x coördinate")
#         ax.set_aspect('auto')
#         plt.tight_layout()
#
#
#     # animation set up
#     max_frames = max(len(r) for r in routes.values())
#     ani = FuncAnimation(fig, update, frames=len(G.nodes), interval=500, repeat=False)
#
#     # showing the visualization
#     plt.tight_layout()
#     plt.show()
