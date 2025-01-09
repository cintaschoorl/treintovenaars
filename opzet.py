
class Station():
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x

class Connection():
    def __init__(self, name, station1, station2, travel_time):
        self.name = name
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time

# open and load csv with station1, station2, time

class Trajectory():
    def __init__(self, connections, max_duration: int):
        self.max_duration = max_duration
        self.connections = []

# hoihoihoihoihoi test test
print('hi')

    


