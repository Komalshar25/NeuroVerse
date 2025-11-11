class Character:
    def __init__(self, x, y, brain):
        self.x = x
        self.y = y
        self.brain = brain
        self.hunger = 50  # Hunger starts medium (0-100)

    def update(self, sensors, world):
        # Hunger grows over time
        self.hunger += 0.1   # ← SLOWER!
        self.hunger = min(100, self.hunger)

        # Add hunger to sensors (high hunger = strong signal)
        sensors['hunger_sensor'] = 1 if self.hunger > 30 else 0

        # Brain decides actions
        outputs = self.brain.process(sensors)

        # Move based on brain
        if outputs.get('move_left', 0):
            self.x -= 1
        if outputs.get('move_right', 0):
            self.x += 1
        if outputs.get('move_up', 0):
            self.y -= 1
        if outputs.get('move_down', 0):
            self.y += 1

        # Clamp position
        self.x = max(0, min(9, self.x))
        self.y = max(0, min(9, self.y))

        # Eat food if standing on it
        world.eat_food(self.x, self.y)
        if world.eat_food(self.x, self.y):  # Eats → resets hunger
            self.hunger = 0