# oude versie: 
class Station_a():
    """
    Represents a train station with a name and coordinates.
    Attributes are: name and y- and x-coordinate.
    """
    def __init__(self,  name, y, x):
        self.name = name
        self.y = y
        self.x = x


# nieuwe versie:
# radio russia voorbeeld als Node class, nog niet overeen met 
# connection class, misschien is deze dus overbodig later door 
# de add_neighbour method

# class Station():
#     def __init__(self, name, y, x, uid):
#         """
#         Represents a train station with a name and coordinates.
#         Attributes are: 
#         - name
#         - y- and x-coordinates
#         - id: unique ID
#         """
#         self.name = name
#         self.y = y
#         self.x = x
#         self.id = uid
#         self.neighbours = {}

#     def add_neighbours(self, station):
#         "Add neigbouring stations to make connection"
#         self.neighbours[station.id] = station

#     def __repr__(self):
#         "Represent object with its ID in a list/dict"
#         return self.id

