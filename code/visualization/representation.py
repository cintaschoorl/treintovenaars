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

    Input: A given name and a given x and y coördinate for each station.

    Returns: Instances for each station.
    """
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x


class Connection:
    """
    Initializing the connections with their stations

    Input: Two stations and the given travel_time between these stations.

    Returns: Instances for each connection.

    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time


def load_station_short_names(filepath):
    """
    Loading the short names from the uid.csv file

    Input: The given filepath for the file with the names of
    each station and its short name.

    Returns: The short names for each stations_path.
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
    Loading the stations from the StationsNationaal.csv file

    Input: A given filepath with the file of the stations
    with their coördinates.

    Returns: The loaded stations in a list.

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

    Input: A given filepath with all of the connections and their travel time

    Returns: A list of connections.
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

    """
    Loading the routes from the json file.

    Input: A given filepath towards the right json file.

    Returns: The routes.

    """

    with open(filepath, 'r') as file:

        data = json.load(file)

    return data["routes"]


def create_graph(stations, connections, station_names):

    """
    Creating a graph of the nodes(stations) and edges(connections)

    Input:
    -stations: Stations object of the stations and coördinates
    -connections: Connections object of the connections and travel time
    -station_names: Instance of the station with the station names.

    Returns: The initialization of the graph.

    """

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
    """
    Visualizing the whole map, using the previous create_graph function.

    Returns: a plot with an image(map of the Netherlands), given nodes(short names of the stations),
    and their connections between the stations. Each route is displayed in a different color.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = os.path.join(script_dir, "../../data/StationsNationaal.csv")
    connections_path = os.path.join(script_dir, "../../data/ConnectiesNationaal.csv")
    uid_path = os.path.join(script_dir, "../../data/uid_NL.csv")
    routes_path = os.path.join(script_dir, "../../output/best_railmap_random_heuristic.json")
    image_path = os.path.join(script_dir, "../../data/Nederland_kaart.png")

    # using the loading functions from before to get the right data
    station_names = load_station_short_names(uid_path)
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)
    routes = load_routes(routes_path)

    G, pos = create_graph(stations, connections, station_names)

    colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "brown", "pink", "cyan"])
    train_colors = {train: next(colors) for train in routes}

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    country_map = plt.imread(image_path)
    height, width, _ = country_map.shape


def update(frame, ax, G, pos, country_map, routes, station_names, train_colors):
    """
    Updating the moving map with the new added routes (which are combinations of the connections).

    Input:
    -frame: A frame that is set for the plot.
    -ax: Instances from the previous functions.
    -G: The initialized nodes and adges.
    -pos: The positions of the items inside of the plot.
    -country_map: The given image of the Netherlands.
    -routes: The given routes the plot should visualize.
    -station_names: The names of the stations.
    -train_colours: The colour for each train route.

    Returns: The updated plot.

    """
    ax.clear()
    x_min, x_max = min(pos[k][0] for k in pos), max(pos[k][0] for k in pos)
    y_min, y_max = min(pos[k][1] for k in pos), max(pos[k][1] for k in pos)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # getting the plot in the right place into the image of the Netherlands
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
    ax.set_aspect((x_max - x_min) / (y_max - y_min))
    plt.tight_layout()
