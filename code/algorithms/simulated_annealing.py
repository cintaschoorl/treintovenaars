import random
import math
from collections import Counter
from copy import deepcopy
from code.classes.route import Route
from code.algorithms.randomise import randomise_route, randomise_heuristics

def simulated_annealing(railmap, iterations, max_duration, num_routes, initial_temp, cooling_rate=0.9, cooling_type='linear'):
    """
    Simulated Annealing algorithm to optimize the quality score K for a rail network

    Input:
        - railmap (Railmap): Railmap object containing all stations and connections
        - iterations (int): maximum number of iterations to improve the solution
        - max_duration (int): maximum duration for each route
        - num_routes (int): number of routes to generate in a solution
        - initial_temp (float): initial temperature for simulated annealing
        - cooling_type (str): 

    Returns:
        - tuple: (best Railmap object, its quality score K, list of all scores to visualize)
    """ 
     # keep track of all scores and temperatures
    all_scores = []
    all_temperatures = []

    # generate initial solution with randomise algorithm
    current_railmap = generate_initial_solution(railmap, num_routes, max_duration)
    current_score = current_railmap.quality_K()

    # create deepcopy of current railmap
    best_railmap = deepcopy(current_railmap)
    best_score = current_score

    print(f"Initial Quality Score (K): {current_score}")

    # simulated annealing loop
    for i in range(iterations):
        # Calculate temperature for iteration
        temperature = calculate_temp(cooling_type, initial_temp, cooling_rate, iterations, i)
        all_temperatures.append(temperature)

        # generate a new solution by mutating the current solution
        new_railmap = modify_solution(current_railmap)
        new_score = new_railmap.quality_K()

        # calculate acceptance probability ! met bas zn functie
        if new_score < current_score:
            acceptance_prob = 2 ** (-(current_score - new_score) / temperature)
        else:
            acceptance_prob = 1
        print(f"Acceptance probability = {acceptance_prob}")

        # accept new solution based on probability
        if new_score > current_score or random.random() < acceptance_prob:
            current_railmap = deepcopy(new_railmap)
            current_score = new_score

            # Update new best solution
            if new_score > best_score:
                best_railmap = deepcopy(new_railmap)
                best_score = new_score

        all_scores.append(current_score)

        # Debug output
        print(f"#{i + 1}: New Score = {new_score}, Current Best Score = {best_score}, Temperature = {temperature:.4f}")

    return best_railmap, best_score, all_scores, all_temperatures


def calculate_temp(cooling_type, startT, cooling_rate, iterations, i):
    """
    Calculate the new temperature for the given cooling type

    Input:
        - cooling_type (str): linear or exponential cooling function
        - startT (float): initial temperature
        - iterations (int): maximum number of iterations to improve the solution
        - i (int): current iteration

    Returns:
        - New temperature (float)

    """
    if cooling_type == "linear":
        return startT - (startT/iterations) * i
    elif cooling_type == "exponential":
        return startT * cooling_rate ** i


def generate_initial_solution(railmap, n_routes, max_duration):
    """
    Generate an initial railmap solution using the randomise algorithm.
    
    Input:
        - railmap (Railmap): Railmap object with stations and connections
        - n_routes (int): number of routes to generate
        - max_duration (int): maximum duration for each route in minutes

    Returns:
        - initial Railmap solution

    """
    # create new deepcopy of the railmap to work with and leave original unaltered
    init_railmap = deepcopy(railmap)

    for i in range(n_routes):
        # initialize new routes with random algorithm
        route_stations, total_time = randomise_route(init_railmap.stations, max_duration)

        route = Route(init_railmap.stations, max_duration)
        route.route = route_stations
        route.travel_time = total_time
        route.id = f"train_{i + 1}"

        init_railmap.add_trajectory(route)

    return init_railmap


def modify_solution(current_railmap):
    """
    Generate a new solution by modifying the current solution.
    The most common station in the railmap is tracked and cut in a route 
    where it occurs the most, and regenerated from this point. 

    Input: 
        - current_railmap (Railmap): current Railmap object

    Returns:
        - New modified Railmap solution
    """
    # Create a copy of the current solution
    new_railmap = deepcopy(current_railmap)

    # count station occurences across all routes
    station_counter = Counter()
    for route in new_railmap.routes.values():
        for station in route.route:
            station_counter[station.id] += 1

    # find most common station
    most_common = max(station_counter, key=station_counter.get)
    # print(f"Most common station: {most_common} ({station_counter[most_common]} times)")

    # find route where the station occurs the most
    route_to_modify = None
    max_occurrences = 0
    for route in new_railmap.routes.values():
        occurrences = sum(1 for station in route.route if station.id == most_common)
        if occurrences > max_occurrences:
            route_to_modify = route
            max_occurrences = occurrences

    if not route_to_modify:
        print("No route found to modify.")
        # pick random route and make random cut and regenerate???
        return new_railmap

    # cut route at the first occurrence of the most common station
    cut_idx = next(i for i, station in enumerate(route_to_modify.route) if station.id == most_common)
    # print(f"Cutting route at station {most_common} (index {cut_idx})")
    new_start_station = route_to_modify.route[cut_idx]
    route_to_modify.route = route_to_modify.route[:cut_idx + 1]

    # calculate new travel time of cut route
    route_to_modify.travel_time = sum(
        route_to_modify.route[i].neighbours.get(route_to_modify.route[i + 1])
        for i in range(len(route_to_modify.route) - 1))

    # regenerate the route from the cut point
    current_station = new_start_station
    while route_to_modify.is_valid(route_to_modify.travel_time):
        # retrieve valid neighbours to connect with
        neighbours = current_station.neighbours      
        valid_next_stations = []
        for station, time in neighbours.items():
            if route_to_modify.is_valid(route_to_modify.travel_time + time)\
            and station not in route_to_modify.route:
                valid_next_stations.append((station, time))

        if not valid_next_stations:
            break
        
        # pick random valid neighbour and continue with route
        next_station, travel_time = random.choice(valid_next_stations)
        route_to_modify.add_station(next_station, travel_time)
        current_station = next_station

    return new_railmap