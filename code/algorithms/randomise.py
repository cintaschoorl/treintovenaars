import random
from code.classes.route import Route
import csv
from code.classes.railmap import Railmap


def randomise_route(stations_list, max_duration=120):
    """
    Generate one random route through the railmap.

    Input:
        - stations_list (list): List of Station objects
        - max_duration (int): maximum duration for the route in minutes

    Returns:
        - list of stations in route, total time spent
    """
    spent_time = 0
    route = Route(stations_list, max_duration)

    current_station = random.choice(route.stations)
    route.add_station(current_station)

    while spent_time <= max_duration:
        # get current neighbours
        neighbours = route.get_neighbours(current_station)

        # get random neighbour and travel time
        next_station, next_time =  random.choice(list(neighbours.items()))

        # validate if it will be longer than max duration
        if route.is_valid((spent_time + next_time)):
            # update route and time with the new connection
            route.add_station(next_station, next_time)
            #previous_stations.add(next_station)
            current_station = next_station
            spent_time += next_time
            #print(f"{next_station} added to route, travel time: {next_time}.\nTotal route duration: {spent_time}.")
        else:
            break

    return route.route, spent_time

def run_randomise_route(stations_path, uid_path, connections_path, output_file, iterations=10000, num_routes=7, max_duration=120):
    """
    Run the random algorithm multiple times and save results to CSV.

    Input:
        - stations_path (str): Path to stations CSV file
        - uid_path (str): Path to UID CSV file
        - connections_path (str): Path to connections CSV file
        - output_file (str): Path to output CSV file
        - iterations (int): Number of iterations to run
        - num_routes (int): Number of routes to generate
        - max_duration (int): Maximum duration for each route in minutes

    Returns:
        - None, the results are saved to specified output file
    """
    # Create CSV header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['quality_score'])

    # Run random algorithm multiple times
    for iteration in range(iterations):
        railsystem = Railmap()
        railsystem.load_stations(stations_path, uid_path, connections_path)

        number_routes = num_routes
        max_duration = max_duration

        for i in range(number_routes):
            route_stations, total_time = randomise_route(railsystem.stations, max_duration)

            route = Route(railsystem.stations, max_duration)
            route.route = route_stations
            route.travel_time = total_time
            route.id = f"train_{i + 1}"

            railsystem.add_trajectory(route)

        K = railsystem.quality_K()

        # Write result to CSV
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([K])

    print(f"\nRandom results have been saved to {output_file}")

# dict om de gebruiks frequentie bij te houden in de lijnvoering (dus van meerdere routes)
global_connection_usage = {}

def randomise_heuristics(stations_list, max_duration, first_route = False):
    """
    Generate one route through the railmap using heuristic-based randomization.

    Input:
        - stations_list (list): List of Station objects
        - max_duration (int): Maximum duration for the route in minutes
        - first_route (bool): Indicates if this is the first route in a new line system

    Returns:
        list of stations in route, total time spent
    """
    if first_route:
        global_connection_usage.clear()

    spent_time = 0
    route = Route(stations_list, max_duration)

    # track used connections as a tuple (station1, station2)
    used_connections = set()

    # get a list with possible start stations (1 neighbour)
    route.get_possible_start()
    current_station = route.pick_start()
    route.add_station(current_station)

    # keep track of the previous station to not 'pendelen'
    previous_station = current_station

    while spent_time <= max_duration:

        # get current neighbours
        neighbours = route.get_neighbours(current_station)

        # get the neighbours that are not the previous station
        valid_neighbours = {}
        for station, time in neighbours.items():
            if station != previous_station:
                valid_neighbours[station] = time
        if not valid_neighbours:
            break

        # Score neighbours based on global connection usage
        neighbour_scores = {}
        for station, time in valid_neighbours.items():
            connection = tuple(sorted([current_station.name, station.name]))
            usage_count = global_connection_usage.get(connection, 0)
            # Lagere score = betere keuze
            neighbour_scores[station] = usage_count

        # Sorteer buren op basis van globale gebruiksfrequentie (minst gebruikt eerst)
        sorted_neighbours = sorted(
            valid_neighbours.items(),
            key=lambda x: neighbour_scores[x[0]]
        )

        # 85% kans om de minst gebruikte verbinding te kiezen
        if sorted_neighbours and random.random() < 0.85:
            next_station, next_time = sorted_neighbours[0]
        else:
            next_station, next_time = random.choice(sorted_neighbours)

            # validate if it will be longer than max duration
        if route.is_valid((spent_time + next_time)):
            route.add_station(next_station, next_time)

            # update used_connections
            connection = tuple(sorted([current_station.name, next_station.name]))
            global_connection_usage[connection] = global_connection_usage.get(connection, 0) + 1

            previous_station = current_station
            current_station = next_station
            spent_time += next_time
            #print(f"{next_station} added to route, travel time: {next_time}.\nTotal route duration: {spent_time}.")
        else:
            break

    return route.route, spent_time


def run_randomise_heuristics(stations_path, uid_path, connections_path, output_file, iterations=10000, num_routes=7, max_duration=120):
    """
    Run the heuristic-based random algorithm multiple times and save results to CSV.

    Input:
        - stations_path (str): Path to stations CSV file
        - uid_path (str): Path to UID CSV file
        - connections_path (str): Path to connections CSV file
        - output_file (str): Path to output CSV file
        - iterations (int): Number of iterations to run
        - num_routes (int): Number of routes to generate
        - max_duration (int): Maximum duration for each route in minutes

    Returns:
        - None, the results are saved to specified output file
    """
    # Create CSV header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['quality_score'])

    # Run random algorithm with heuristics multiple times
    for iteration in range(iterations):
        railsystem = Railmap()
        railsystem.load_stations(stations_path, uid_path, connections_path)

        number_routes = num_routes
        max_duration = max_duration

        for i in range(number_routes):
            # Indicate if this is the first route of a new line system
            first_route = (i == 0)

            route_stations, total_time = randomise_heuristics(
                railsystem.stations,
                max_duration,
                first_route
            )

            route = Route(railsystem.stations, max_duration)
            route.route = route_stations
            route.travel_time = total_time
            route.id = f"train_{i + 1}"

            railsystem.add_trajectory(route)

        K = railsystem.quality_K()

        # Write result to CSV
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([K])

    print(f"\nRandom with heuristics results have been saved to {output_file}")
