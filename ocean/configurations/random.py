from .base import OceanBaseConfig

class OceanRandomConfig(OceanBaseConfig):
    eps = 1e-9
    probability_full = 1.

    def __init__(self, parser, *args, **kwargs):
        super(OceanRandomConfig, self).__init__(parser, *args, **kwargs)
        
        self.random_seed = int(parser.get('random', 'random_seed'))
        self.probability_predator = float(parser.get('random', 'probability_predator'))
        self.probability_barrier = float(parser.get('random', 'probability_barrier'))
        self.probability_victim = float(parser.get('random', 'probability_victim'))
        self.probability_empty = float(parser.get('random', 'probability_empty'))

        probability_sum = (self.probability_barrier + self.probability_empty + 
            self.probability_predator + self.probability_victim)
        if abs(probability_sum - self.probability_full) > self.eps:
            raise 'ERROR: probabilities for creating ocean are incorrect!'
