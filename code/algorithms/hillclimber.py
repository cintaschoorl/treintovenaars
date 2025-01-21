import random 
from code.classes.route import Route
from code.classes.railmap import Railmap


def quality_function(railmap):
    return railmap.quality_K() 

    
def generate_route():

    route = Route(stations_list, max_duration)

    # get a list with possible start stations (1 neighbour)
    possible_start_stations = route.get_possible_start()



def create_railmap():
    pass 



def hill_climber():
    pass 


















# def generate_neighbor(railmap):
#     # Generate a neighbor by making a small change to the current railmap
#     new_railmap = railmap.copy()
#     # Example of changing a route (this should be customized based on railmap structure)
#     if len(new_railmap) > 1:
#         i = random.randint(0, len(new_railmap) - 1)
#         j = random.randint(0, len(new_railmap) - 1)
#         new_railmap[i], new_railmap[j] = new_railmap[j], new_railmap[i]  # Swap two routes
#     return new_railmap

# def hill_climber(initial_railmap, max_iterations=1000):
#     current_railmap = initial_railmap
#     current_quality = quality_function(current_railmap)
    
#     for _ in range(max_iterations):
#         neighbor = generate_neighbor(current_railmap)
#         neighbor_quality = quality_function(neighbor)
        
#         if neighbor_quality > current_quality:
#             current_railmap = neighbor
#             current_quality = neighbor_quality
#             print(f"New better solution found with quality {current_quality}")
    
#     return current_railmap, current_quality

# # Example usage:
# initial_railmap = ["route1", "route2", "route3", "route4"]  # Placeholder for actual railmap routes
# optimized_railmap, optimized_quality = hill_climber(initial_railmap)
# print(f"Optimized Railmap: {optimized_railmap} with quality: {optimized_quality}")
