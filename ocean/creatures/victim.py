
class Victim(object):
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration_life = duration

    def move_xy(self, dx, dy):
        self.x += dx
        self.y += dy
        self.duration_life -= 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    @property
    def is_dead(self):
        return self.duration_life <= 0
    
    def get_age(self):
        return self.duration_life
