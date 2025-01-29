# Treintovenaars - RailNL

De Nederlandse Spoorwegen (NS) zoekt naar een optimale lijnvoering voor haar intercity-treinen. Het doel is om een dienstregeling te creëren die alle belangrijke verbindingen berijdt, binnen de gestelde tijdslimieten blijft, en de kwaliteit maximaliseert volgens de formule:

    K = p*10000 - (T*100 + Min)

waarbij:
- K = kwaliteit van de lijnvoering
- p = fractie van bereden verbindingen (0-1)
- T = aantal trajecten
- Min = totaal aantal minuten van alle trajecten

We lossen dit op voor twee cases:
1. Noord- en Zuid-Holland (max 7 trajecten, 120 minuten per traject)
2. Nederland (max 20 trajecten, 180 minuten per traject)
   
## Gebruikte algoritmes

### 1. Random algoritme
Dit algoritme genereert een random route.
- Selecteert een random beginstatiom
- Bouwt routes op door een willekeurige buur te kiezen
- Stopt met toevoegen als de tijdslimiet is bereikt

randomise_heuristics() is een random algoritme met de volgende heuristieken:
1. 50% kans dat een startstation begint bij een station met één buurstation.
2. De trein mag niet op en neer pendelen (A --> B --> A).
3. Minimaliseren van overlap tussen verschillende routes in de lijnvoering.

### 2. Random Greedy algoritme
Dit random algoritme genereert ook een random route, maar volgens het Greedy principe. Onbereden verbindingen en verbindingen met de kortste reistijd hebben hierbij prioriteit. 

### 3. Hill Climber algoritme
Dit is een iteratief algoritme en start met een random route en maakt stapsgewijs kleine aanpassingen. Bij de aanpassing word een random route en daarbinnnen een random stations geselecteerd, vanaf hier word een knip gemaakt en de route opnieuw afgebouwd. Hij accepteert alleen veranderingen die de kwaliteitsscore K verhoogt. 

### 4. Simulated Annealing
Dit is een optimalisatie die voortbouwt op de Hill Climber aanpak. In het begin accepteert hij alleen slechtere oplossingen. Hierna vermindert de acceptatie van slechtere oplossingen geleidelijk. Deze optimalisatie helpt bij het ontsnappen aan lokale optima.
  
## Aan de slag
### Vereisten
Deze codebase is geschreven in Python v3.10.8. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

    pip install -r requirements.txt

Of via conda:

    conda install --file requirements.txt

### Gebruik
Start het programma met:

    python main.py

Dit voert grid search uit voor de algoritmes met verschillende parameters.

### Parameters Aanpassen
Je kunt de volgende parameters aanpassen in `main.py`:
- `iterations`: Aantal iteraties 
- `num_routes`: Aantal trajecten (max: 7 voor Holland, 20 voor Nederland)
- `max_duration`: Maximale trajectduur (standaard: 120 voor Holland, 180 voor Nederland)

### Output
Resultaten worden opgeslagen in de `/output` map:
- Grid search resultaten: `grid_search_{algoritme}.csv`
- Beste routes: `best_railmap_{algoritme}.json`
- Visualisaties: `quality_scores_histogram_{algoritme}.png`

### Structuur
Het project is als volgt georganiseerd:

- `/code`: bevat alle code van dit project
  - `/code/algorithms`: bevat onze implementaties van de volgende algoritmes:
    - Random
    - Random + greedy
    - Hill Climber
    - Simulated
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
