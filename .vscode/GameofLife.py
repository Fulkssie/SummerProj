import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH = 800
HEIGHT = 800
TILESIZE = 20
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE
FPS = 960

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRIDHEIGHT), random.randrange(0, GRIDWIDTH)) for _ in range(num)])

def drawGrid(positions):
    for position in positions:
        col, row = position
        topLeft = (col * TILESIZE, row * TILESIZE)
        pygame.draw.rect(screen, YELLOW, (*topLeft, TILESIZE, TILESIZE))

    for row in range(GRIDHEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILESIZE), (WIDTH, row * TILESIZE))

    for col in range(GRIDWIDTH):
        pygame.draw.line(screen, BLACK, (col * TILESIZE, 0), (col * TILESIZE, HEIGHT))

def adjustGrid(positions):
    allNeighbors = set()
    newPositions = set()

    for position in positions:
        neighbors = getNeighbors(position)
        allNeighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            newPositions.add(position)

    for position in allNeighbors:
        neighbors = getNeighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            newPositions.add(position)
        
    return newPositions

def getNeighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0  or x + dx > GRIDWIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0  or y + dy > GRIDHEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    return neighbors

def main():
    running = True
    playing = False
    generation = 0
    genFrequency = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            generation += 1

        if generation >= genFrequency:
            generation = 0
            positions = adjustGrid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILESIZE
                row = y // TILESIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    generation = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5) * GRIDWIDTH)

        screen.fill(GRAY)
        drawGrid(positions)
        pygame.display.update()
    pygame.quit()

main()