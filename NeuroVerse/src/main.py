# neuroverse - simple neural network game
# red = fire (run away), green = food (eat), blue = you
# use arrow keys or wasd to move manually, AI will also react
import pygame
import sys
import random

# Neuron class
class Neuron:
    def __init__(self, name, kind='hidden'):
        self.name = name
        self.kind = kind  # 'input', 'hidden', or 'output'
        self.val = 0.0
        self.out = []  # list of (target_neuron, weight) tuples

    def link(self, target, w=1.0):
        """Create a weighted connection to another neuron"""
        self.out.append((target, w))

    def fire(self):
        """Activation function - simple threshold"""
        # Keep the value as is, don't force to binary 0/1
        # This allows negative weights to work properly
        pass

# Brain class - neural network
class Brain:
    def __init__(self):
        self.n = {}  # dictionary of neurons by name

    def add(self, neuron):
        """Add a neuron to the brain"""
        self.n[neuron.name] = neuron

    def set(self, name, val):
        """Set input neuron value"""
        if name in self.n and self.n[name].kind == 'input':
            self.n[name].val = val

    def run(self):
        """Execute one forward pass through the network"""
        # Reset non-input neurons
        for neuron in self.n.values():
            if neuron.kind != 'input':
                neuron.val = 0.0
        
        # Forward pass: each neuron sends its value to all connected targets
        for neuron in self.n.values():
            for target, weight in neuron.out:
                target.val += neuron.val * weight
        
        # Activation function
        for neuron in self.n.values():
            if neuron.kind != 'input':
                neuron.fire()
        
        # Return output neuron values
        return {name: n.val for name, n in self.n.items() if n.kind == 'output'}

# World environment
class World:
    def __init__(self):
        self.s = 10  # grid size
        self.g = [[0]*10 for _ in range(10)]  # grid: 0=empty, 1=fire, 2=food
        # Initial objects
        self.spawn_objects()

    def spawn_objects(self):
        """Place fire and food randomly"""
        self.g = [[0]*10 for _ in range(10)]
        # Place 3 fire tiles
        fire_count = 0
        while fire_count < 3:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if self.g[y][x] == 0 and not (x == 5 and y == 5):  # don't spawn on start
                self.g[y][x] = 1
                fire_count += 1
        # Place 4 food tiles
        food_count = 0
        while food_count < 4:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if self.g[y][x] == 0 and not (x == 5 and y == 5):
                self.g[y][x] = 2
                food_count += 1

    def sense_nearby(self, x, y):
        """Sense objects in adjacent cells with directional info"""
        sensors = {
            'fire_left': 0.0, 'fire_right': 0.0, 
            'fire_up': 0.0, 'fire_down': 0.0,
            'food_left': 0.0, 'food_right': 0.0,
            'food_up': 0.0, 'food_down': 0.0
        }
        
        # Check each direction
        directions = {
            'left': (-1, 0), 'right': (1, 0),
            'up': (0, -1), 'down': (0, 1)
        }
        
        for dir_name, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.s and 0 <= ny < self.s:
                if self.g[ny][nx] == 1:
                    sensors[f'fire_{dir_name}'] = 1.0
                if self.g[ny][nx] == 2:
                    sensors[f'food_{dir_name}'] = 1.0
        
        return sensors

# Character (player)
class Character:
    def __init__(self, x, y, brain):
        self.x = x
        self.y = y
        self.b = brain
        self.h = 100.0  # hunger/health (0-100)
        self.score = 0

    def ai_move(self, world):
        """Process AI behavior and decide movement"""
        sensors = world.sense_nearby(self.x, self.y)
        
        # Set directional input sensors
        self.b.set('fire_left', sensors['fire_left'])
        self.b.set('fire_right', sensors['fire_right'])
        self.b.set('fire_up', sensors['fire_up'])
        self.b.set('fire_down', sensors['fire_down'])
        self.b.set('food_left', sensors['food_left'])
        self.b.set('food_right', sensors['food_right'])
        self.b.set('food_up', sensors['food_up'])
        self.b.set('food_down', sensors['food_down'])
        self.b.set('hunger_sensor', 1.0 - self.h/100.0)

        # Run neural network
        actions = self.b.run()

        # Find the strongest action (can now be negative)
        best_action = None
        best_val = -999  # allow negative values
        
        for action_name in ['move_left', 'move_right', 'move_up', 'move_down']:
            if actions.get(action_name, 0) > best_val:
                best_val = actions[action_name]
                best_action = action_name

        # Execute best action only if positive
        if best_val > 0:
            if best_action == 'move_left' and self.x > 0:
                self.x -= 1
            elif best_action == 'move_right' and self.x < world.s - 1:
                self.x += 1
            elif best_action == 'move_up' and self.y > 0:
                self.y -= 1
            elif best_action == 'move_down' and self.y < world.s - 1:
                self.y += 1

    def check_tile(self, world):
        """Check what's on current tile and react"""
        if world.g[self.y][self.x] == 1:  # fire
            self.h = max(0, self.h - 20)
            self.score -= 10
        elif world.g[self.y][self.x] == 2:  # food
            self.h = min(100, self.h + 30)
            world.g[self.y][self.x] = 0  # consume food
            self.score += 20

    def update(self):
        """Update character state"""
        # Gradual hunger decrease
        self.h = max(0, self.h - 0.2)

