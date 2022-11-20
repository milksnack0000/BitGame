import pygame
import random
from time import sleep

import pygame
from pygame.locals import *
 
WINDOW_WIDTH = 480
WIDOW_HEIGHT = 640

WHITE = (255, 255, 255)

FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH)
        self.rect.y = WIDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx


        if self.rect.y < 0 or self.rect.y + self.rect.height > WIDOW_HEIGHT:

            self.rect.y -= self.dy


    def draw(self, screen):
        screen.blit(self.image, self.rect)

#미사일


def game_loop():
    player = Player()



    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    player.dx += 5
                elif event.key == pygame.K_UP:
                    player.dy -= 5
                elif event.key == pygame.K_DOWN:
                    player.dy += 5                


            if event.type == pygame.KEYUP:
                if event.key == pygame.KEY_LEFT or event.key == pygame.KEY_RIGHT:
                    player.dx = 0
                elif event.key == pygame.KEY_UP or event.key == pygame.KEY_DOWN:
                    player.dy = 0

        player.update()    
        player.draw(screen)
        pygame.display.flip()
pygame.quit()
