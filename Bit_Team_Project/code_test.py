import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math # 적 플레이어 추적
from effect import *

pygame.init() # 초기화

# 화면 설정
screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen_width = int(screen.get_width())
screen_height = int(screen.get_height())
WHITE = (255, 255, 255)
main_menu = False
menu_command = 0
mmm = True
whole_ticks = 0



pygame.display.set_caption("BIT_GAME")
fontsize = 16
font = pygame.font.SysFont("malgungothic", fontsize)

#눈 효과
snow = []
for i in range(50):
    x = random.randrange(0,1700)
    y = random.randrange(0,1700)
    snow.append([x,y])

#크리스마스 트리
class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.surf = pygame.image.load('크리스마스 트리.png').convert_alpha()
		self.rect = self.surf.get_rect(topleft = pos)

class Button:
    def __init__(self, img, txt ,pos, name):
        self.text = str(txt)
        self.name = name
        self.pos = pos
        self.icon = pygame.image.load(img).convert_alpha()
        self.icon_surf = pygame.transform.scale(self.icon, (96, 96))
        self.rect = self.icon.get_rect()
        self.button = pygame.rect.Rect((0, 0), (400, 100))
        self.button.center = (self.pos[0], self.pos[1])

        
    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        self.text2 = font.render(self.text, True, (0, 0, 0))
        self.text3 = font.render(self.name, True, (0, 0, 0))
        screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
        screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
        screen.blit(self.icon_surf, (self.button.centerx - 190 , self.button.centery - 48))

    def changeColor(self):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
            self.text2 = font.render(self.text, True, (0, 255, 0))
            screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
            screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
            screen.blit(self.icon_surf, (self.button.centerx - 190 , self.button.centery - 48))
        else:
            pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
            self.text2 = font.render(self.text, True, (0, 0, 0))
            screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
            screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
            screen.blit(self.icon_surf, (self.button.centerx - 190 , self.button.centery - 48))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


