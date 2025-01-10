# radio russia voorbeeld als Node class
class Station():
    def __init__(self, name, y, x, uid):
        """
        Represents a train station with a name and coordinates.
        Attributes are: 
        - name
        - y- and x-coordinates
        - uid: unique three-letter ID
        """
        self.name = name
        self.y = y
        self.x = x
        self.id = uid


    def __repr__(self):
        "Represent object with its ID in a list/dict"
        return self.id


# class Station_a():
#     """
#     Represents a train station with a name and coordinates.
#     Attributes are: name and y- and x-coordinate.
#     """
#     def __init__(self,  name, y, x):
#         self.name = name
#         self.y = y
#         self.x = x

#     def print(self):
#         return f'{self.name}'