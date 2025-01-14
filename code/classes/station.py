
class Station():
    def __init__(self, name, y, x, uid):
        """
        Represents a train station with a name and coordinates.
        Attributes are: 
        - name
        - y- and x-coordinates
        - id: unique ID
        """
        self.name = name
        self.y = y
        self.x = x
        self.id = uid

    def __repr__(self):
        "Represent object with its ID in a list/dict"
        return self.id

