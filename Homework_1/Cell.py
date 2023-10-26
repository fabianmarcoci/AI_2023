
class Cell:
    def __init__(self, poz_x, poz_y, value):
        self.poz_x = poz_x
        self.poz_y = poz_y
        self.value = value
        self.recently_moved = False

    def get_x(self):
        return self.poz_x

    def get_y(self):
        return self.poz_y

    def set_x(self, poz_x):
        self.poz_x = poz_x

    def set_y(self, poz_y):
        self.poz_y = poz_y

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def set_recently_moved(self, recently_moved):
        self.recently_moved = recently_moved

    def is_moveable(self):
        if self.recently_moved:
            return False
        else:
            return True

