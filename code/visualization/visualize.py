import csv
import pandas as pd
from plotnine import element_blank
from plotnine import ggplot, aes, geom_point, geom_text, geom_segment, labs, theme_minimal, theme
import os


class Station:
    """
    Initializing the stations with their coördinates
    """
    def __init__(self, name, y, x):
        self.name = name
        self.y = y
        self.x = x


class Connection:
    """
    Initializing the connections with their stations
    """
    def __init__(self, station1, station2, travel_time):
        self.station1 = station1
        self.station2 = station2
        self.travel_time = travel_time


def load_stations(filepath):
    """
    Loading the stations from the StationsHolland.csv file
    """

    stations = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            name, y, x = row

            # de stations lijst vullen met de name, x and y voor ieder station
            stations.append(Station(name, float(y), float(x)))

    return stations



def load_connections(filepath):
    """
    Loading the connections with their stations and the travel time
    """
    connections = []

    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            station1, station2, travel_time = row

            # de connections lijst vullen
            connections.append(Connection(station1, station2, int(travel_time)))
    return connections



if __name__ == "__main__":

    # in de juiste mappen de juiste data vinden als input voor de functies die deze inladen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stations_path = os.path.join(script_dir, "../../data/StationsHolland.csv")
    connections_path = os.path.join(script_dir, "../../data/ConnectiesHolland.csv")

    # een output pad creëren
    output_dir = os.path.join(script_dir, "output")
    output_path = os.path.join(output_dir, "train_routes_plot.png")

    os.makedirs(output_dir, exist_ok=True)


    # de data inladen vanuit de voorgaande csv files
    stations = load_stations(stations_path)
    connections = load_connections(connections_path)

    stations.sort(key=lambda station: station.y)

    connections_data = []
    stations_dict = {station.name: station for station in stations}

    for connection in connections:
        station1 = stations_dict[connection.station1]
        station2 = stations_dict[connection.station2]
        connections_data.append({
            "from_station": station1.name,
            "to_station": station2.name,
            "from_x": station1.x,
            "from_y": station1.y,
            "to_x": station2.x,
            "to_y": station2.y,
            "travel_time": connection.travel_time
        })

    connections_df = pd.DataFrame(connections_data)

    # de plot aanmaken en opslaan
    plot = (
        ggplot(connections_df) +
        geom_segment(
            aes(x='from_x', y='from_y', xend='to_x', yend='to_y', color='travel_time'),
            size=1,
            alpha=0.8
        ) +
        geom_point(
            aes(x='from_x', y='from_y'),
            size=4,
            color='blue'
        ) +
        geom_text(
            aes(x='from_x', y='from_y', label='from_station'),
            nudge_y=0.02,
            size=8,
            ha="center"
        ) +
        labs(
            title="Train Route Connections",
            x="Longitude",
            y="Latitude",
            color="Travel Time (min)"
        ) +
        theme_minimal() +
        theme(
            axis_text_x=element_blank(),
            axis_text_y=element_blank(),
            axis_ticks=element_blank()
        )
    )


    plot.save(output_path)
    print(f"Plot saved to {output_path}")
