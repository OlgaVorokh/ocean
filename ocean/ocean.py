import random

from .creatures import Predator, Victim

class Ocean(object):
    def __init__(self, config):
        self.config = config
        self.ocean = []
        self.predators = []
        self.victims = []

    def initialize_random(self):
        self.create_random_ocean()
        self.find_creatures()
        
    def create_random_ocean(self):
        random.seed(self.config.random_seed)
        for i in xrange(self.config.size_ocean):
            line = []
            for j in xrange(self.config.size_ocean):
                current_probability = random.random()
                if current_probability <= self.config.probability_predator:
                    line.append(self.config.label_predator)
                elif (
                    current_probability <= 
                    self.config.probability_predator + 
                    self.config.probability_barrier
                ):
                    line.append(self.config.label_barrier)
                elif (
                    current_probability <= 
                    self.config.probability_predator + 
                    self.config.probability_barrier + 
                    self.config.probability_victim
                ):
                    line.append(self.config.label_victim)
                else:
                    line.append(self.config.label_empty)
            self.ocean.append(line)

    def initialize_from_file(self, filename):
        self.create_from_file(filename)
        self.find_creatures()

    def create_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line_value = map(int, list(line.strip()))
                if len(line_value) != self.config.size_ocean:
                    raise 'ERROR: invalid size of ocean.'
                self.ocean.append(line_value)

        if len(self.ocean) != self.config.size_ocean:
            raise 'ERROR: invalid size of ocean.'

    def find_creatures(self):
        for X in xrange(self.config.size_ocean):
            for Y in xrange(self.config.size_ocean):
                if self.ocean[X][Y] == self.config.label_predator:
                    new_predator = Predator(
                        X, Y, 
                        self.config.predator_satiety, 
                        self.config.predator_duration_life,
                    )
                    self.predators.append(new_predator)
                elif self.ocean[X][Y] == self.config.label_victim:
                    new_victim = Victim(X, Y, self.config.victim_duration_life)
                    self.victims.append(new_victim)

    def create_empty(self):
        """For tests"""
        for i in xrange(self.config.size_ocean):
            self.ocean.append([0] * self.config.size_ocean)

    @property
    def is_over(self):
        return not self.victims and not self.predators

    def make_one_iteration(self, iteration):
        self.check_predators()
        self.check_victims()
       
        self.make_actions()

        if (
            iteration > 0 and 
            not iteration % self.config.predator_reproduction_interval
        ):
            self.predator_reproduction()
        if (
            iteration > 0 and 
            not iteration % self.config.victim_reproduction_interval
        ):
            self.victim_reproduction()

        # self.print_ocean(iteration)

    def print_ocean(self, iteration):
        count_victim = 0
        count_predator = 0
        for X in xrange(len(self.ocean)):
            for Y in xrange(len(self.ocean)):
                if self.ocean[X][Y] == 1:
                    count_predator += 1
                if self.ocean[X][Y] == 3:
                    count_victim += 1
        print 'itr:', iteration, 'v:', count_victim, 'p:', count_predator, 'per:', count_victim / (float)(count_predator + 1)
        
    def check_predators(self):
        result_predators = []
        for predator in self.predators:
            if predator.is_dead:
                X = predator.get_x()
                Y = predator.get_y()
                self.ocean[X][Y] = self.config.label_empty
            else:
                result_predators.append(predator)
        self.predators = result_predators

    def check_victims(self):
        result_victims = []
        for victim in self.victims:
            X = victim.get_x()
            Y = victim.get_y()
            if victim.is_dead:
                self.ocean[X][Y] = self.config.label_empty
            elif self.victim_is_alive(X, Y):
                result_victims.append(victim)
        self.victims = result_victims

    def victim_is_alive(self, X, Y):
        """
        The victim can be eat during iteration by predator.
        This event is marked on the ocean, so this victim is 
        not deleted from self.victims immediately after the murder.
        Thats why when array of current victims should be updated,
        you should check if this victim is exist on the ocean in its place
        """
        return self.ocean[X][Y] == self.config.label_victim

    def make_actions(self):
        for predator in self.predators:
            self.step_predator(predator)
        for victim in self.victims:
            self.step_victim(victim)
        self.check_victims()
      
    def step_predator(self, predator):
        X = predator.get_x()
        Y = predator.get_y()
        
        move_order = range(len(self.config.dx))
        random.shuffle(move_order)
        is_moved = False

        # try to eat a victim
        for step in move_order:
            x_new = X + self.config.dx[step]
            y_new = Y + self.config.dy[step]
            if (
                self.in_ocean(x_new, y_new) and
                self.ocean[x_new][y_new] == self.config.label_victim
            ):
                self.eat_predator_victim(predator, X, Y, x_new, y_new)
                is_moved = True
                break

        # try to move somewhere
        for step in move_order:
            x_new = X + self.config.dx[step]
            y_new = Y + self.config.dy[step]
            if (
                self.in_ocean(x_new, y_new) and
                self.ocean[x_new][y_new] == self.config.label_empty and 
                not is_moved
            ):
                self.move_predator(predator, X, Y, x_new, y_new)
                is_moved = True
                break

        if not is_moved:
            predator.move_xy(0, 0)

    def eat_predator_victim(self, predator, X1, Y1, X2, Y2):
        predator.eat_xy(X2 - X1, Y2 - Y1)
        self.ocean[X1][Y1] = self.config.label_empty
        self.ocean[X2][Y2] = self.config.label_predator

    def move_predator(self, predator, X1, Y1, X2, Y2):
        predator.move_xy(X2 - X1, Y2 - Y1)
        self.ocean[X1][Y1] = self.config.label_empty
        self.ocean[X2][Y2] = self.config.label_predator

    def step_victim(self, victim):
        X = victim.get_x()
        Y = victim.get_y()

        # can be eat by predator (their steps goes first)
        if not self.victim_is_alive(X, Y):
            return

        move_order = range(len(self.config.dx))
        random.shuffle(move_order)
        is_moved = False
        for step in move_order:
            x_new = X + self.config.dx[step]
            y_new = Y + self.config.dy[step]
            if (
                self.in_ocean(x_new, y_new) and
                self.ocean[x_new][y_new] == self.config.label_empty
            ):
                self.move_victim(victim, X, Y, x_new, y_new)
                is_moved = True
                break

        if not is_moved:
            victim.move_xy(0, 0)

    def move_victim(self, victim, X1, Y1, X2, Y2):
        victim.move_xy(X2 - X1, Y2 - Y1)
        self.ocean[X1][Y1] = self.config.label_empty 
        self.ocean[X2][Y2] = self.config.label_victim  

    def predator_reproduction(self):
        new_creaters = []   
        for predator in self.predators:
            X = predator.get_x()
            Y = predator.get_y()

            move_order = range(len(self.config.dx))
            random.shuffle(move_order)
            is_moved = False  

            for step in move_order:
                x_new = X + self.config.dx[step]
                y_new = Y + self.config.dy[step]
                if (
                    self.in_ocean(x_new, y_new) and
                    self.ocean[x_new][y_new] == self.config.label_empty
                ):
                    self.ocean[x_new][y_new] = self.config.label_predator
                    new_predator = Predator(
                        x_new, y_new, 
                        self.config.predator_satiety, 
                        self.config.predator_duration_life
                    )
                    new_creaters.append(new_predator)
                    is_moved = True
                    break

            for step in move_order:
                x_new = X + self.config.dx[step]
                y_new = Y + self.config.dy[step]
                if (
                    self.in_ocean(x_new, y_new) and
                    self.ocean[x_new][y_new] == self.config.label_victim and 
                    not is_moved
                ):
                    self.eat_predator_victim(predator, X, Y, x_new, y_new)
                    self.ocean[X][Y] = self.config.label_predator
                    new_predator = Predator(
                        X, Y, 
                        self.config.predator_satiety, 
                        self.config.predator_duration_life
                    )
                    new_creaters.append(new_predator)
                    is_moved = True
                    break   

            if not is_moved:
                predator.move_xy(0, 0)
        
        self.check_victims()
        self.predators.extend(new_creaters)

    def victim_reproduction(self):
        new_creaters = []
        for victim in self.victims:
            X = victim.get_x()
            Y = victim.get_y()

            move_order = range(len(self.config.dx))
            random.shuffle(move_order)
            is_moved = False
            for step in move_order:
                x_new = X + self.config.dx[step]
                y_new = Y + self.config.dy[step]
                if (
                    self.in_ocean(x_new, y_new) and
                    self.ocean[x_new][y_new] == self.config.label_empty
                ):
                    self.ocean[x_new][y_new] = self.config.label_victim
                    new_victim = Victim(
                        x_new, y_new,
                        self.config.victim_duration_life,
                    )
                    new_creaters.append(new_victim)
                    is_moved = True
                    break

            if not is_moved:
                victim.move_xy(0, 0)

        self.victims.extend(new_creaters)

    def in_ocean(self, X, Y):
        return (
            0 <= X < self.config.size_ocean and
            0 <= Y < self.config.size_ocean
        )

    def to_file(self, filename):
        with open(filename, 'w') as f:
            for line in self.ocean:
                line_str = ''.join(map(str, line))
                f.write('{}\n'.format(line_str))
