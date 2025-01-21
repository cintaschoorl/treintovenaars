import randomise
from code.classes.route import Route
from code.classes.railmap import Railmap

def hill_climber(railmap, iterations, max_duration, calculate_score):
    """
    Hill climber algoritme voor het optimaliseren van de kwaliteitsscore K.
    
    Parameters:
        railmap (Railmap): Het treinnetwerk object.
        iterations (int): Het maximale aantal iteraties.
        max_duration (int): De maximale reistijd van een route.
        calculate_score (function): Functie om de kwaliteitsscore K te berekenen.

    Returns:
        tuple: Beste oplossing en bijbehorende score.
    """
    # Stap 1: Genereer een initiële oplossing met random algoritme
    current_solution = generate_initial_solution(railmap, max_duration)
    current_score = calculate_score(current_solution)

    # Sla de beste oplossing op
    best_solution = current_solution
    best_score = current_score

    print(f"Startpunt: score = {current_score}")

    # Stap 2: Iteratief verbeteren
    for i in range(iterations):
        # Maak een nieuwe oplossing door een mutatie
        new_solution = mutate_solution(current_solution, railmap, max_duration)
        new_score = calculate_score(new_solution)

        # Accepteer de nieuwe oplossing als deze beter is
        if new_score > current_score:
            current_solution = new_solution
            current_score = new_score

            # Update de beste oplossing
            if new_score > best_score:
                best_solution = new_solution
                best_score = new_score

        # Print debug-informatie
        print(f"Iteratie {i + 1}: huidige score = {current_score}, beste score = {best_score}")

    return best_solution, best_score


def generate_initial_solution(railmap, max_duration):
    """
    Genereer een initiële oplossing met een random algoritme.
    
    Parameters:
        railmap (Railmap): Het treinnetwerk object.
        max_duration (int): De maximale reistijd van een route.

    Returns:
        list: Een lijst met routes als initiële oplossing.
    """
    solution = []
    for _ in range(railmap.max_routes):  # max_routes kan een limiet zijn op het aantal routes
        route = Route(railmap.stations, max_duration)
        current_station = random.choice(railmap.stations)
        route.add_station(current_station)
        
        spent_time = 0
        while spent_time < max_duration:
            neighbours = railmap.get_neighbours(current_station)
            if not neighbours:
                break
            next_station, next_time = random.choice(list(neighbours.items()))
            if spent_time + next_time <= max_duration:
                route.add_station(next_station)
                spent_time += next_time
                current_station = next_station
            else:
                break
        solution.append(route)
    return solution


def mutate_solution(solution, railmap, max_duration):
    """
    Maak een mutatie in de huidige oplossing.
    
    Parameters:
        solution (list): De huidige oplossing (lijst met routes).
        railmap (Railmap): Het treinnetwerk object.
        max_duration (int): De maximale reistijd van een route.

    Returns:
        list: Een nieuwe oplossing met een kleine mutatie.
    """
    # Maak een diepe kopie van de oplossing (zodat we de originele niet overschrijven)
    new_solution = solution.copy()

    # Kies een willekeurige route om te muteren
    route_to_mutate = random.choice(new_solution)

    # Kies een mutatie: toevoegen, verwijderen of vervangen van een station
    mutation_type = random.choice(["add_station", "remove_station", "replace_station"])

    if mutation_type == "add_station":
        # Voeg een willekeurige buur toe aan de route
        if route_to_mutate.stations:
            current_station = random.choice(route_to_mutate.stations)
            neighbours = railmap.get_neighbours(current_station)
            if neighbours:
                new_station, travel_time = random.choice(list(neighbours.items()))
                if route_to_mutate.total_time + travel_time <= max_duration:
                    route_to_mutate.add_station(new_station)

    elif mutation_type == "remove_station":
        # Verwijder een willekeurig station uit de route
        if len(route_to_mutate.stations) > 1:
            station_to_remove = random.choice(route_to_mutate.stations)
            route_to_mutate.remove_station(station_to_remove)

    elif mutation_type == "replace_station":
        # Vervang een station door een willekeurige buur
        if route_to_mutate.stations:
            current_station = random.choice(route_to_mutate.stations)
            neighbours = railmap.get_neighbours(current_station)
            if neighbours:
                new_station, travel_time = random.choice(list(neighbours.items()))
                if route_to_mutate.total_time - current_station.travel_time + travel_time <= max_duration:
                    route_to_mutate.replace_station(current_station, new_station)

    return new_solution


def calculate_score(solution):
    """
    Bereken de kwaliteitsscore K van de oplossing.
    
    Parameters:
        solution (list): De oplossing (lijst met routes).

    Returns:
        int: De kwaliteitsscore K.
    """
    score = 0
    visited_stations = set()
    total_time = 0

    for route in solution:
        visited_stations.update(route.stations)
        total_time += route.total_time

    # Voorbeeld van scoreberekening:
    score += len(visited_stations) * 100  # Beloning voor unieke stations
    score -= total_time  # Penaliseer lange reistijd

    return score


# Test het hill climber algoritme
if __name__ == "__main__":
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    railmap = Railmap()
    railmap.load_stations(stations_path, connections_path)

    iterations = 1000
    max_duration = 120

    best_solution, best_score = hill_climber(railmap, iterations, max_duration, calculate_score)
    print(f"Beste oplossing gevonden met score: {best_score}")


