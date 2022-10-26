import pygame
from pygame.locals import *

import math #적 플레이어 추적

pygame.init() #초기화

#화면 설정
screen = pygame.display.set_mode((300, 540))
WHITE = (255, 255, 255)
pygame.display.set_caption("BIT_GAME")

clock = pygame.time.Clock()

"""surf = pygame.Surface((400, 600))
surf.fill(WHITE)
S_rect = surf.get_rect()""" #맵 제한 테스트용

#플레이어, Sprite 클래스를 바탕으로 만듦
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() #여기까지 무시해도 됨

        self.surf = pygame.image.load("player.png").convert_alpha() #이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) #투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = 150, 280

player = Player()

#적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__() #여기까지 무시해도 됨

        self.surf = pygame.image.load("enemy.png").convert_alpha() #이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) #투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = 50, 270

enemy = Enemy()

#적 플레이어 추적



dx, dy = 0,0

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    #적 플레이어 추적
    px = player.rect.x
    py = player.rect.y
    #플레이어와 적 사이의 direction vector (dx, dy) 찾기
    dx = px - enemy.rect.x
    dy = py - enemy.rect.y
    dist = (math.sqrt(dx**2 + dy**2))
    print(dist)
    if dist != 0:
        dx = dx / dist
        dy = dy / dist  # Normalize.
    print(dx, dy)
    
    # 적이 normalized vector을 따라 플레이어를 향해 이동(속도 조절 가능)
    enemy.rect.x =  enemy.rect.x + dx * 2
    enemy.rect.y =  enemy.rect.y + dy * 2
    print(enemy.rect.x, enemy.rect.y)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player.rect.y = player.rect.y - 10
    
    #플레이어 화면에 보이기
    pygame.draw.rect(screen, (0, 0, 255), player.rect)
    screen.blit(player.surf, player.rect)

    #적 화면에 보이기
    pygame.draw.rect(screen, WHITE, enemy.rect)
    screen.blit(enemy.surf, enemy.rect)
    
    #screen.blit(surf, S_rect)
    
    pygame.display.update()
    

pygame.quit()