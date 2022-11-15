import pygame
from pygame.locals import *
import random
import pygame, sys

pygame.init()
#화면 설정
screen_width = 300
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))
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
        self.current_health = 200
        self.target_health = 500
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5
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

    def update(self):
		
        self.advanced_health()
		
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
        health_bar = pygame.Rect(10,45,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
		
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(255,255,255),(10,45,self.health_bar_length,25),4)
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


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            enemy = Enemy()
            #적 랜덤 생성
            pos_width = random.choice([random.randint(-320, -120), random.randint(screen_width + 120, screen_width + 320)])
            pos_height = random.choice([random.randint(-320, -120), random.randint(screen_height + 120, screen_height + 320)])
            enemy.rect.center = pos_width, pos_height
            #적 화면에 보이기
            pygame.draw.rect(screen, WHITE, enemy.rect)
            screen.blit(enemy.surf, enemy.rect)

    #screen.blit(surf, S_rect)

    #플레이어 화면에 보이기
    pygame.draw.rect(screen, (0, 0, 255), player.rect)
    screen.blit(player.surf, player.rect)

    pygame.display.update()
pygame.init()
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player())

while True:
	for event in pygame. event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.quit()
			
		# if event.type == pygame.KEYDOWN:
		# 	if event.key == pygame.K_UP:
		# 		player.sprite.get_health(200)
		# 	if event.key == pygame.K_DOWN:
		# 		player.sprite.get_damage(200)

	screen.fill((30,30,30))
	player.draw(screen)
	player.update()
	pygame.display.update()
	clock.tick(60)
pygame.quit()
