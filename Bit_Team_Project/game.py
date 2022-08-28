import pygame
from pygame.locals import *

pygame.init() #초기화

#화면 설정
screen = pygame.display.set_mode((300, 540))
WHITE = (255, 255, 255)
screen.fill(WHITE)
pygame.display.set_caption("BIT_GAME")


#플레이어
player0 = pygame.image.load("player.png")
#player = pygame.transform.rotozoom(player0, 0, 2) #줌 기능
P_rect = player0.get_rect()
P_rect.center = 150, 270

#적
enemy0 = pygame.image.load("enemy.png")
#enemy = pygame.transform.rotozoom(enemy0, 0, 2)
E_rect = enemy0.get_rect()
E_rect.center = 50, 270


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #플레이어 화면에 보이기
    pygame.draw.rect(screen, (0, 0, 255), P_rect)
    screen.blit(player0, P_rect)

    #적 화면에 보이기
    pygame.draw.rect(screen, WHITE, E_rect)
    screen.blit(enemy0, E_rect)

    pygame.display.update()

pygame.quit()