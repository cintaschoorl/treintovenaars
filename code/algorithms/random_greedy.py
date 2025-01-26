from code.classes.station import Station
from code.classes.railmap import Railmap
from code.classes.route import Route

import random
import os
import csv

def reset_connections(railmap):
    """
    Resets all routes and ridden connections in the railmap.
    This does not modify the Railmap class directly.
    """
    railmap.routes = {}


def greedy_route(railmap, max_duration):
    """
    Generate a single route using a greedy approach.
    Prioritize unvisited connections or the shortest travel time.
    """

    used_connections = set()

    current_station = random.choice(railmap.stations)

    route = Route(railmap.stations, max_duration)
    route.add_station(current_station)

    while True:

        unvisited_neighbors = {
            neighbor: time
            for neighbor, time in current_station.neighbours.items()
            if (current_station, neighbor) not in used_connections and (neighbor, current_station) not in used_connections}


        if not unvisited_neighbors:
            neighbors = current_station.neighbours
        else:
            neighbors = unvisited_neighbors


        if not neighbors:
            break


        next_station, travel_time = min(
            neighbors.items(), key=lambda item: item[1]
        )


        if route.travel_time + travel_time > max_duration:
            break


        route.add_station(next_station, travel_time)

        used_connections.add((current_station, next_station))
        used_connections.add((next_station, current_station))


        current_station = next_station

    return route



def random_greedy_algorithm(stations_path, uid_path, connections_path, num_routes, max_duration, iterations):
    """
    Runs the random greedy algorithm multiple times and returns the final quality score.
    """
    railmap = Railmap()
    railmap.load_stations(stations_path, uid_path, connections_path)

    for iteration in range(iterations):
        reset_connections(railmap)

        for i in range(num_routes):
            route = greedy_route(railmap, max_duration)
            route.id = f"train_{i + 1}"
            railmap.add_trajectory(route)

    quality_score = railmap.quality_K()
    return quality_score
