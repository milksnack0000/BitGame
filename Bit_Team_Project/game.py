import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math # 적 플레이어 추적
from effect import *
import random
from random import randint
pygame.init() # 초기화

#눈 효과
snow = []
for i in range(50):
    x = random.randrange(0,1700)
    y = random.randrange(0,1700)
    snow.append([x,y])
# 화면 설정
screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen_width = int(screen.get_width())
screen_height = int(screen.get_height())
WHITE = (255, 255, 255)

main_menu = False
menu_command = 0
mmm = True
whole_ticks = 0

#크리스마스 트리
class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.surf = pygame.image.load('크리스마스 트리.png').convert_alpha()
		self.rect = self.surf.get_rect(topleft = pos)


pygame.display.set_caption("BIT_GAME")
font = pygame.font.Font('freesansbold.ttf', 24)



class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_menu():
    command = -1
    pygame.draw.rect(screen, 'black', [100, 100, 300, 300])
    pygame.draw.rect(screen, 'green', [100, 100, 300, 300], 5)
    pygame.draw.rect(screen, 'white', [120, 120, 260, 40], 0, 5)
    pygame.draw.rect(screen, 'gray', [120, 120, 260, 40], 5, 5)
    txt = font.render('Menus Tutorial!', True, 'black')
    screen.blit(txt, (135, 127))
    # menu 탈출 버튼
    menu = Button('Exit Menu', (120, 350))
    menu.draw()
    button1 = Button('Button 1', (120, 180))
    button1.draw()
    button2 = Button('Button 2', (120, 240))
    button2.draw()
    button3 = Button('Button 3', (120, 300))
    button3.draw()
    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    if button3.check_clicked():
        command = 3
    return command


def draw_game():
    menu_btn = Button('Main Menu', (230, 450))
    menu_btn.draw()
    menu = menu_btn.check_clicked()
    return menu


# 플레이어, Sprite 클래스를 바탕으로 만듦
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() # 여기까지 무시해도 됨

        self.surf = pygame.image.load("Sprite/player.png").convert_alpha() # 이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = screen_width//2, screen_height//2

        # 레벨
        self.level = 1
        self.current_exp = 50
        self.max_exp = 100 * (1 + self.level/10)
        self.exp_bar_length = 500
        self.surplus_exp = 0
        self.exp_ratio = self.max_exp / self.exp_bar_length

		# 플레이어 이동
        self.direction = pygame.math.Vector2()
        self.speed = 2

        # 체력
        self.current_health = 200
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 2

    def get_exp(self,amount):
        self.current_exp += amount
        if self.current_exp >= self.max_exp:
            self.surplus_exp = self.current_exp - self.max_exp
            self.current_health = 0
            self.level + 1

    def draw_exp(self):
        #경험치 글씨
        exp_font = pygame.font.SysFont("None", 40, True)
        exp_text = exp_font.render("EXP", True, (90,90,90))

        exp_bar_width = int(self.current_exp / self.exp_ratio)
        exp_bar = pygame.Rect(screen_width/2 -250 , 0, exp_bar_width,30)
        exp_bar2 = pygame.Rect(screen_width/2 -250 , 0, self.exp_bar_length,30)
		
        pygame.draw.rect(screen,(255,255,0),exp_bar2)
        pygame.draw.rect(screen,(50,238,254),exp_bar)	
        screen.blit(exp_text, (screen_width/2 -40 , 27))
        pygame.draw.rect(screen,(0, 0, 0),(screen_width/2 -250 , 0, self.exp_bar_length,30),5)
        

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



# 적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__() # 여기까지 무시해도 됨

        self.surf = pygame.image.load("Sprite/enemy.png").convert_alpha() # 이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.rect = self.surf.get_rect()


def colllided():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    #if pygame.sprite.spritecollideany(player, enemies):
        #player.get_damage(1)
    pass


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
# 랜덤 생성 간격 
enemy_term = 250

class Using_Skill(pygame.sprite.Group):
    def __init__(self):                  
        super().__init__()

