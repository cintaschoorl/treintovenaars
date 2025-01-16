
class Station():
    def __init__(self, name, y, x, uid):
        """
        Represents a train station with a name and coordinates.
        Attributes are: 
        - name
        - y- and x-coordinates
        - id: unique 3-letter ID
        - neighbours: dictionary containing neighbouring stations and their travel times
        """
        self.name = name
        self.coordinates = (x, y)
        self.id = uid
        self.neighbours = {}

    def add_neighbour(self, neighbour, travel_time):
        # check for presence
        if neighbour in self.neighbours:
            print(f"{neighbour} already present.")
            return
        # otherwise add to dict
        self.neighbours[neighbour] = travel_time    

    def __repr__(self):
        "Represent object with its ID in a list/dict"
        return self.id

