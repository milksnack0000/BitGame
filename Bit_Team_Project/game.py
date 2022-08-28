import pygame

pygame.init()

screen = pygame.display.set_mode((640, 200))
screen.fill(WHITE)
pygame.display.update
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



pygame.quit()