# 플레이어, Sprite 클래스를 바탕으로 만듦
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() # 여기까지 무시해도 됨

        self.santa_move_right = [pygame.image.load("Sprite/Player_move/right_1.png").convert_alpha(), pygame.image.load("Sprite/Player_move/right_2.png").convert_alpha()]
        self.santa_move_left = [pygame.image.load("Sprite/Player_move/left_1.png").convert_alpha(), pygame.image.load("Sprite/Player_move/left_2.png").convert_alpha()]
        self.santa_move_forward = [pygame.image.load("Sprite/Player_move/forward_1.png").convert_alpha(), pygame.image.load("Sprite/Player_move/forward_2.png").convert_alpha()]
        self.santa_move_backward = [pygame.image.load("Sprite/Player_move/backward_1.png").convert_alpha(), pygame.image.load("Sprite/Player_move/backward_2.png").convert_alpha()]
        self.Walkcount = 0

        self.surf = pygame.image.load("Sprite/Player_move/right_1.png").convert_alpha() # 이미지 불러오기
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.rect = self.surf.get_rect()
        self.rect.center = screen_width//2, screen_height//2
        self.place = [(screen_width//2, screen_height//2 + 150), (screen_width//2, screen_height//2+45), (screen_width//2, screen_height//2- 60)]

        # 레벨
        self.level = 1
        self.current_exp = 0
        self.max_exp = 100
        self.exp_bar_length = 500
        self.surplus_exp = 0
        self.exp_ratio = self.max_exp / self.exp_bar_length
        self.level_get = False

		# 플레이어 이동
        self.direction = pygame.math.Vector2()
        self.speed = 3

        # 체력
        self.current_health = 100
        self.target_health = 100
        self.max_health = 100
        self.health_bar_length = 40
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 2
        self.cooldown = False
        self.present_ticks = 0

    def get_exp(self,amount):
        print(self.level)
        self.current_exp += amount
        if self.current_exp >= self.max_exp:
            self.surplus_exp = self.current_exp - self.max_exp
            self.current_exp = 0
            self.level + 1
            self.max_exp = 100 * self.level/10
            self.level_get = True
        if self.surplus_exp >= self.max_exp:
            self.get_exp(self.surplus_exp)
        else:
            self.current_exp += self.surplus_exp 
            self.surplus_exp = 0

    def level_up(self):
        self.selected_skill = pygame.sprite.Group()
        window = pygame.image.load("Skill/window/window.png").convert_alpha()
        window = pygame.transform.scale(window, (560, 640))
        screen.blit(window, (screen_width//2 -280, screen_height//2-320))
        for i in range(3):
            self.len0 = len(All_Skills)
            self.choice = random.choice(list(range(self.len0)))
            self.selected_skill.add(All_Skills.sprites()[self.choice])
            All_Skills.remove(self.selected_skill)
        self.button1 = Button(self.selected_skill.sprites()[0].icon, self.selected_skill.sprites()[0].txt , self.place[0], self.selected_skill.sprites()[0].name)
        self.button2 = Button(self.selected_skill.sprites()[1].icon, self.selected_skill.sprites()[1].txt , self.place[1], self.selected_skill.sprites()[1].name)
        self.button3 = Button(self.selected_skill.sprites()[2].icon, self.selected_skill.sprites()[2].txt , self.place[2], self.selected_skill.sprites()[2].name)

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
        health_bar = pygame.Rect(screen_width/2 -20,screen_height/2 -32,health_bar_width,6)
        transition_bar = pygame.Rect(health_bar.right,screen_height/2 -32,transition_width,6)
		
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(0, 0, 0),(screen_width/2 -20,screen_height/2 -32,self.health_bar_length,6),1)

    def player_hit(self):
        if self.cooldown == False:      
            self.cooldown = True # Enable the cooldown
            self.present_ticks = whole_ticks
            
            if self.target_health <= 0:
                self.kill()

        # 방향지정
    def input(self):         
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:   
            self.direction.y = -1
            self.forward = True
            self.backward = False
            self.left = False
            self.right = False
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.backward = True
            self.forward = False
            self.left = False
            self.right = False
        else:
            self.direction.y = 0
            self.backward = False
            self.forward = False

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.right = True
            self.left = False
            self.forward = False
            self.backward = False
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.left = True
            self.right = False
            self.forward = False
            self.backward = False
        else:
            self.direction.x = 0
            self.right = False
            self.left = False


    def update(self):
        self.input()
        if self.direction.x == 0 or self.direction.y == 0:
            self.rect.center += self.direction * self.speed
        else: 
            self.rect.center += pygame.Vector2.normalize(self.direction)* self.speed
        if self.Walkcount + 1 >= 16:
            self.Walkcount = 0
        elif self.right:
            self.surf = self.santa_move_right[self.Walkcount//8]
            self.Walkcount += 1
        elif self.left:
            self.surf = self.santa_move_left[self.Walkcount//8]
            self.Walkcount += 1
        elif self.forward:
            self.surf = self.santa_move_forward[self.Walkcount//8]
            self.Walkcount += 1
        elif self.backward:
            self.surf = self.santa_move_backward[self.Walkcount//8]
            self.Walkcount += 1
        else:
            self.surf = self.santa_move_right[0]
            self.Walkcount = 0
        self.surf = pygame.transform.scale(self.surf, (64, 64))
            




# 적, Sprite 클래스를 바탕으로 만듦
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__() # 여기까지 무시해도 됨

        self.surf = pygame.image.load("Sprite/enemy.png").convert_alpha() # 이미지 불러오기
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # 투명한 부분 색 선택
        self.surf = pygame.transform.scale(self.surf, (32, 32))
        self.rect = self.surf.get_rect()

        # 적 스텟
        self.health = 200

    def get_damage(self,amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0

    def update(self):
        if self.health <= 0:
            self.kill()
            player.get_exp(100)



def colllided():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    if len(pygame.sprite.spritecollide(player, enemies, False)) > 0 and (player.cooldown == False):
        player.get_damage(10)
        player.player_hit()



hit_cooldown = 600

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
		else: coordinate = round(x + player_offset_x), round(y + player_offset_y)
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
enemy_term = 30

All_Skills = pygame.sprite.Group()
Using_skills = pygame.sprite.Group()

class Skill(pygame.sprite.Sprite):
    def __init__(self, icon, throwing_object, all_txt):
        super(Skill, self).__init__() # 여기까지 무시해도 됨

        self.skill_level = 1 # 스킬 레벨
        self.skill_damage = 0 # 스킬 데미지
        self.skill_effect = "터지는 이미지 주소"
        self.throwing_object = throwing_object
        self.icon = icon
        self.surf = pygame.image.load(self.throwing_object).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (32, 32))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.damage_area = pygame.rect.Rect(100, 100, 100, 100)
        self.speed = 2
        self.stat = False
        self.selected_time = 0
        self.cool_time = 0 # 스킬 쿨타임 60=1초
        self.effect_time = 0 # 스킬 이펙트 시간
        self.effect_call = False
        self.i = 0
        self.count_tick = 0
        self.first_tempt = True
        self.player_offset_x = 0
        self.player_offset_y = 0
        self.chosen = False
        self.bomb_skill = False

        # 장판 딜 관련
        self.floor_skill = False
        self.floor_damage = 1
        self.floor_time = 1
        self.floor_skill_effect = 'd'

        # 스킬 설명
        self.all_txt = all_txt
        self.txt = self.all_txt[self.skill_level - 1]
        self.name = ''

    def txt_update(self):
        self.txt = self.all_txt[self.skill_level - 1]


    # 스킬 공격 범위
    def make_damage_area(self, coordinate):
        self.damage_area.center = coordinate
        self.rect = self.damage_area
        for i in pygame.sprite.spritecollide(self, enemies, False):
            i.get_damage(self.skill_damage)
    
    def run_floor_deal(self, coordinate):
        for i in pygame.sprite.spritecollide(self, enemies, False):
            i.get_damage(self.floor_damage)


    # 스킬 이펙트 발생
    def run_effect(self):
        self.mass = len(self.skill_effect)
        per_time = self.effect_time / self.mass
        if self.count_tick < self.effect_time:
            self.surf = pygame.image.load(self.skill_effect[int(self.count_tick//per_time)]).convert_alpha()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.count_tick += 1
        elif self.floor_skill == True and self.effect_time <= self.count_tick and self.count_tick < (self.floor_time + self.effect_time):
            self.surf = pygame.image.load(self.floor_skill_effect).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (320, 320))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.center = self.set_coord
            if self.count_tick - self.effect_time == self.floor_time // 10:
                self.run_floor_deal(self.set_coord)
            self.count_tick += 1
        else:
            camera_group.remove(self)
            all_sprites.remove(self)
            self.effect_call = False
            self.count_tick = 0
            self.surf = pygame.image.load(self.throwing_object).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (32, 32))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.center = (screen_width // 2, screen_height // 2)

    # 스킬이 날아가는 모션
    def throwing_skill(self, coordinate):
        self.rect.center = (screen_width // 2 + self.player_offset_x, screen_height // 2 + self.player_offset_y)
        coord = (round(coordinate[0]), round(coordinate[1]))
        target = pygame.math.Vector2(coord)
        dist = target.normalize()
        if target.x != 0:
            count = round(target.x // (dist.x * self.speed))
        else:
            count = round(target.y // (dist.y * self.speed))
        if self.i < count:
            self.i += 1
            self.rect.centerx += round(dist.x * self.speed * self.i)
            self.rect.centery += round(dist.y * self.speed * self.i)
            self.set_coord = (self.rect.centerx, self.rect.centery)
        else:
            self.effect_call = True
            if self.bomb_skill == True:
                self.make_damage_area(self.set_coord)
            elif self.floor_skill == True:
                self.rect.center = self.set_coord
                




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

        if whole_ticks >= self.selected_time + self.cool_time and self.chosen == True:
            self.throwing_skill(coordinate)
            camera_group.add(self)




# 폭탄 스킬 생성 예시(던지면 범위에 터지는)
#
# 스킬이름 = Skill(player, 스킬 아이콘 주소, 던지는 이미지 주소, 스킬 설명 리스트 이름)
# All_Skills.add(스킬이름)
# 스킬이름.skill_effect = 스킬 이펙트
# 스킬이름.skill_damage = 10 # 스킬 데미지
# 스킬이름.cool_time = 6000 # 스킬 쿨타임 60=1초
# 스킬이름.effect_time = 120 # 스킬 이펙트 시간
# 스킬이름.damage_area = (0, 0, 너비, 높이)
# 스킬이름.speed = 날아가는 속도
# 스킬이름.bomb_skill = True
#
# 장판 스킬 생성 예시
# 위와 동일
# 스킬이름.floor_time = 장판 스킬 시간        
# self.floor_skill = True
# 스킬이름.floor_damage = 1
# 스킬이름.floor_time = 1
# 스킬이름.floor_skill_effect = 'd'
# 스킬이름.name = '스킬이름'


# 메인코드에서 스킬 사용 예시
# 
# 스킬이름.run_skill(스킬 발동 지점, whole_ticks) 


# test_skill = Skill(test_skill_icon, skill_throwing_test, skill_txt)
# All_Skills.add(test_skill)
# test_skill.cool_time = 300 # 스킬 쿨타임 60=1초
# test_skill.effect_time = 30 # 스킬 이펙트 시간
# test_skill.skill_effect = test_skill_effect
# test_skill.skill_damage = 1000
# test_skill.chosen = True
# test_skill.bomb_skill = True
# test_skill.name = '테스트용 스킬'

# ice_bomb = Skill(ice_bomb_icon, ice_bomb_throw, ice_bomb_txt)
# ice_bomb.cool_time = 60 # 스킬 쿨타임 60=1초
# ice_bomb.effect_time = 30 # 스킬 이펙트 시간
# ice_bomb.skill_effect = test_skill_effect
# ice_bomb.skill_damage = 10
# ice_bomb.floor_time = 180       
# ice_bomb.floor_skill = True
# ice_bomb.floor_damage = 20
# ice_bomb.floor_skill_effect = ice_bomb_floor
# ice_bomb.name = '눈 폭탄'
# All_Skills.add(ice_bomb)
# ice_bomb.chosen = False

# health_up = Skill(health_up_icon, dummy_throw_object, health_up_txt)
# health_up.stat = True
# health_up.name = 'hp 증가'
# All_Skills.add(health_up)


# speed_up = Skill(speed_up_icon, dummy_throw_object, speed_up_txt)
# speed_up.stat = True
# speed_up.name = '이동속도 증가'
# All_Skills.add(speed_up)

#스프라이트 그룹
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

#적 플레이어 추적
dx, dy = 0,0

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
    centerx = int(screen.get_rect().midtop[0])
    screen.blit(gamepoint, (centerx,y_pos_text+50))

#게임시작 화면
def startscreen():
    font_gamestart = pygame.font.SysFont(None, 80) # 게임시작 폰트
    txt_game_start = font_gamestart.render('Game Start', True, (0,0,0)) #게임시작 글자

    size_txt_gamestart_width = txt_game_start.get_rect().size[0]
    size_txt_gamestart_height = txt_game_start.get_rect().size[1]
    x_pos_text = screen_width/2-size_txt_gamestart_width/2 #게임 시작 글자 위치
    y_pos_text = screen_height/2-size_txt_gamestart_height/2 #게임 시작 글자 위치
    screen.fill(WHITE)
    screen.blit(txt_game_start, (x_pos_text,y_pos_text))

intro = True #게임시작화면

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, pos, enemy, screen_rect):
    
        """Take the pos, direction and angle of the player."""
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha() # 이미지 불러오기
        # The `pos` parameter is the center of the bullet.rect.
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)  # The position of the bullet.
        # This Vector points from the mouse pos to the enemy.
        direction = enemy - pos
        # The polar coordinates of the direction Vector.
        radius, angle = direction.as_polar()
        # Rotate the image by the negatiVe angle (because the y-axis is flipped).
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        # The Velocity is the normalized direction Vector scaled to the desired length.
        self.Velocity = direction.normalize() * 11
        self.screen_rect = screen_rect

    def update(self):
        """MoVe the bullet."""
        self.position += self.Velocity  # Update the position Vector.
        self.rect.center = self.position  # And the rect.

        # RemoVe the bullet when it leaVes the screen.
        if not self.screen_rect.contains(self.rect):
            self.kill()


def intercept(position, bullet_speed, enemy, target_Velocity):
    a = target_Velocity.x**2 + target_Velocity.y**2 - bullet_speed**2
    b = 2 * (target_Velocity.x * (enemy.x - position.x) + target_Velocity.y * (enemy.y - position.y))
    c = (enemy.x - position.x)**2 + (enemy.y - position.y)**2

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        print("Target can't be reached.")
        return None
    else:
        t1 = (-b + math.sqrt(discriminant)) / (2*a)
        t2 = (-b - math.sqrt(discriminant)) / (2*a)
        t = max(t1, t2)
        x = target_Velocity.x * t + enemy.x
        y = target_Velocity.y * t + enemy.y
        return pygame.math.Vector2(x, y)


def main():
    pygame.init()
    screen_rect = screen.get_rect()
    bullet_group = pygame.sprite.Group()
    enemy = pygame.math.Vector2(50, 300)
    target_Velocity = pygame.math.Vector2(4, 3)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                target_Vector = intercept(pygame.math.Vector2(event.pos), 11, enemy, target_Velocity)
                # Shoot a bullet. Pass the start position (in this
                # case the mouse position) and the enemy position Vector.
                if target_Vector is not None:  # Shoots only if the enemy can be reached.
                    bullet = Bullet(event.pos, target_Vector, screen_rect)
                    all_sprites.add(bullet)
                    bullet_group.add(bullet)


        all_sprites.update()
        all_sprites.draw(screen)


if __name__ == '__main__':
    main()

#크리스마스 트리 생성/배치
for i in range(2500):
	random_x = random.randint(-9000,9000)
	random_y = random.randint(-9000,9000)
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

    # 플레이어 쿨다운
    if whole_ticks >= player.present_ticks +  hit_cooldown:
        player.cooldown = False

        
    #플레이어 위치 업데이트용
    px = round(player.rect.centerx)
    py = round(player.rect.centery)

    for i in enemies:
        #플레이어와 적 사이의 direction vector (dx, dy) 찾기
        dx, dy = px - i.rect.centerx, py - i.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
    
        # 적이 normalized vector을 따라 플레이어를 향해 이동(속도 조절 가능)
        i.rect.x += round(dx * 2)
        i.rect.y += round(dy * 2)

    colllided()

    #화면표시
    screen.fill(WHITE)

    # test_skill.run_skill((100, -100), whole_ticks)
    # ice_bomb.run_skill((100, 100), whole_ticks)

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

    if player.level_get == True:
        player.level_up()
        player.button1.draw()
        player.button2.draw()
        player.button3.draw()
        while mmm:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mmm = False
                player.button1.changeColor()
                player.button2.changeColor()
                player.button3.changeColor()

                if player.button1.check_clicked():
                    player.selected_skill.sprites()[0].skill_level += 1
                    player.selected_skill.sprites()[0].selected_time = whole_ticks
                    player.selected_skill.sprites()[0].txt_update()
                    if player.selected_skill.sprites()[0].skill_level == 1:
                        player.selected_skill.sprites()[0].chosen = True
                    mmm = False
                if player.button2.check_clicked():
                    player.selected_skill.sprites()[1].skill_level += 1
                    player.selected_skill.sprites()[1].selected_time = whole_ticks
                    player.selected_skill.sprites()[1].txt_update()
                    if player.selected_skill.sprites()[1].skill_level == 1:
                        player.selected_skill.sprites()[1].chosen = True
                    mmm = False
                if player.button3.check_clicked():
                    player.selected_skill.sprites()[2].skill_level += 1
                    player.selected_skill.sprites()[2].selected_time = whole_ticks
                    player.selected_skill.sprites()[2].txt_update()
                    if player.selected_skill.sprites()[2].skill_level == 1:
                        player.selected_skill.sprites()[2].chosen = True
                    mmm = False
            pygame.display.update()
        player.level_get = False
    whole_ticks += 1
    pygame.display.update()

pygame.quit()

LIME = pygame.Color(192, 255, 0)


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, pos, enemy, screen_rect):
        """Take the pos, direction and angle of the player."""
        super().__init__()
        self.image = pygame.Surface((16, 10), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, LIME, ((0, 0), (16, 5), (0, 10)))
        # The `pos` parameter is the center of the bullet.rect.
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)  # The position of the bullet.

        # This Vector points from the mouse pos to the enemy.
        direction = enemy - pos
        # The polar coordinates of the direction Vector.
        radius, angle = direction.as_polar()
        # Rotate the image by the negatiVe angle (because the y-axis is flipped).
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        # The Velocity is the normalized direction Vector scaled to the desired length.
        self.Velocity = direction.normalize() * 11
        self.screen_rect = screen_rect

    def update(self):
        """MoVe the bullet."""
        self.position += self.Velocity  # Update the position Vector.
        self.rect.center = self.position  # And the rect.

        # RemoVe the bullet when it leaVes the screen.
        if not self.screen_rect.contains(self.rect):
            self.kill()


def intercept(position, bullet_speed, enemy, target_Velocity):
    a = target_Velocity.x**2 + target_Velocity.y**2 - bullet_speed**2
    b = 2 * (target_Velocity.x * (enemy.x - position.x) + target_Velocity.y * (enemy.y - position.y))
    c = (enemy.x - position.x)**2 + (enemy.y - position.y)**2

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        print("Target can't be reached.")
        return None
    else:
        t1 = (-b + math.sqrt(discriminant)) / (2*a)
        t2 = (-b - math.sqrt(discriminant)) / (2*a)
        t = max(t1, t2)
        x = target_Velocity.x * t + enemy.x
        y = target_Velocity.y * t + enemy.y
        return pygame.math.Vector2(x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    enemy = pygame.math.Vector2(50, 300)
    target_Velocity = pygame.math.Vector2(4, 3)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                target_Vector = intercept(pygame.math.Vector2(event.pos), 11, enemy, target_Velocity)
                # Shoot a bullet. Pass the start position (in this
                # case the mouse position) and the enemy position Vector.
                if target_Vector is not None:  # Shoots only if the enemy can be reached.
                    bullet = Bullet(event.pos, target_Vector, screen_rect)
                    all_sprites.add(bullet)
                    bullet_group.add(bullet)

        enemy += target_Velocity
        if enemy.x >= screen_rect.right or enemy.x < 0:
            target_Velocity.x *= -1
        if enemy.y >= screen_rect.bottom or enemy.y < 0:
            target_Velocity.y *= -1

        all_sprites.update()
        all_sprites.draw(screen)


if __name__ == '__main__':
    main()