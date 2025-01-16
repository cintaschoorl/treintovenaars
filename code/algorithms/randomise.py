from code.classes.route import Route

spent_time = 50
start_station = 'slo'
route = Route(stations, max_duration=120)
route.add_station(start_station)
next_station, travel_time = route.get_neighbours(start_station)
spent_time += travel_time
if route.is_valid(spent_time) == True:
    whole_route = route.add_station(next_station)
start_station = next_station
print(whole_route)
