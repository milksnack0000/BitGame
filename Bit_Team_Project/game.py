import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math #적 플레이어 추적
import time #살아남은 시간

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

startTime = time.time() # 시작 시간(살아남은 시간)

#게임오버 화면
def showGameOverScreen():
    font_gameover = pygame.font.SysFont(None, 80) # 게임오버 폰트
    txt_game_over = font_gameover.render('Game Over', True, (255,0,0)) #게임오버 글자

    size_txt_gameover_width = txt_game_over.get_rect().size[0]
    size_txt_gameover_height = txt_game_over.get_rect().size[1]
    x_pos_text = screen_width/2-size_txt_gameover_width/2 #게임 오버 글자 위치
    y_pos_text = screen_height/2-size_txt_gameover_height/2 #게임 오버 글자 위치
    screen.fill(WHITE)
    pygame.time.wait(500)
    screen.blit(txt_game_over, (x_pos_text,y_pos_text-50))
    screen.blit(gamepoint, (x_pos_text,y_pos_text+50))

#게임시작 화면
def startscreen():
    font_gamestart = pygame.font.SysFont(None, 80) # 게임시작 폰트
    txt_game_start = font_gamestart.render('Game Start', True, (255,0,0)) #게임시작 글자

    size_txt_gamestart_width = txt_game_start.get_rect().size[0]
    size_txt_gamestart_height = txt_game_start.get_rect().size[1]
    x_pos_text = screen_width/2-size_txt_gamestart_width/2 #게임 시작 글자 위치
    y_pos_text = screen_height/2-size_txt_gamestart_height/2 #게임 시작 글자 위치
    screen.fill(WHITE)
    screen.blit(txt_game_start, (x_pos_text,y_pos_text))

intro = True #게임시작화면

while running:

    while intro:
        startscreen()

        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            intro = False
        
        pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            print(a) #살아남은 시간 출력

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
    
    #살아남은 시간
    font = pygame.font.SysFont(None, 32)
    a = str(int(time.time() - startTime))
    counting_text = font.render(a, 1, (0,0,0))
    center0 = int(screen.get_rect().midtop[0]), int(screen.get_rect().midtop[1]) + 200
    counting_rect = counting_text.get_rect(center = center0)
    screen.blit(counting_text, counting_rect)
    print(a)

    gamepoint = int(a)

    pressed = pygame.key.get_pressed()

    #게임오버 화면에 표시(스페이스바 누르면)
    if pressed[pygame.K_SPACE] :
        running = False
        gamepoint = font.render(a, 1, (0,0,0))
        showGameOverScreen()
       
    pygame.display.update()


pygame.time.delay(3000) #게임 종료 전 딜레이
pygame.quit()
