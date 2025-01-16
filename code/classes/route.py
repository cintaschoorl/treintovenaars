import random

class Route():
    "Create a train trajectory within a given timeframe"
    def __init__(self, stations: dict, max_duration: int):
        """
        Neighbours is een dict die per station de omliggende buren
        en reistijd bevat.
        """
        self.stations = stations
        self.max_duration = max_duration
        self.traject = []

    def random_route(self):
        """
        Genereert random route vanaf een random startstation als een lijst met IUDs.
        """
        # mogelijke startstations met 1 buuurman
        possible_start_stations = [
            station for station, values in self.stations.items()
            if len(values.get("neighbours", {})) == 1
        ]

        # selecteer random uit de start stations
        start_station = random.choice(possible_start_stations)
        self.traject.append(start_station)
        self.duration = 0

        # houd bij welke stations je al hebt bezocht
        visited = {start_station}
        current_station = start_station

        while self.duration < self.max_duration:
            # zo krijg je de buren van het huidige station
            neighbour_station = self.stations[current_station].get('neighbours', {})

            unvisited = {}

            for station, travel_time in neighbour_station.items():
                if station not in visited:
                    unvisited[station] = travel_time

            # stop de loop als er geen buren meer over zijn
            if not unvisited:
                break

            # kies random volgende station
            next_station, travel_time = random.choice(list(unvisited.items()))

            if self.duration + travel_time > self.max_duration:
                break

            self.traject.append(next_station)
            self.duration += travel_time
            visited.add(next_station)
            current_station = next_station

        return self.traject








    # def add_name(self, train_name):
    #     self.id = train_name

#    def add_connection(self, station1, station2):
#        """
#        Voegt connecties aan traject toe.
#        """
#        for c in self.connection_list:
#            # search right connection
#            if c.station1 == station1 and c.station2 == station2:
                # check if within timeframe
#                if (self.duration + c.travel_time) < self.max_duration:
#                    if self.traject == []:

#                    self.traject.append(c.station1)
#                        self.traject.append(c.station2)
#                    else:
                        # add only the second
#                        self.traject.append(c.station2)

#                    self.duration += c.travel_time
#                    print(f"Connection {station1} - {station2} added: total duration is {self.duration} min.")

#                else:
#                    print(f"Max duration of {self.max_duration} min exceeded.")
