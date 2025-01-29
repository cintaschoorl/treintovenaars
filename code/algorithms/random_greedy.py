from code.classes.station import Station
from code.classes.railmap import Railmap
from code.classes.route import Route

import random
import os
import csv


# using this global set
used_connections = set()


def reset_connections(railmap):
    """
    Resetting all of the routes and ridden connections in the railmap, without
    modifying the Railmap class itself.

    Input:
        -railmap (Railmap): Railmap object with stations and connections

    Returns:
        -Resetted global variable used_connections when called
    """
    global used_connections
    used_connections.clear()



def greedy_route(railmap, max_duration):
    """
    Generating a route using a greedy approach, prioritizing unvisited connections or the shortest travel time.

    Input:
        -railmap (Railmap): Railmap object with stations and connections
        -max_duration: integer which is given in the main, that determines the
         maximum amount of minutes the trains can ride their routes

    Returns:
        -Initialization for the greedy routes
    """

    global used_connections

    starting_stations = [station for station in railmap.stations if len(station.neighbours) == 1]

    # using the stations with only 1 neighbour as starting station
    if starting_stations:
        current_station = random.choice(starting_stations)

    # if there is not such a station, then pick a random starting station
    else:
        current_station = random.choice(railmap.stations)


    route = Route(railmap.stations, max_duration)
    route.add_station(current_station)


    # prioritizing unvisited connections
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


        # prioritizing the shortest amount of travel time
        if route.travel_time + travel_time > max_duration:
            break

        route.add_station(next_station, travel_time)

        used_connections.add((current_station, next_station))
        used_connections.add((next_station, current_station))

        current_station = next_station


    return route




def random_greedy_algorithm(stations_path, uid_path, connections_path, num_routes, max_duration, iterations, output_csv):
    """
    Running the random greedy algorithm and writing the quality score at each iteration.

    Input:
        -stations_path: a string which will define the path towards the right the stations csv file
        -uid_path: a string which will define the path towards the right csv file with the short names
        -connections_path: a string which will define the path towards the right file with the connections csv file
        -num_routes: an integer that defines the maximum amount of routes that can be possibly ridden
        -max_duration: integer which is given in the main, that determines the
         maximum amount of minutes the trains can ride their routes
        -iterations: an integer that defines the number of times the algorithm will run
        -output_csv: a string which will define the path towards the right output file

    Returns:
        -A csv file with the values for K for each run
    """

    best_score = 0
    best_routes = None
    all_scores = []

    railmap = Railmap()
    railmap.load_stations(stations_path, uid_path, connections_path)


    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['iteration', 'quality_score'])

        for iteration in range(iterations):


            # resetting the railmap for each iteration and running the routes
            reset_connections(railmap)

            for i in range(num_routes):
                route = greedy_route(railmap, max_duration)
                route.id = f"train_{i + 1}"
                railmap.add_trajectory(route)

            # calculating the quality score K
            quality_score = railmap.quality_K()

            # writing the values into a CSV fil
            writer.writerow([iteration + 1, quality_score])

            # updating the best score and routes if better
            if quality_score > best_score:
                best_score = quality_score
                best_routes = railmap.routes.copy()

            all_scores.append(quality_score)


    # formatting the best_routes to include stations and connections
    formatted_routes = {}

    for route_id, route in best_routes.items():
        station_names = [station.name for station in route.route]
        formatted_routes[route_id] = station_names


    return best_score, best_routes, all_scores
