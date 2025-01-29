# Treintovenaars - RailNL

De Nederlandse Spoorwegen (NS) zoekt naar een optimale lijnvoering voor haar intercity-treinen. Het doel is om een dienstregeling te creëren die alle belangrijke verbindingen berijdt, binnen de gestelde tijdslimieten blijft, en de kwaliteit maximaliseert volgens de formule:

    K = p*10000 - (T*100 + Min)

waarbij:
- K = kwaliteit van de lijnvoering
- p = fractie van bereden verbindingen (0-1)
- T = aantal trajecten
- Min = totaal aantal minuten van alle trajecten

## Aan de slag
### Vereisten
Deze codebase is geschreven in Python. 

### Gebruik
Start het programma met:

    python main.py

### Structuur
Het project is als volgt georganiseerd:

- `/code`: bevat alle code van dit project
  - `/code/algorithms`: bevat onze implementaties van:
    - Random algoritme en heuristieken
    - Random greedy algoritme
    - Hill Climber algoritme
    - Simulated Annealing
  - `/code/classes`: bevat de kernclasses:
    - Station
    - Route
    - Railmap
  - `/code/visualisation`: bevat visualisatie tools voor:
    - Kaartweergave van trajecten
    - Statistieken en grafieken
- `/data`: bevat de databestanden:
  - Holland stations en verbindingen
  - Nationaal stations en verbindingen

### Auteurs
Groepsproject Algoritmen &amp; Heuristieken
- Cinta Schoorl
- Isa Wagemans
- Emma van Tuinen
