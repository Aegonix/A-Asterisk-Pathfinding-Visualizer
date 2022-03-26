from tracemalloc import start
import pygame
import random

pygame.init()

# Global Variables
WIDTH, HEIGHT = 700, 500
NODELENGTH = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualizer")
clock = pygame.time.Clock()
pathfinding = False
current = None

class Node:
    nodes = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.is_start = False
        self.is_target = False
        self.color = WHITE
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.is_wall = False
        self.is_explored = False
        self.is_selected = False
        self.path_dist = 0
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, NODELENGTH, NODELENGTH))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, NODELENGTH, NODELENGTH), 1)
    
    @classmethod
    def create_nodes(cls):
        for i in range(0, WIDTH, NODELENGTH):
            for j in range(0, HEIGHT, NODELENGTH):
                cls.nodes.append(Node(i, j))

        return cls.nodes
    
    def find_neighbours(self):
        for node in Node.nodes:
            # Straight
            if node.x == self.x and node.y == self.y - NODELENGTH: # Up
                self.neighbours.append(node)
            elif node.x == self.x and node.y == self.y + NODELENGTH: # Down
                self.neighbours.append(node)
            elif node.x == self.x - NODELENGTH and node.y == self.y: # Left
                self.neighbours.append(node)
            elif node.x == self.x + NODELENGTH and node.y == self.y: # Right
                self.neighbours.append(node)
            
            # Diagonal
            elif node.x == self.x - NODELENGTH and node.y == self.y - NODELENGTH: # Up Left
                self.neighbours.append(node)
            elif node.x == self.x + NODELENGTH and node.y == self.y - NODELENGTH: # Up Right
                self.neighbours.append(node)
            elif node.x == self.x - NODELENGTH and node.y == self.y + NODELENGTH: # Down Left
                self.neighbours.append(node)
            elif node.x == self.x + NODELENGTH and node.y == self.y + NODELENGTH: # Down Right
                self.neighbours.append(node)
            
            if len(self.neighbours) == 8:
                break
        
    def set_color(self):
        if self.is_start:
            self.color = YELLOW
        elif self.is_target:
            self.color = RED
        elif self.is_wall:
            self.color = BLACK
        elif self.is_explored:
            self.color = GREEN
            if self.is_selected:
                self.color = BLUE
        else:
            self.color = WHITE
    
    def __sub__(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def reset(self):
        # Reset all attributes to original state
        self.is_start = False
        self.is_target = False
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.is_wall = False
        self.is_explored = False
        self.is_selected = False
        self.path_dist = 0
        self.set_color()

def pick_start_and_target(nodes):
    start = random.choice(nodes)
    target = random.choice(nodes)

    while start == target:
        target = random.choice(nodes)
    
    start.is_start = True
    start.set_color()
    target.is_target = True
    target.set_color()

    return start, target

def create_obstacles(nodes):
    for node in nodes:
        if random.randint(1, 20) == 1:
            node.is_wall = True
            node.set_color()
            for neighbour in node.neighbours:
                if random.randint(1, 4) == 1:
                    neighbour.is_wall = True
                    neighbour.set_color()

def pathfind(target_node):
    global pathfinding
    global current
    # start_node = current
    # open = [start_node]
    # closed = []

    while pathfinding:
        # print(sorted(open, key=lambda x: x.f))
        # current = sorted(open, key=lambda x: x.f)[0]
        # open.remove(current)
        # closed.append(current)
        
        # if current == target_node:
        #     break

        for neighbour in current.neighbours:
            # if neighbour in closed or neighbour.is_wall:
            #     continue

            if neighbour.is_target:
                pathfinding = False
                break

            if not neighbour.is_wall:
                neighbour.is_explored = True
                neighbour.set_color()
                neighbour.parent = current
                neighbour.g = neighbour - current
                neighbour.h = neighbour - target_node
                neighbour.f = neighbour.g + neighbour.h
                print(neighbour.f)


        current.neighbours.sort(key=lambda x: x.f if not x.is_wall else float('inf'))
        lowest_f_cost_node = current.neighbours[0]
        for i in range(1, len(current.neighbours)):
            if lowest_f_cost_node.f == current.neighbours[i].f and not current.neighbours[i].is_wall:
                current = current.neighbours[i] if current.neighbours[i].h < lowest_f_cost_node.h else lowest_f_cost_node
            else:
                current = lowest_f_cost_node
                break

        print(f"\n{current.f}")
        current.is_selected = True
        current.set_color()
        yield

    pathfinding = False
        
def draw(nodes):
    screen.fill(BLACK)
    for node in nodes:
        node.draw()

def main():
    global pathfinding
    global current

    running = True
    nodes = Node.create_nodes()
    for i, node in enumerate(nodes):
        node.find_neighbours()
        print(i)
    print("All Neighbours found")
    start_node, target_node = pick_start_and_target(nodes)
    current = start_node
    create_obstacles(nodes)

    while running:
        clock.tick(60)

        if pathfinding:
            next(generator)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Pathfinding Starting")
                    pathfinding = True
                    generator = pathfind(target_node)
                if event.key == pygame.K_ESCAPE:
                    pathfinding = False
                    current = start_node
                if event.key == pygame.K_r:
                    for node in nodes:
                        node.reset()
                    pathfinding = False
                    start_node, target_node = pick_start_and_target(nodes)
                    current = start_node
                    create_obstacles(nodes)
                    
        draw(nodes)
        pygame.display.update()

if __name__ == "__main__":
    main()