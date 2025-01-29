from code.algorithms.hillclimber import hill_climber
from code.algorithms.simulated_annealing import simulated_annealing
from code.classes.railmap import Railmap

if __name__ == "__main__":
    stations_Holland_path = "data/StationsHolland.csv"
    stations_NL_path = "data/StationsNationaal.csv"
    connections_Holland_path = "data/ConnectiesHolland.csv"
    connections_NL_path = "data/ConnectiesNationaal.csv"
    uid_path_Holland = "data/uid_Holland.csv"
    uid_path_NL = "data/uid_NL.csv"

    Holland_kwargs = (stations_Holland_path, uid_path_Holland, connections_Holland_path)
    Netherlands_kwargs = (stations_NL_path, uid_path_NL, connections_NL_path)

    ### HOLLAND ###
    # create railmap
    railmap = Railmap()
    railmap.load_stations(*Holland_kwargs)


    best_railmap, best_score, all_scores = hill_climber(railmap, 5000, 120, 4)

    print(f"Best Hill Climber score (Holland): {best_score}\n")
    for train, route in best_railmap.routes.items():
        print(f"{train}: {route.route}\n")

    # create new railmap
    railmap2 = Railmap()
    railmap2.load_stations(*Holland_kwargs)


    best_railmap2, best_score2, all_scores2, _ = simulated_annealing(railmap2, 5000, 120, 4)

    print(f"\nBest Simulated Annealing score (Holland): {best_score2}\n")
    for train, route in best_railmap2.routes.items():
        print(f"{train}: {route.route}\n")

    ### NETHERLANDS ###
       # create railmap
    railmap = Railmap()
    railmap.load_stations(*Netherlands_kwargs)


    best_railmap, best_score, all_scores = hill_climber(railmap, 5000, 120, 4)

    print(f"Best Hill Climber score (Netherlands): {best_score}\n")
    for train, route in best_railmap.routes.items():
        print(f"{train}: {route.route}\n")

    # create new railmap
    railmap2 = Railmap()
    railmap2.load_stations(*Netherlands_kwargs)


    best_railmap2, best_score2, all_scores2, _ = simulated_annealing(railmap2, 5000, 120, 4)

    print(f"\nBest Simulated Annealing score (Netherlands): {best_score2}\n")
    for train, route in best_railmap2.routes.items():
        print(f"{train}: {route.route}\n")

### CONCLUSIE: (holland) ###
# Simulated annealing scored hoger bij meer iteraties (1000 vs 5000) om goed de mogelijkheden te exploreren,
# HC convergeerd al sneller en kan hoger scoren bij bv maar 1000i . Voor HC dus niet veel iteraties nodig,
# Sim Ann wel meer voor een zo goed mogelijk resultaat
