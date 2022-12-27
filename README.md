import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math # 적 플레이어 추적
import time

pygame.init() # 초기화
width , height = 800 , 600
velocity = 7
velocitynalguis = velocity - 2
Enemyes =  []
FPS = 60

# 화면 설정
screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen_width = int(screen.get_width())
screen_height = int(screen.get_height())
WHITE = (255, 255, 255)
pygame.display.set_caption("BIT_GAME")


# 플레이어, Sprite 클래스를 바탕으로 만듦
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() # 여기까지 무시해도 됨

        self.surf = pygame.image.load("player.png").convert_alpha() # 이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = screen_width//2, screen_height//2
        self.cooldown = False
		# 플레이어 이동
        self.direction = pygame.math.Vector2() 
        self.speed = 5 

        # 체력
        self.current_health = 200
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 10
        self.experiance = 0
        self.attacking = True
        self.attack_frame = 0

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

        # 방향지정
    def input(self):         
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:   
	        self.direction.y = -1
        elif keys[pygame.K_DOWN]:
	        self.direction.y = 1
        else:
	        self.direction.y = 0

        if keys[pygame.K_RIGHT]:
	        self.direction.x = 1
        elif keys[pygame.K_LEFT]:
	        self.direction.x = -1
        else:
	        self.direction.x = 0

    def update(self): 
        self.input()
        self.rect.center += self.direction * self.speed

    def attack(self):        
      # If attack frame has reached end of sequence, return to base frame      
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        self.attack_frame += 1

    def player_hit(self):
        if self.cooldown == False:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second
 
            self.target_health = self.target_health - 1
             
            if self.target_health <= 0:
                self.kill()
                pygame.display.update()

