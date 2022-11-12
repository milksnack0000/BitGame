import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math #적 플레이어 추적

pygame.init() #초기화

#화면 설정
screen_width = 900
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)
pygame.display.set_caption("BIT_GAME")


#플레이어, Sprite 클래스를 바탕으로 만듦
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() #여기까지 무시해도 됨

        self.surf = pygame.image.load("player.png").convert_alpha() #이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) #투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = screen_width/2, screen_height/2

player = Player()


#적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__() #여기까지 무시해도 됨

        self.surf = pygame.image.load("enemy.png").convert_alpha() #이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) #투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        
#적 추가하는 이벤트
second = 250
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, second) #현재 0.25초마다 실행

#스프라이트 그룹
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#적 플레이어 추적

dx, dy = 0,0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            enemy = Enemy()
            #적 랜덤 생성
            coordinate = 0, 0
            x = random.randint(-320, screen_width + 320)
            y = random.randint(-320, screen_height + 320)
            if -120 < x < screen_width + 120 and -120 < y < screen_height + 120:
                a = x + screen_width, x - screen_width
                b = y + screen_height, y - screen_height
                coordinate = random.choice(a), random.choice(b)

            enemy.rect.center = coordinate
            enemies.add(enemy)
            all_sprites.add(enemy)

    #플레이어 위치 업데이트용
    px = player.rect.x
    py = player.rect.y
    for enemy in enemies:
        #플레이어와 적 사이의 direction vector (dx, dy) 찾기
        dx, dy = px - enemy.rect.x, py - enemy.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
    
        # 적이 normalized vector을 따라 플레이어를 향해 이동(속도 조절 가능)
        enemy.rect.x += dx * 1
        enemy.rect.y += dy * 1

    screen.fill(WHITE)

    #적과 플레이어 화면에 표시
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    enemies.update()
    pygame.display.update()

pygame.quit()

import pygame
import sys
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption('BIT_GAME')
SURFACE = pygame.display.set_mode((1000,600))
FPSCLOCK = pygame.time.Clock()
Big_font = pygame.font.SysFont(None, 150)
Small_font = pygame.font.SysFont(None, 40)


def main():
    Score = 0
    Miss = 0
    message_Title = Big_font.render("BIT GAME", True, (255, 0 , 255))  # 게임제목 적기
    message_Score = Small_font.render("Score: {}".format(Score), True, (255, 255, 255))  # 스코어
    message_Miss = Small_font.render("Miss_Point: {}".format(Miss), True, (255, 255, 255))  # 놓친장애물수
    message_caution = Small_font.render("Game instructioin ", True, (255, 255, 0))
    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        SURFACE.blit(message_Title, (250,250))  # 화면상에 제목 표시

        SURFACE.blit(message_caution, (650, 400))  # 화면상에 주의사항 표시

     
        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
