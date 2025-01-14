class Routemap():
    """
    The full route system with all trajectories
    """
    def __init__(self):
        self.trajectories = {}

    def add_trajectory(self, train):
        self.trajectories[train.id] = train

    def fraction_p(self):
        "Compute fraction p of used connections"
        self.p = 0.8 # example value -> needs to be computed!

    def quality_K(self):
        T = len(self.trajectories)
        Min = 0

        for values in self.trajectories.values():
            Min += values[1]
        
        # compute quality of the lines K
        return (self.p * 10000 - (T * 100 + Min))