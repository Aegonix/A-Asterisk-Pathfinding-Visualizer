import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500

BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualizer")
clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)

def main():
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw()
        pygame.display.update()

if __name__ == "__main__":
    main()