from code.classes.station import Station
from code.classes.railmap import Railmap
from code.classes.route import Route

import random
import os
import csv


used_connections = set()


def reset_connections(railmap):
    """
    Resetting all of the routes and ridden connections in the railmap, without
    modifying the Railmap class itself.
    """
    global used_connections
    used_connections.clear()


def greedy_route(railmap, max_duration):
    """
    Generate a route using a greedy approach, prioritizing unvisited connections or the shortest travel time.
    """

    global used_connections

    starting_stations = [station for station in railmap.stations if len(station.neighbours) == 1]

    if starting_stations:
        current_station = random.choice(starting_stations)
    else:
        current_station = random.choice(railmap.stations)


    route = Route(railmap.stations, max_duration)
    route.add_station(current_station)

    while True:

        unvisited_neighbors = {
            neighbor: time
            for neighbor, time in current_station.neighbours.items()
            if (current_station, neighbor) not in used_connections and (neighbor, current_station) not in used_connections
        }

        if not unvisited_neighbors:
            neighbors = current_station.neighbours
        else:
            neighbors = unvisited_neighbors

        if not neighbors:
            break

        next_station, travel_time = min(neighbors.items(), key=lambda item: item[1])

        if route.travel_time + travel_time > max_duration:
            break

        route.add_station(next_station, travel_time)

        used_connections.add((current_station, next_station))
        used_connections.add((next_station, current_station))

        current_station = next_station

    return route



    #
    # used_connections = set()
    # current_station = random.choice(railmap.stations)
    #
    # route = Route(railmap.stations, max_duration)
    # route.add_station(current_station)
    #
    # while True:
    #     unvisited_neighbors = {
    #         neighbor: time
    #         for neighbor, time in current_station.neighbours.items()
    #         if (current_station, neighbor) not in used_connections and (neighbor, current_station) not in used_connections}
    #
    #     if not unvisited_neighbors:
    #         neighbors = current_station.neighbours
    #     else:
    #         neighbors = unvisited_neighbors
    #
    #     if not neighbors:
    #         break
    #
    #     next_station, travel_time = min(neighbors.items(), key=lambda item: item[1])
    #
    #     if route.travel_time + travel_time > max_duration:
    #         break
    #
    #     route.add_station(next_station, travel_time)
    #
    #     used_connections.add((current_station, next_station))
    #     used_connections.add((next_station, current_station))
    #
    #     current_station = next_station
    #
    #
    # return route

def random_greedy_algorithm(stations_path, uid_path, connections_path, num_routes, max_duration, iterations, output_csv):
    """
    Running the random greedy algorithm multiple times and writing the quality score at each iteration.
    """
    railmap = Railmap()
    railmap.load_stations(stations_path, uid_path, connections_path)


    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Writing down the score for each iteration
        for iteration in range(iterations):
            reset_connections(railmap)

            # Resetting the railmap for each iteration and running the routes
            for i in range(num_routes):
                route = greedy_route(railmap, max_duration)
                route.id = f"train_{i + 1}"
                railmap.add_trajectory(route)

            # Calculating the quality score
            quality_score = railmap.quality_K()

            # Writing into the CSV file
            writer.writerow([iteration + 1, quality_score])

    return railmap.quality_K()  # Return final quality score




    quality_score = railmap.quality_K()
    return quality_score
