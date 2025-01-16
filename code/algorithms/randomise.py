from code.classes.route import Route



def randomise_route(stations_list, max_duration=120):
    spent_time = 0
    route = Route(stations_list, max_duration)

    for i in range(20):
        current_station = random.choice(route.stations)
        route.add_station(current_station)
        neighbours = route.get_neighbours(current_station)
        next_station =  random.choice(neighbours)


        spent_time += next_station.values()
        print(f"time is now {spent_time}")
        if route.is_valid(spent_time):
            whole_route = route.add_station(next_station)
            current_station = next_station.keys()
        print(whole_route)




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


            if self.duration + travel_time > self.max_duration:
                break

            self.traject.append(next_station)
            self.duration += travel_time
            visited.add(next_station)
            current_station = next_station

        return self.traject
