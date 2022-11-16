import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math #적 플레이어 추적

pygame.init() #초기화

#화면 설정
screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen_width = int(screen.get_width())
screen_height = int(screen.get_height())
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
        #체력
        self.current_health = 200
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 2
    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0,255,0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed 
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(screen_width/2 -20,screen_height/2 +10,health_bar_width,6)
        transition_bar = pygame.Rect(health_bar.right,screen_height/2 +10,transition_width,6)
		
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(0, 0, 0),(screen_width/2 -20,screen_height/2 +10,self.health_bar_length,6),1)

player = Player()


#적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__() #여기까지 무시해도 됨

        self.surf = pygame.image.load("enemy.png").convert_alpha() #이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) #투명한 부분 색 선택
        self.rect = self.surf.get_rect()

def colllided():
    #여기에 충돌 시 hp 깎는 걸 만들자.
    #if pygame.sprite.spritecollideany(player, enemies):
        #player.get_damage(1)
    pass

clock = pygame.time.Clock()
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

#실행
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #적 랜덤 생성
        elif event.type == ADDENEMY:
            enemy = Enemy()
            coordinate = 0, 0
            x = random.randint(-320, screen_width + 320)
            y = random.randint(-320, screen_height + 320)

            if -120 < x < screen_width + 120 and -120 < y < screen_height + 120:
                a = x + screen_width, x - screen_width
                b = y + screen_height, y - screen_height
                coordinate = random.choice(a), random.choice(b)
            else: coordinate = x, y

            enemy.rect.center = coordinate
            enemies.add(enemy)
            all_sprites.add(enemy)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.get_health(200)
            if event.key == pygame.K_DOWN:
                player.get_damage(200)

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

    #화면표시
    screen.fill(WHITE)

    #적과 플레이어 화면에 표시
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    enemies.update()
    player.advanced_health()

    pygame.display.update()
    clock.tick(720)
pygame.quit()