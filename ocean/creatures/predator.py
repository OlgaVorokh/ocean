
class Predator(object):
    def __init__(self, x, y, satiety, duration):
        self.x = x
        self.y = y
        self.satiety_limit = satiety

        self.satiety = satiety
        self.duration_life = duration

    def move_xy(self, dx, dy):
        self.x += dx
        self.y += dy
        
        self.satiety -= 1
        self.duration_life -= 1

    def eat_xy(self, dx, dy):
        self.x += dx
        self.y += dy
        
        self.satiety += self.satiety_limit   
        self.duration_life -= 1

    @property
    def is_dead(self):
        return self.satiety <= 0 or self.duration_life <= 0
        
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_satiety(self):
        return self.satiety
