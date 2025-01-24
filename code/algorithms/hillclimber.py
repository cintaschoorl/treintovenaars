import random
from copy import deepcopy
from code.classes.route import Route
from code.algorithms.randomise import randomise_route

def hill_climber(railmap, iterations, max_duration, num_routes):
    """
    Hill Climber algorithm to optimize the quality score K for a rail network

    Input:
        - railmap (Railmap): Railmap object containing all stations and connections
        - iterations (int): maximum number of iterations to improve the solution
        - max_duration (int): maximum duration for each route
        - num_routes (int): number of routes to generate in a solution

    Returns:
        - tuple: (best Railmap object, its quality score K, list of scores to visualize)
    """ 
    # keep track of all scores
    all_scores = []

    # generate initial solution with randomise algorithm
    current_railmap = generate_initial_solution(railmap, num_routes, max_duration)
    current_score = current_railmap.quality_K()

    # create deepcopy of current railmap
    best_railmap = deepcopy(current_railmap)
    best_score = current_score

    print(f"Initial Quality Score (K): {current_score}")

    # iteratively improve solution
    for i in range(iterations):
        # Generate a new solution by mutating the current solution
        new_railmap = modify_solution(current_railmap)
        new_score = new_railmap.quality_K()

        # accept new solution if score is improved
        if new_score > current_score:
            current_railmap = deepcopy(new_railmap)
            current_score = new_score

            # update new best solution
            if new_score > best_score:
                best_railmap = deepcopy(new_railmap)
                best_score = new_score

        all_scores.append(current_score)

        # Debug output 
        # print(f"Iteration {i + 1}: Current Score = {current_score}, Best Score = {best_score}")

    return best_railmap, best_score, all_scores


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
    This simplified version allows adding or removing a station in a route.

    Input: 
        - current_railmap (Railmap): current Railmap object
        - max_duration (int): maximum duration for each route

    Returns:
        - New modified Railmap solution
    """
    # Create a copy of the current solution
    new_railmap = deepcopy(current_railmap)

    # Select a random route to modify
    route_id = random.choice(list(new_railmap.routes.keys()))
    route_to_change = new_railmap.routes[route_id]

    # select random station modification: add or remove a station
    modification = random.choice(["add", "remove"])
    if modification == "add":
        # Add a neighboring station if possible
        if route_to_change.route:
            current_station = random.choice(route_to_change.route)
            neighbours = current_station.neighbours
            if neighbours:
                new_station, travel_time = random.choice(list(neighbours.items()))
                if route_to_change.is_valid(route_to_change.travel_time + travel_time):
                    route_to_change.add_station(new_station, travel_time)
    elif modification == "remove":
        # remove a station from the route if there is more than one station
        if len(route_to_change.route) > 1:
            station_to_remove = random.choice(route_to_change.route)
            route_to_change.route.remove(station_to_remove)

    return new_railmap


## presentation notes to implement / change:
#
#
#
#