class Skill(pygame.sprite.Sprite):
    def __init__(self, icon, throwing_object):
        super(Skill, self).__init__() # 여기까지 무시해도 됨

        self.skill_level = 1 # 스킬 레벨
        self.skill_damage = 0 # 스킬 데미지
        self.skill_effect = "터지는 이미지 주소"
        self.throwing_object = throwing_object
        self.icon_surf = pygame.image.load(icon).convert_alpha() # 이미지 불러오기
        self.icon_surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.surf = pygame.image.load(self.throwing_object).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.damage_area = pygame.rect.Rect(100, 100, 100, 100)
        self.selected_time = 180
        self.cool_time = 0 # 스킬 쿨타임 60=1초
        self.effect_time = 0 # 스킬 이펙트 시간
        self.effect_call = False
        self.i = 0
        self.count_tick = 0
        self.first_tempt = True
        self.player_offset_x = 0
        self.player_offset_y = 0
        self.player_offset_x1 = 0
        self.player_offset_y1 = 0
    
    # 스킬 공격 범위
    def make_damage_area(self, coordinate):
        self.damage_area.center = coordinate
        self.rect = self.damage_area
        for i in pygame.sprite.spritecollide(self, enemies, False):
            #get_damage(self.skill_damage)
            pass
        
    # 스킬 이펙트 발생
    def run_effect(self):
        self.mass = len(self.skill_effect)
        per_time = self.effect_time / self.mass
        if self.count_tick < self.effect_time:
            self.surf = pygame.image.load(self.skill_effect[int(self.count_tick//per_time)]).convert_alpha()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.count_tick += 1

        else:
            camera_group.remove(self)
            all_sprites.remove(self)
            self.effect_call = False
            self.count_tick = 0
            self.surf = pygame.image.load(self.throwing_object).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (100, 100))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.center = (screen_width // 2, screen_height // 2)

    # 스킬이 날아가는 모션
    def throwing_skill(self, coordinate):
        self.rect.center = (screen_width // 2 + self.player_offset_x, screen_height // 2 + self.player_offset_y)
        self.speed = 0.5
        coord = (round(coordinate[0]), round(coordinate[1]))
        target = pygame.math.Vector2(coord)
        dist = target.normalize()
        count = round(target.x // (dist.x * self.speed))
        if self.i < count:
            self.i += 1
            self.rect.centerx += round(dist.x * self.speed * self.i)
            self.rect.centery += round(dist.y * self.speed * self.i)
        else:
            self.effect_call = True
            self.make_damage_area((self.rect.centerx + round(dist.x * self.speed * self.i), self.rect.centery + round(dist.y * self.speed * self.i)))

    # 스킬 전체 구동
    def run_skill(self, coordinate, whole_ticks):

        # 2. 스킬 발동 시각(selected_time)을 갱신하면서 1번이 더 이상 실행 되지 않음.
        # 스킬 이펙트 발생
        if self.effect_call == True:
            self.selected_time = whole_ticks
            self.run_effect()
            self.i = 0
            self.first_tempt = True

        # 1. 쿨타임이 지나면 날아가는 모션 실행. 목표 지점에 도착하면 데미지 발생
        if whole_ticks >= self.selected_time + self.cool_time and self.first_tempt == True:
            self.first_tempt = False
            self.player_offset_x = player.rect.centerx - screen_width//2
            self.player_offset_y = player.rect.centery - screen_height//2
        if whole_ticks >= self.selected_time + self.cool_time:
            self.throwing_skill(coordinate)
            camera_group.add(self)
        
            


# 스킬 생성 예시
#
# 스킬이름 = Skill(player, 스킬 아이콘 주소, 던지는 이미지 주소)
# 스킬이름.skill_effect = 스킬 이펙트
# 스킬이름.skill_damage = 10 # 스킬 데미지
# 스킬이름.cool_time = 6000 # 스킬 쿨타임 60=1초
# 스킬이름.effect_time = 120 # 스킬 이펙트 시간
# 스킬이름.damage_area = (0, 0, 너비, 높이)
# 스킬이름.damage = 10
#
# 메인코드에서 스킬 사용 예시
# 
# 스킬이름.run_skill(스킬 발동 지점, whole_ticks)
# 

test_skill = Skill(test_skill_icon, skill_throwing_test)
test_skill.cool_time = 300 # 스킬 쿨타임 60=1초
test_skill.effect_time = 30 # 스킬 이펙트 시간
test_skill.skill_effect = test_skill_effect


#스프라이트 그룹
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#적 플레이어 추적
dx, dy = 0,0
#크리스마스 트리 생성/배치
for i in range(2500):
	random_x = randint(-9000,9000)
	random_y = randint(-9000,9000)
	Tree((random_x,random_y),camera_group)

#실행
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #적 랜덤 생성
    if (whole_ticks % enemy_term) == 0:
        add_enemy(player)
        
    #플레이어 위치 업데이트용
    px = player.rect.x
    py = player.rect.y

    for enemy in enemies:
        #플레이어와 적 사이의 direction vector (dx, dy) 찾기
        dx, dy = px - enemy.rect.centerx, py - enemy.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
    
        # 적이 normalized vector을 따라 플레이어를 향해 이동(속도 조절 가능)
        enemy.rect.x += round(dx * 1)
        enemy.rect.y += round(dy * 1)

    #화면표시
    screen.fill(WHITE)
    

    test_skill.run_skill((100, -100), whole_ticks)

    #적과 플레이어 화면에 표시
    camera_group.update()
    camera_group.custom_draw(player)
    #눈 효과 생성
    for ice in range(len(snow)):
        pygame.draw.circle(screen, 'sky blue', snow[ice],3)
        snow[ice][1]+=1  
        if snow[ice][1]>1700: 
            snow[ice][1] = random.randrange(-550,-10)
            snow[ice][0] = random.randrange(0,1700)

    player.advanced_health()
    player.draw_exp()
    
    while mmm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mmm = False
        if main_menu:
            menu_command = draw_menu()
            if menu_command != -1:
                main_menu = False
        else:
            main_menu = draw_game()
            if menu_command > 0:
                text = font.render(f'Button {menu_command} pressed!', True, 'black')
                screen.blit(text, (150, 100))
                mmm = False
        pygame.display.update()

    
    pygame.display.update()
    whole_ticks += 1
    
    
pygame.quit()
