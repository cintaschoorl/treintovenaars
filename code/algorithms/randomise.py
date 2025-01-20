import random
from code.classes.route import Route


def randomise_route(stations_list, max_duration=120):
    spent_time = 0
    route = Route(stations_list, max_duration)

    # get a list with possible start stations
    possible_start_stations = route.get_possible_start()
    print(possible_start_stations)

    # pick random starting station
    current_station = random.choice(possible_start_stations)
    route.add_station(current_station)
    print(f"Starting route at: {current_station.name}")

    previous_station = None

    while spent_time <= max_duration:

        # get current neighbours
        neighbours = route.get_neighbours(current_station)

        # get the neighbours that are not the previous stations
        valid_neighbours = {}
        for station, time in neighbours.items():
            if station != previous_station:
                valid_neighbours[station] = time

        # get random neighbour and travel time
        next_station, next_time =  random.choice(list(valid_neighbours.items()))

        # validate if it will be longer than max duration
        if route.is_valid((spent_time + next_time)):
            # update route and time with the new connection
            route.add_station(next_station)
            previous_station = current_station
            current_station = next_station
            spent_time += next_time
            print(f"{next_station} added to route, travel time: {next_time}.\nTotal route duration: {spent_time}.")
        else:
            break

    return route.route, spent_time
