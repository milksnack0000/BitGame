import pygame
from pygame.locals import *

pygame.init() #초기화

#화면 설정
screen = pygame.display.set_mode((300, 540))
WHITE = (255, 255, 255)
screen.fill(WHITE)
pygame.display.set_caption("BIT_GAME")

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
        self.rect.center = 150, 270

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


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen.blit(surf, S_rect)

    #플레이어 화면에 보이기
    pygame.draw.rect(screen, (0, 0, 255), player.rect)
    screen.blit(player.surf, player.rect)

    #적 화면에 보이기
    pygame.draw.rect(screen, WHITE, enemy.rect)
    screen.blit(enemy.surf, enemy.rect)
    
    pygame.display.update()

pygame.quit()

 #점수
    point = 0
    font_point = pygame.font.SysFont(None,30)
    text_point = font_pont.render(str(point)),True,(255,0,0)
    background.blit(text_point,(10,10))

    #적을 물리칠때마다 포인트 점수 +5
    point += 5

    #초기화 및 디스플레이 설정

    pygame.init()
    background = pygame.display.set_mode((480,360))
    pygame.display. set_caption("UniverseGame")
