import pygame

pygame.init()

# Global Variables
WIDTH, HEIGHT = 700, 500
BLOCKSIZE = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualizer")
clock = pygame.time.Clock()

class Node:
    nodes = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, BLOCKSIZE, BLOCKSIZE), 1)
    
    @classmethod
    def create_nodes(cls):
        for i in range(0, WIDTH, BLOCKSIZE):
            for j in range(0, HEIGHT, BLOCKSIZE):
                cls.nodes.append(Node(i, j))

        return cls.nodes
    
    def find_neighbours(self):
        for node in Node.nodes:
            # Straight
            if node.x == self.x and node.y == self.y - BLOCKSIZE: # Up
                self.neighbours.append(node)
            elif node.x == self.x and node.y == self.y + BLOCKSIZE: # Down
                self.neighbours.append(node)
            elif node.x == self.x - BLOCKSIZE and node.y == self.y: # Left
                self.neighbours.append(node)
            elif node.x == self.x + BLOCKSIZE and node.y == self.y: # Right
                self.neighbours.append(node)
            
            # Diagonal
            elif node.x == self.x - BLOCKSIZE and node.y == self.y - BLOCKSIZE: # Up Left
                self.neighbours.append(node)
            elif node.x == self.x + BLOCKSIZE and node.y == self.y - BLOCKSIZE: # Up Right
                self.neighbours.append(node)
            elif node.x == self.x - BLOCKSIZE and node.y == self.y + BLOCKSIZE: # Down Left
                self.neighbours.append(node)
            elif node.x == self.x + BLOCKSIZE and node.y == self.y + BLOCKSIZE: # Down Right
                self.neighbours.append(node)

def draw(nodes):
    screen.fill(BLACK)
    for node in nodes:
        node.draw()

def main():
    running = True
    nodes = Node.create_nodes()
    for i, node in enumerate(nodes):
        node.find_neighbours()
        print(len(node.neighbours))
    print("All Neighbours found")

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(nodes)
        pygame.display.update()

if __name__ == "__main__":
    main()