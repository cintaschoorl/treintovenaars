
class Connection():
    """
    Represents a connection between two train stations with a travel time.
    Attributes are: names and travel time.
    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time

    def __repr__(self):
        """
        Represent with station ids, e.g:
            'asc_slo' =  Amsterdam Centraal - Amsterdam Sloterdijk
        """
        return f"{repr(self.station1)}_{repr(self.station2)}"
    