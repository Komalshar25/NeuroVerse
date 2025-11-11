import random

class World:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 0: empty, 1: fire, 2: food
        self.place_fires(3)   # Fewer fires
        self.place_food(3)    # Add 3 food items

    def place_fires(self, num):
        for _ in range(num):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            self.grid[y][x] = 1

    def place_food(self, num):
        for _ in range(num):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            while self.grid[y][x] != 0:  # Don't place on fire
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            self.grid[y][x] = 2

    def get_sensors(self, char_x, char_y):
        # Fire sensor (nearby fire)
        fire_nearby = 0
        food_nearby = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = char_x + dx, char_y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.grid[ny][nx] == 1:
                        fire_nearby = 1
                    elif self.grid[ny][nx] == 2:
                        food_nearby = 1
        return {'fire_sensor': fire_nearby, 'food_sensor': food_nearby}

    def eat_food(self, char_x, char_y):
        """Character eats food if standing on it"""
        if self.grid[char_y][char_x] == 2:
            self.grid[char_y][char_x] = 0  # Remove food
            return True
        return False