# 적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__() # 여기까지 무시해도 됨

        self.surf = pygame.image.load("enemy.png").convert_alpha() # 이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.health = 200
        self.contadordecolisiones = 1
        self.enerandom = random.randint(0,4)
        self.velocity = velocitynalguis

        if self.enerandom == 0:
             self.rect.center = (random.randrange(-130,-30),random.randrange(-130,height+130))
        if self.enerandom == 1:
             self.rect.center = (random.randrange(-130,width+130),random.randrange(-130,-30))
        if self.enerandom == 2:
             self.rect.center = (random.randrange(width+30,width+130),random.randrange(-130,height+130))
        if self.enerandom == 3:
            self.rect.center = (random.randrange(-130,width+130),random.randrange(height+30,height+130))


        
    def get_damage(self,amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0
# 경험치
    def update(self):

        self.pely = enemy.rect.y
        self.pelx = enemy.rect.x
        self.perx = self.rect.x
        self.pery = self.rect.y

        self.dist = math.sqrt(((self.pely-self.pery)**2) + ((self.pelx-self.perx)**2))/velocitynalguis

        self.angle = math.atan2(self.pely-self.pery,self.pelx-self.perx)

        self.speedx = 0
        self.speedy = 0
        self.speedx = math.cos(self.angle) 
        self.speedy = math.sin(self.angle) 
        
        old_rect = self.rect.copy()
        if self.dist>=1:
            self.rect.x += velocitynalguis * self.speedx
            self.rect.y += velocitynalguis * self.speedy

      # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False, pygame.sprite.collide_circle)
        if len(hit) > 1: # at last 1, because the ball hits itself
            if random.randrange(2) == 0:
                self.rect.x = old_rect.x
            else:
                self.rect.y = old_rect.y
            hit = pygame.sprite.spritecollide(self, Enemy_group, False, pygame.sprite.collide_circle)
            if len(hit) > 1:
                    self.rect = old_rect
        if self.health <= 0:
                self.kill()
                pygame.display.update()
      # Activates upon either of the two expressions being true
        if hits and player.attacking == True:
            self.get_damage(5)
            player.experiance += 1   # Release expeiriance
 
      # If collision has occured and player not attacking, call "hit" function            
        elif hits and player.attacking == False:
            player.player_hit()
Enemy_group = pygame.sprite.Group()
def collided():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    if pygame.sprite.spritecollideany(player, enemies):
        player.get_damage(5)
get_damage = ()

# 카메라
class CameraGroup(pygame.sprite.Group):    
	def __init__(self):                  
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		# camera offset(offset: 거리차)
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2   
		self.half_h = self.display_surface.get_size()[1] // 2   
		
        # 땅. 추후 구현 예정
		#self.ground_surf = pygame.image.load('ground.png').convert_alpha() #ground 이미지를 띠우게 하는 코드
		#self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

	# 거리차를 설정한다. 
	# 플레이어가 중앙에서 시작하기에 처음은 (0,0). 플레이어가 오른쪽으로 움직이면 오프셋이 (얼마, 0)로 변함.
	def center_target_camera(self,target):   
		self.offset.x = target.rect.centerx - self.half_w 
		self.offset.y = target.rect.centery - self.half_h 
	
	#스프라이트들을 화면에 띄워주는 함수
	def custom_draw(self,player):
		self.center_target_camera(player)

		# ground 
		#ground_offset = self.ground_rect.topleft - self.offset 
		#self.display_surface.blit(self.ground_surf,ground_offset)

		# 화면에 띄우기와 카메라 이동
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #스프라이트가 겹칠 때 y가 높으면 앞에오도록 한 코드
			offset_pos = sprite.rect.topleft - self.offset # 플레이어가 움직인 거리만큼 다른 스프라이트들에게 그 반대방향으로 가게 하는 코드
			self.display_surface.blit(sprite.surf,offset_pos)

# 적 랜덤 생성
def add_enemy(player):
		enemy = Enemy()
		player_offset_x = player.rect.centerx - screen_width//2
		player_offset_y = player.rect.centery - screen_height//2
		coordinate = 0, 0
		x = random.randint(-320, screen_width + 320)
		y = random.randint(-320, screen_height + 320)

		if -120 < x < screen_width + 120 and -120 < y < screen_height + 120:
			a = x + screen_width, x - screen_width
			b = y + screen_height, y - screen_height
			coordinate = random.choice(a) + player_offset_x, random.choice(b) + player_offset_y
		else: coordinate = x + player_offset_x, y + player_offset_y
		# 좌표에 현재 플레이어의 오프셋을 더해주어 적들이 화면 밖 원래 자리에 생성되도록 수정.
		enemy.rect.center = coordinate
		enemies.add(enemy)
		camera_group.add(enemy)
		all_sprites.add(enemy)

camera_group = CameraGroup()
player = Player()
camera_group.add(player)
clock = pygame.time.Clock()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
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

hit_cooldown = pygame.USEREVENT + 2

#실행
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

requested_enemies = 1

while not running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=True
    
    if len(Enemy_group)<1:
        Enemy=Enemy()
        Enemy_group.add(Enemy)
        all_sprites.add(Enemy)

    hit = pygame.sprite.spritecollide(player, Enemy_group, True, pygame.sprite.collide_circle)
    if hit: 
        requested_balls = min(25, requested_balls+1)
    if len(Enemy_group) < requested_balls:
        Enemy = Enemy()
        if not pygame.sprite.spritecollide(Enemy, Enemy_group, True, pygame.sprite.collide_circle):
            all_sprites.add(Enemy)
            Enemy_group.add(Enemy)
            Enemyes.append(Enemy)
        
    dist=1
                                        
    if len(Enemyes)> len(Enemy_group):
        del Enemyes [0]

while running:
    for event in pygame.event.get():
        if event.type == hit_cooldown:
            player.cooldown = False
        if event.type == pygame.QUIT:
            running = False
            print(a)

        #적 랜덤 생성
        elif event.type == ADDENEMY:
            add_enemy(player)

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
        enemy.rect.x += round(dx * 2)
        enemy.rect.y += round(dy * 2)
    player.player_hit()
    #화면표시
    screen.fill(WHITE)

    collided()

    #적과 플레이어 화면에 표시
    camera_group.update()
    camera_group.custom_draw(player)
    
    enemies.update()
    player.advanced_health()
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
    if player.target_health == 0 :
        running = False
        gamepoint = font.render(a, 1, (0,0,0))
        showGameOverScreen()
    pygame.display.update()
    print(player.rect.center)
    clock.tick(60)

pygame.time.delay(3000)
pygame.quit()