# Build neural network brain
def build_brain():
    b = Brain()

    # Directional input neurons for fire
    fire_left = Neuron('fire_left', 'input')
    fire_right = Neuron('fire_right', 'input')
    fire_up = Neuron('fire_up', 'input')
    fire_down = Neuron('fire_down', 'input')
    
    # Directional input neurons for food
    food_left = Neuron('food_left', 'input')
    food_right = Neuron('food_right', 'input')
    food_up = Neuron('food_up', 'input')
    food_down = Neuron('food_down', 'input')
    
    # Hunger sensor
    hunger_sensor = Neuron('hunger_sensor', 'input')

    # Output neurons
    move_left = Neuron('move_left', 'output')
    move_right = Neuron('move_right', 'output')
    move_up = Neuron('move_up', 'output')
    move_down = Neuron('move_down', 'output')

    # Add all neurons to brain
    for n in [fire_left, fire_right, fire_up, fire_down,
              food_left, food_right, food_up, food_down,
              hunger_sensor, move_left, move_right, move_up, move_down]:
        b.add(n)

    # SMART WIRING: Run AWAY from fire (don't move toward fire!)
    fire_left.link(move_left, -3.0)    # fire on left -> DON'T move left (negative weight)
    fire_right.link(move_right, -3.0)  # fire on right -> DON'T move right
    fire_up.link(move_up, -3.0)        # fire above -> DON'T move up
    fire_down.link(move_down, -3.0)    # fire below -> DON'T move down
    
    # Also encourage moving AWAY from fire
    fire_left.link(move_right, 2.0)    # fire on left -> prefer right
    fire_right.link(move_left, 2.0)    # fire on right -> prefer left
    fire_up.link(move_down, 2.0)       # fire above -> prefer down
    fire_down.link(move_up, 2.0)       # fire below -> prefer up

    # SMART WIRING: Move TOWARD food when hungry (weaker than fear)
    food_left.link(move_left, 1.0)     # food on left -> move left
    food_right.link(move_right, 1.0)   # food on right -> move right
    food_up.link(move_up, 1.0)         # food above -> move up
    food_down.link(move_down, 1.0)     # food below -> move down
    
    # Hunger amplifies food seeking slightly
    hunger_sensor.link(move_left, 0.2)
    hunger_sensor.link(move_right, 0.2)
    hunger_sensor.link(move_up, 0.2)
    hunger_sensor.link(move_down, 0.2)

    return b

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 450))
    pygame.display.set_caption("NeuroVerse - Neural AI Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    small_font = pygame.font.SysFont(None, 18)

    w = World()
    brain = build_brain()
    p = Character(5, 5, brain)

    # Keyboard state
    keys = {
        pygame.K_LEFT: False, pygame.K_RIGHT: False,
        pygame.K_UP: False, pygame.K_DOWN: False,
        pygame.K_a: False, pygame.K_d: False,
        pygame.K_w: False, pygame.K_s: False
    }

    running = True
    tick_count = 0
    manual_move_this_frame = False
    
    while running:
        manual_move_this_frame = False
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key in keys:
                    keys[e.key] = True
                if e.key == pygame.K_r:  # reset
                    w.spawn_objects()
                    p.x, p.y = 5, 5
                    p.h = 100
                    p.score = 0
                    tick_count = 0
            if e.type == pygame.KEYUP:
                if e.key in keys:
                    keys[e.key] = False

        # Manual movement (takes priority)
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
            dy = 1
        
        if dx or dy:
            nx = p.x + dx
            ny = p.y + dy
            if 0 <= nx < w.s and 0 <= ny < w.s:
                p.x, p.y = nx, ny
                manual_move_this_frame = True

        # AI movement (only if no manual input and health > 0)
        if not manual_move_this_frame and p.h > 0 and tick_count % 8 == 0:
            p.ai_move(w)

        # Check current tile
        p.check_tile(w)
        
        # Update character
        if p.h > 0:
            p.update()

        # Draw
        screen.fill((240, 240, 240))
        
        # Draw grid
        cell_size = 40
        for y in range(w.s):
            for x in range(w.s):
                rect = pygame.Rect(x*cell_size + 50, y*cell_size + 50, cell_size, cell_size)
                
                if w.g[y][x] == 1:  # fire
                    pygame.draw.rect(screen, (255, 100, 100), rect)
                elif w.g[y][x] == 2:  # food
                    pygame.draw.rect(screen, (100, 255, 100), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                
                pygame.draw.rect(screen, (180, 180, 180), rect, 1)

        # Draw player
        cx = p.x * cell_size + cell_size // 2 + 50
        cy = p.y * cell_size + cell_size // 2 + 50
        pygame.draw.circle(screen, (50, 50, 255), (cx, cy), cell_size // 2 - 5)

        # UI - Health bar
        bar_width = 300
        fill = int(bar_width * p.h / 100)
        pygame.draw.rect(screen, (255, 100, 100), (100, 10, bar_width, 25))
        pygame.draw.rect(screen, (100, 255, 100), (100, 10, fill, 25))
        pygame.draw.rect(screen, (0, 0, 0), (100, 10, bar_width, 25), 2)

        # Text
        health_text = font.render(f"Health: {int(p.h)}", True, (0, 0, 0))
        score_text = font.render(f"Score: {p.score}", True, (0, 0, 0))
        control_text = small_font.render("Arrow/WASD,  R:Restart", True, (100, 100, 100))
        legend_text = small_font.render("Red=Fire  Green=Food  Blue=You", True, (100, 100, 100))
        
        screen.blit(health_text, (105, 12))
        screen.blit(score_text, (300, 12))
        screen.blit(control_text, (100, 420))
        screen.blit(legend_text, (250, 420))

        # Game over
        if p.h <= 0:
            game_over = font.render("GAME OVER! Press R to restart", True, (255, 0, 0))
            screen.blit(game_over, (120, 230))

        pygame.display.flip()
        clock.tick(10)
        tick_count += 1

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()