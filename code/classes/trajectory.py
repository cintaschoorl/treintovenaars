class Trajectory():
    "Create a train trajectory within a given timeframe"
    def __init__(self, connection_list, max_duration: int):
        self.connection_list = connection_list
        self.max_duration = max_duration

        self.duration = 0
        self.traject = []


    def add_name(self, train_name):
        self.id = train_name

    def add_connection(self, station1, station2):
        """
        Voegt connecties aan traject toe.
        Nog automatizeren met algoritme? nu handmatig
        """
        for c in self.connection_list:
            # search right connection
            if c.station1 == station1 and c.station2 == station2:
                # check if within timeframe
                if (self.duration + c.travel_time) < self.max_duration:     
                    # add both 1 and 2 if list is empty     
                    if self.traject == []:

                        self.traject.append(c.station1)
                        self.traject.append(c.station2)
                    else:
                        # add only the second
                        self.traject.append(c.station2)

                    self.duration += c.travel_time
                    print(f"Connection {station1} - {station2} added: total duration is {self.duration} min.")

                else:
                    print(f"Max duration of {self.max_duration} min exceeded.")
