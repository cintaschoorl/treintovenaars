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
    A route with the most common connection is cut at the connection,
    and the route is regenerated from the cut point.

    Input: 
        - current_railmap (Railmap): current Railmap object
        - max_duration (int): maximum duration for each route

    Returns:
        - New modified Railmap solution
    """
    # Create a copy of the current solution
    new_railmap = deepcopy(current_railmap)

    # keep track of station and connection usage
    stations_used = {station.id: 0 for station in new_railmap.stations}
    connections_used = {}

    for route in current_railmap.routes.values():
        for i, station in enumerate(route.route):
            # count occurance of station
            stations_used[station.id] += 1
            # if station is not the last, get connection with next neighbour:
            if i < (len(route.route) - 1):
                connection = tuple(sorted(station.id, route.route[i + 1].id))
                # initialize if not yet present and add occurance
                connections_used[connection] = connections_used.get(connection, 0) + 1
    
    # find most common connection
    most_common = max(connections_used, key=connections_used.get)

    # get all routes with the common connection present
    present_routes = []
    for route_id, route in new_railmap.routes.items():
        for i in range(len(route.route) - 1):
            connection = tuple(sorted((station.id, route.route[i + 1].id)))
            if connection == most_common:
                present_routes.append((route_id, i))

    # if no route contains the connection, return original railmap
    if not present_routes:
        return new_railmap

    # pick a random route and the index of the connection to cut at
    id_to_modify, cut_idx = random.choice(present_routes)
    route_to_modify = new_railmap.routes[id_to_modify]
    
    # cut the route at the connection
    new_start_station = route_to_modify.route[cut_idx]
    route_to_modify.route = route_to_modify.route[:cut_idx + 1]

    # modify travel time for cut route
    route_to_modify.travel_time = sum(
        route_to_modify.route[i].neighbours.get(route_to_modify.route[i + 1])
        for i in range(len(route_to_modify.route) - 1))

    # regenerate route from the cut point
    current_station = new_start_station
    while route_to_modify.is_valid(route_to_modify.travel_time): #and current_station:
        neighbours = current_station.neighbours
        # retrieve valid (new) neighbours to connect with
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

