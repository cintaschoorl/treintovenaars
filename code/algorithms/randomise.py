import random
from code.classes.route import Route


def randomise_route(stations_list, max_duration=120):
    spent_time = 0
    route = Route(stations_list, max_duration)

    # pick random starting station
    current_station = random.choice(route.stations)
    route.add_station(current_station)
    print(f"Starting route at: {current_station.name}")

    while spent_time <= max_duration:
        # get current neighbours        
        neighbours = route.get_neighbours(current_station)

        # get random neighbour and travel time
        next_station, next_time =  random.choice(list(neighbours.items()))

        # validate if it will be longer than max duration
        if route.is_valid((spent_time + next_time)):
            # update route and time with the new connection
            whole_route = route.add_station(next_station)
            current_station = next_station
            spent_time += next_time
            print(f"{next_station} added to route, travel time: {next_time}.\nTotal route duration: {spent_time}.")
        else:
            break
    
    return whole_route, spent_time