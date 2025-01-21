import random
from code.classes.route import Route


def randomise_route(stations_list, max_duration=120):
    spent_time = 0
    route = Route(stations_list, max_duration)

    # get a list with possible start stations (1 neighbour)
    route.get_possible_start()

    current_station = route.pick_start()
    route.add_station(current_station)
    #print(f"Starting route at: {current_station.name}")

    # set with previous stations
    previous_stations = {current_station}

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
        #next_station, next_time =  random.choice(list(valid_neighbours.items()))
        next_station, next_time =  random.choice(list(neighbours.items()))

        # validate if it will be longer than max duration
        if route.is_valid((spent_time + next_time)):
            # update route and time with the new connection
            route.add_station(next_station, next_time)
            previous_stations.add(next_station)
            current_station = next_station
            spent_time += next_time
            #print(f"{next_station} added to route, travel time: {next_time}.\nTotal route duration: {spent_time}.")
        else:
            break

    return route.route, spent_time
