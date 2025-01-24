import random
from code.classes.route import Route


def randomise_route(stations_list, max_duration=120):
    spent_time = 0
    route = Route(stations_list, max_duration)

    # get a list with possible start stations (1 neighbour)
    #route.get_possible_start()

    current_station = random.choice(route.stations)
    route.add_station(current_station)
    #print(f"Starting route at: {current_station.name}")

    # set with previous stations
    #previous_stations = {current_station}

    while spent_time <= max_duration:

        # get current neighbours
        neighbours = route.get_neighbours(current_station)

        # get the neighbours that are not in the previous stations
        #valid_neighbours = {}
        #for station, time in neighbours.items():
            #if station not in previous_stations:
                #valid_neighbours[station] = time
        #if not valid_neighbours:
            #print("No valid neighbours left. Ending Route")
            #break

        # get random neighbour and travel time
        next_station, next_time =  random.choice(list(neighbours.items()))
        #next_station, next_time =  random.choice(list(neighbours.items()))

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

# dict om de gebruiks frequentie bij te houden in de lijnvoering (dus van meerdere routes)
global_connection_usage = {}

def randomise_heuristics(stations_list, max_duration, first_route = False):
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

        # seperate remaining neighbours into new and used connections
        #new_connections = {}
        #used_connections_dict = {}

        #for station, time in valid_neighbours.items():
        #    connection = tuple(sorted([current_station.name, station.name]))
        #    if connection not in used_connections:
        #        new_connections[station] = time
        #    else:
        #        used_connections_dict[station] = time

        # choose from new connections with 85% probability if available
        #if new_connections and random.random() < 0.85:
        #    next_station, next_time = random.choice(list(new_connections.items()))
        #else:
            # fall back to any valid neighbour (new and used)
            #all_valid = {**new_connections, **used_connections_dict}
            #if not all_valid:
            #    break
            #next_station, next_time = random.choice(list(all_valid.items()))

        # get random neighbour and travel time
        #next_station, next_time =  random.choice(list(valid_neighbours.items()))
        #next_station, next_time =  random.choice(list(neighbours.items()))

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
