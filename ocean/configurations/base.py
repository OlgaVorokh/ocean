
class DisplayBaseConfig(object):
    version = 'Ocean 2.0'

    window_size = 600
    window_parameters = (window_size, window_size)

    time_sleep = 0.1

    background_color = "#000080"
    empty_color = "#4169E1"
    predator_color = "#FF6347"
    barrier_color = "#191970"
    victim_color = "#FFFAF0"

    colors = [
        empty_color, 
        predator_color, 
        barrier_color, 
        victim_color
    ]

    def __init__(self, parser, iterations):
        self.iterations = iterations

        self.size_ocean = int(parser.get('ocean', 'size_ocean'))
        self.cell_size = self.window_size / self.size_ocean
        self.cell_parameters = (self.cell_size, self.cell_size)


class OceanBaseConfig(object):
    label_empty = 0
    label_predator = 1
    label_barrier = 2
    label_victim = 3

    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    def __init__(self, parser):
        self.size_ocean = int(parser.get('ocean', 'size_ocean'))
    
        self.predator_duration_life = int(parser.get('ocean', 'predator_duration_life'))
        self.predator_reproduction_interval = int(parser.get('ocean', 'predator_reproduction_interval'))
        self.predator_satiety = int(parser.get('ocean', 'predator_hungry_interval'))
        
        self.victim_duration_life = int(parser.get('ocean', 'victim_duration_life'))
        self.victim_reproduction_interval = int(parser.get('ocean', 'victim_reproduction_interval'))
