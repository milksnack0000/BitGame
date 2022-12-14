import pygame
from pygame.locals import *
import random # 적 랜덤 생성
import math # 적 플레이어 추적
from effect import *
import time


pygame.init() # 초기화

# 화면 설정
screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen_width = int(screen.get_width())
screen_height = int(screen.get_height())
WHITE = (255, 255, 255)

main_menu = False
menu_command = 0
whole_ticks = 0



pygame.display.set_caption("BIT_GAME")
fontsize = 16
font = pygame.font.Font("malgun.ttf", fontsize)

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
        if len(self.text) >= 19:
            self.text1 = self.text[:19]
            self.text4 = self.text[19:]
            self.text2 = font.render(self.text1, True, (0, 0, 0))
            self.text5 = font.render(self.text4, True, (0, 0, 0))
            screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
            screen.blit(self.text5, (self.button.centerx-64, self.button.centery - fontsize*1.5 + 16))
        else:
            screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
        screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
        screen.blit(self.icon_surf, (self.button.centerx - 190 , self.button.centery - 48))

    def changeColor(self):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
            self.text2 = font.render(self.text, True, (0, 255, 0))
            screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
            if len(self.text) >= 19:
                self.text2 = font.render(self.text1, True, (0, 255, 0))
                self.text5 = font.render(self.text4, True, (0, 255, 0))
                screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
                screen.blit(self.text5, (self.button.centerx-64, self.button.centery - fontsize*1.5 + 16))
            else:
                screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
            screen.blit(self.icon_surf, (self.button.centerx - 190 , self.button.centery - 48))
        else:
            pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
            self.text2 = font.render(self.text, True, (0, 0, 0))
            screen.blit(self.text3, (self.button.centerx-64, self.button.centery - fontsize*1.5 - 16))
            if len(self.text) >= 19:
                self.text2 = font.render(self.text1, True, (0, 0, 0))
                self.text5 = font.render(self.text4, True, (0, 0, 0))
                screen.blit(self.text2, (self.button.centerx-64, self.button.centery - fontsize*1.5))
                screen.blit(self.text5, (self.button.centerx-64, self.button.centery - fontsize*1.5 + 16))
            else:
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
        self.exp_ratio = self.max_exp / self.exp_bar_length
        self.window_closed = False
        self.charge_exp = 0

		# 플레이어 이동
        self.direction = pygame.math.Vector2()
        self.speed = 4

        # 체력
        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 40
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 2
        self.cooldown = False
        self.present_ticks = 0
    
    def pop_window(self):
        self.button1.changeColor()
        self.button2.changeColor()
        self.button3.changeColor()

        if self.button1.check_clicked():
            self.selected_skill.sprites()[0].skill_level_up()
            self.selected_skill.sprites()[0].selected_time = whole_ticks
            self.window_closed = True
            self.mmm = False
            if self.selected_skill.sprites()[0].skill_level == 1:
                self.selected_skill.sprites()[0].chosen = True
            self.selected_skill = []
        
        if self.button2.check_clicked():
            self.selected_skill.sprites()[1].skill_level_up()
            self.selected_skill.sprites()[1].selected_time = whole_ticks
            self.window_closed = True
            self.mmm = False
            if self.selected_skill.sprites()[1].skill_level == 1:
                self.selected_skill.sprites()[1].chosen = True
            self.selected_skill = []

        if self.button3.check_clicked():
            self.selected_skill.sprites()[2].skill_level_up()
            self.selected_skill.sprites()[2].selected_time = whole_ticks
            self.window_closed = True
            self.mmm = False
            if self.selected_skill.sprites()[2].skill_level == 1:
                self.selected_skill.sprites()[2].chosen = True
            self.selected_skill = []

    def get_exp(self,amount):
        self.current_exp += amount
        if self.current_exp >= self.max_exp:
            self.current_exp = 0
            self.level += 1
            self.max_exp = 100 * (self.level/10)


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
        All_Skills.add(self.selected_skill)
        self.mmm = True

    def draw_exp(self):
        #경험치 글씨
        exp_font = pygame.font.SysFont("None", 40, True)
        exp_text = exp_font.render("LV." + str(self.level), True, (90,90,90))

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

        self.scale = (64, 64)
        self.surf = pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha() # 이미지 불러오기
        self.surf = pygame.transform.scale(self.surf, self.scale)
        self.rect = self.surf.get_rect()
        self.enemy_move_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_2.png").convert_alpha(), self.scale)]
        self.enemy_move_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_2.png").convert_alpha(), self.scale)]
        self.enemy_hurt_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_2.png").convert_alpha(), self.scale)]
        self.enemy_hurt_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_2.png").convert_alpha(), self.scale)]

        self.damage_count = 0
        self.death_count = 0        
        self.Walkcount = 0
        self.damage = False
    

        # 적 스텟
        self.health = 200
        self.speed = 2

    def get_damage(self,amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0
        self.damage = True

#거리에 따라서 적이미지 방향판단
    def input(self): 
        if player.rect.centerx >= self.rect.centerx :
            self.left = False
            self.right = True
        if player.rect.centerx < self.rect.centerx :
            self.right = False
            self.left = True

#적이미지 변환
    def update(self):
        
        if self.health <= 0:
            enemies.remove(self)
            Enemy_group.remove(self)
            # mmanager.playsound(hit, 0.05)
            player.charge_exp += 5
            self.surf = pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/enemy_dead.png").convert_alpha(), self.scale)
            self.death_count += 1
            self.health += 1
        elif self.death_count >= 1:
            self.death_count += 1
            if self.death_count == 120:
                self.kill()
        else:
            self.input()

            if self.Walkcount + 1 >= 16:
                    self.Walkcount = 0
            elif self.right:
                self.surf = self.enemy_move_right[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy_hurt_right[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            elif self.left:
                self.surf = self.enemy_move_left[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy_hurt_left[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            else:
                self.surf = self.enemy_move_left[0]
                if self.damage == True:
                    self.surf = self.enemy_hurt_left[0]
                    self.damage_count += 1
                self.Walkcount = 0
            if self.damage_count == 30:
                self.damage = False
                self.damage_count = 0

# 적, Sprite 클래스를 바탕으로 만듦
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy2, self).__init__() # 여기까지 무시해도 됨

        self.scale = (96, 96)
        self.surf = pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha() # 이미지 불러오기
        self.surf = pygame.transform.scale(self.surf, self.scale)
        self.rect = self.surf.get_rect()
        self.enemy2_move_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_2.png").convert_alpha(), self.scale)]
        self.enemy2_move_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_2.png").convert_alpha(), self.scale)]
        self.enemy2_hurt_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_2.png").convert_alpha(), self.scale)]
        self.enemy2_hurt_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_2.png").convert_alpha(), self.scale)]

        self.damage_count = 0
        self.death_count = 0        
        self.Walkcount = 0
        self.damage = False

        # 적 스텟
        self.health = 500
        self.speed = 3

    def get_damage(self,amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0
        self.damage = True

#거리에 따라서 적이미지 방향판단
    def input(self): 
        if player.rect.centerx >= self.rect.centerx :
            self.left = False
            self.right = True
        if player.rect.centerx < self.rect.centerx :
            self.right = False
            self.left = True

#적이미지 변환
    def update(self):
        if self.health <= 0:
            enemies.remove(self)
            Enemy2_group.remove(self)
            # mmanager.playsound(hit, 0.05)
            player.charge_exp += 30
            self.surf = pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/enemy_dead.png").convert_alpha(), self.scale)
            self.death_count += 1
            self.health += 1
        if self.death_count >= 1:
            self.death_count += 1
            if self.death_count == 120:
                self.kill()
        else:
            self.input()
            if self.Walkcount + 1 >= 16:
                    self.Walkcount = 0
            elif self.right:
                self.surf = self.enemy2_move_right[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy2_hurt_right[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            elif self.left:
                self.surf = self.enemy2_move_left[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy2_hurt_left[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            else:
                self.surf = self.enemy2_move_left[0]
                if self.damage == True:
                    self.surf = self.enemy2_hurt_left[0]
                    self.damage_count += 1
                self.Walkcount = 0
            if self.damage_count == 30:
                self.damage = False
                self.damage_count = 0

class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy3, self).__init__() # 여기까지 무시해도 됨

        self.scale = (128, 128)
        self.surf = pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha() # 이미지 불러오기
        self.surf = pygame.transform.scale(self.surf, self.scale)
        self.rect = self.surf.get_rect()
        self.enemy_move_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/right_2.png").convert_alpha(), self.scale)]
        self.enemy_move_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_move/left_2.png").convert_alpha(), self.scale)]
        self.enemy3_hurt_right = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_1.png").convert_alpha(), self.scale), pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_right_2.png").convert_alpha(), self.scale)]
        self.enemy3_hurt_left = [pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_1.png").convert_alpha(), self.scale),pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/hurt_left_2.png").convert_alpha(), self.scale)]

        self.damage_count = 0
        self.death_count = 0        
        self.Walkcount = 0
        self.damage = False

        # 적 스텟
        self.health = 1000
        self.speed = 2

    def get_damage(self,amount):
        if self.health > 0:
            self.health -= amount
        if self.health < 0:
            self.health = 0
        self.damage = True

#거리에 따라서 적이미지 방향판단
    def input(self): 
        if player.rect.centerx >= self.rect.centerx :
            self.left = False
            self.right = True
        if player.rect.centerx < self.rect.centerx :
            self.right = False
            self.left = True

#적이미지 변환
    def update(self):
        
        if self.health <= 0:
            enemies.remove(self)
            Enemy3_group.remove(self)
            # mmanager.playsound(hit, 0.05)
            player.charge_exp += 50
            self.surf = pygame.transform.scale(pygame.image.load("Sprite/Enemy_hurt/enemy_dead.png").convert_alpha(), self.scale)
            self.death_count += 1
            self.health += 1
        if self.death_count >= 1:
            self.death_count += 1
            if self.death_count == 120:
                self.kill()
        else:
            self.input()
            if self.Walkcount + 1 >= 16:
                    self.Walkcount = 0
            elif self.right:
                self.surf = self.enemy_move_right[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy3_hurt_right[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            elif self.left:
                self.surf = self.enemy_move_left[self.Walkcount//8]
                if self.damage == True:
                    self.surf = self.enemy3_hurt_left[self.Walkcount//8]
                    self.damage_count += 1
                self.Walkcount += 1
            else:
                self.surf = self.enemy_move_left[0]
                if self.damage == True:
                    self.surf = self.enemy3_hurt_left[0]
                    self.damage_count += 1
                self.Walkcount = 0
            if self.damage_count == 30:
                self.damage = False
                self.damage_count = 0

def colllided():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    if len(pygame.sprite.spritecollide(player, Enemy_group, False)) > 0 and (player.cooldown == False):
        player.get_damage(50)
        player.player_hit()
def colllided2():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    if len(pygame.sprite.spritecollide(player, Enemy2_group, False)) > 0 and (player.cooldown == False):
        player.get_damage(100)
        player.player_hit()
def colllided3():
    # 여기에 충돌 시 hp 깎는 걸 만들자.
    if len(pygame.sprite.spritecollide(player, Enemy3_group, False)) > 0 and (player.cooldown == False):
        player.get_damage(300)
        player.player_hit()

group0 = pygame.sprite.Group()
hit_cooldown = 60

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

		for sprite in self.sprites():
			if isinstance(sprite, Skill):
				if sprite.floor_skill == True:
					self.remove(sprite)
					group0.add(sprite)
					offset_pos = sprite.rect.topleft - self.offset # 플레이어가 움직인 거리만큼 다른 스프라이트들에게 그 반대방향으로 가게 하는 코드
					self.display_surface.blit(sprite.surf,offset_pos)
					
		# 화면에 띄우기와 카메라 이동
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #스프라이트가 겹칠 때 y가 높으면 앞에오도록 한 코드
			offset_pos = sprite.rect.topleft - self.offset # 플레이어가 움직인 거리만큼 다른 스프라이트들에게 그 반대방향으로 가게 하는 코드
			self.display_surface.blit(sprite.surf,offset_pos)
		for i in group0:
			self.add(i)
			group0.remove(i)

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
		Enemy_group.add(enemy)
		camera_group.add(enemy)
		all_sprites.add(enemy)

def add_enemy2(player):
		enemy2 = Enemy2()
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
		enemy2.rect.center = coordinate
		enemies.add(enemy2)
		Enemy2_group.add(enemy2)
		camera_group.add(enemy2)
		all_sprites.add(enemy2)
def add_enemy3(player):
		enemy3 = Enemy3()
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
		enemy3.rect.center = coordinate
		enemies.add(enemy3)
		Enemy3_group.add(enemy3)
		camera_group.add(enemy3)
		all_sprites.add(enemy3)
Enemy_group = pygame.sprite.Group()
Enemy2_group = pygame.sprite.Group()
Enemy3_group = pygame.sprite.Group()
camera_group = CameraGroup()
player = Player()
camera_group.add(player)
clock = pygame.time.Clock()

# 랜덤 생성 간격 
enemy_term = 120
enemy2_term = 120
enemy3_term = 120


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

        self.skill_level = 0 # 스킬 레벨
        self.skill_damage = 0 # 스킬 데미지
        self.skill_effect = "터지는 이미지 주소"
        self.throwing_object = throwing_object
        self.icon = icon
        self.scale = (32, 32)
        self.effect_scale = (64, 64)
        self.surf = pygame.image.load(self.throwing_object).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, self.scale)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.damage_area = pygame.rect.Rect(100, 100, 100, 100)
        self.speed = 4
        self.stat_health = False
        self.stat_speed = False
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
        self.floor_area = (160, 160)

        # 닿으면 터지는 스킬
        self.touch_skill = False

        # 스킬 설명
        self.all_txt = all_txt
        self.txt = self.all_txt[self.skill_level]
        self.name = ''

    def txt_update(self):
        self.txt = self.all_txt[self.skill_level]

        # 스킬 레벨업
    def skill_level_up(self):
        self.skill_level += 1
        self.txt_update()

        if self.skill_level == 2:
            self.skill_damage += self.skill_damage * (1//5)

        elif self.skill_level == 2 and self.floor_skill == True:
            self.floor_damage += self.floor_damage * (3/10)

        elif self.skill_level == 2 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 2 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 3:
            self.damage_area.width = self.damage_area.width * 13/10
            self.damage_area.width = self.damage_area.height * 13/10

        elif self.skill_level == 3 and self.floor_skill == True:
            self.floor_area += (self.floor_area * 4/10, self.floor_area * 4/10)

        elif self.skill_level == 3 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 3 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 4:
            self.cool_time -= self.cool_time * 8/10

        elif self.skill_level == 4 and self.floor_skill == True:
            self.floor_time += self.floor_time * 1/2 

        elif self.skill_level == 4 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 4 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 5:
            self.skill_damage = self.skill_damage * (3/2)

        elif self.skill_level == 5 and self.floor_skill == True:
            self.floor_damage += self.floor_damage * (4/10)

        elif self.skill_level == 5 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 5 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 6:
            self.speed *= 2
    
        elif self.skill_level == 6 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 6 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 7:
            self.damage_area.width = self.damage_area.width * 3/2
            self.damage_area.width = self.damage_area.height * 3/2

        elif self.skill_level == 7 and self.floor_skill == True:
            self.floor_area += (self.floor_area * 1/2, self.floor_area * 1/2)

        elif self.skill_level == 7 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 7 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 8:
            self.cool_time -= self.cool_time * 7/10

        elif self.skill_level == 8 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 8 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 9:
            self.skill_damage = self.skill_damage * 2

        elif self.skill_level == 9 and self.floor_skill == True:
            self.damage_area.width= self.damage_area.width * 2
            self.damage_area.height = self.damage_area.height * 2

        elif self.skill_level == 9 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100

        elif self.skill_level == 9 and self.stat_speed == True:
            player.speed *= 1.1

        elif self.skill_level == 10:
            self.damage_area = (self.damage_area.width * 2, self.damage_area.height * 2)
            All_Skills.remove(self)

        elif self.skill_level == 10 and self.floor_skill == True:
            self.floor_area += (self.floor_area * 6/10, self.floor_area * 6/10)
            All_Skills.remove(self)

        elif self.skill_level == 10 and self.stat_health == True:
            player.max_health += 100
            player.target_health += 100
            All_Skills.remove(self)

        elif self.skill_level == 10 and self.stat_speed == True:
            player.speed *= 1.1
            All_Skills.remove(self)


    # 스킬 공격 범위
    def make_damage_area(self, coordinate):
        self.damage_area.center = coordinate
        self.rect = self.damage_area
        for i in pygame.sprite.spritecollide(self, enemies, False):
            i.get_damage(self.skill_damage)
    
    def run_floor_deal(self):
        self.rect = self.surf.get_rect()
        self.rect.center = self.set_coord
        for i in pygame.sprite.spritecollide(self, enemies, False):
            i.get_damage(self.floor_damage)

    # 스킬 이펙트 발생
    def run_effect(self):
        self.mass = len(self.skill_effect)
        per_time = self.effect_time / self.mass
        if self.count_tick < self.effect_time:
            self.surf = pygame.image.load(self.skill_effect[int(self.count_tick//per_time)]).convert_alpha()
            pygame.transform.scale(self.surf, self.effect_scale)
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.count_tick += 1
        elif self.floor_skill == True and self.effect_time <= self.count_tick and self.count_tick < (self.floor_time + self.effect_time):
            self.surf = pygame.image.load(self.floor_skill_effect).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, self.floor_area)
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            if (self.count_tick - self.effect_time) % self.floor_time//5 == 0:
                self.run_floor_deal()
            self.count_tick += 1
        else:
            camera_group.remove(self)
            all_sprites.remove(self)
            self.effect_call = False
            self.count_tick = 0
            self.surf = pygame.image.load(self.throwing_object).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, self.scale)
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.center = (screen_width // 2, screen_height // 2)

    # 스킬이 날아가는 모션
    def throwing_skill(self, coordinate):
        self.rect.center = (screen_width // 2 + self.player_offset_x, screen_height // 2 + self.player_offset_y)
        coord = (round(coordinate[0] - (screen_width // 2 )), round(coordinate[1] - (screen_height // 2 )))
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


big_bomb = Skill(big_bomb_icon, skill_throwing_test, skill_txt)
All_Skills.add(big_bomb)
big_bomb.cool_time = 480 # 스킬 쿨타임 60=1초
big_bomb.effect_time = 32 # 스킬 이펙트 시간
big_bomb.skill_effect = big_bomb_effect
big_bomb.skill_damage = 300
big_bomb.damage_area = pygame.rect.Rect(0, 0, 128, 128)
big_bomb.bomb_skill = True
big_bomb.scale = (128, 128)
big_bomb.effect_scale = (128, 128)
big_bomb.surf = pygame.image.load(big_bomb.throwing_object).convert_alpha()
big_bomb.surf = pygame.transform.scale(big_bomb.surf, big_bomb.scale)
big_bomb.name = '빅 봄'

ice_bomb = Skill(ice_bomb_icon, ice_bomb_throw, ice_bomb_txt)
ice_bomb.cool_time = 240 # 스킬 쿨타임 60=1초
ice_bomb.effect_time = 16 # 스킬 이펙트 시간
ice_bomb.skill_effect = big_bomb_effect
ice_bomb.floor_time = 180
ice_bomb.floor_area = (240, 240)
ice_bomb.floor_skill = True
ice_bomb.floor_damage = 40
ice_bomb.floor_skill_effect = ice_bomb_floor
ice_bomb.name = '눈 폭탄'
ice_bomb.floor_area = (160, 160)
All_Skills.add(ice_bomb)


basic_skill = Skill(basic_skill_icon, basic_skill_throw, basic_skill_txt)
basic_skill.name = '요정을 위한 첫 선물'
basic_skill.cool_time = 240
basic_skill.damage_area = pygame.rect.Rect(0, 0, 96, 96)
basic_skill.skill_damage = 200
basic_skill.skill_effect = basic_skill_effect
basic_skill.effect_time = 32
basic_skill.speed = 5
All_Skills.add(basic_skill)
basic_skill.bomb_skill = True
basic_skill.chosen = True
basic_skill.skill_level = 1
basic_skill.txt_update()


health_up = Skill(health_up_icon, dummy_throw_object, health_up_txt)
health_up.stat_health = True
health_up.name = 'hp 증가'
health_up.skill_level = 1
All_Skills.add(health_up)
health_up.txt_update()

speed_up = Skill(speed_up_icon, dummy_throw_object, speed_up_txt)
speed_up.stat_speed = True
speed_up.name = '이동속도 증가'
speed_up.skill_level = 1
All_Skills.add(speed_up)
speed_up.txt_update()

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

#크리스마스 트리 생성/배치
for i in range(2500):
	random_x = random.randint(-9000,9000)
	random_y = random.randint(-9000,9000)
	Tree((random_x,random_y),camera_group)


list_cd1 = [0, 0]
#실행
running = True
while running:
    clock.tick(60)
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    while intro:
        startscreen()
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if pressed[pygame.K_a]:
                intro = False
        pygame.display.update()
    #적 랜덤 생성
    if whole_ticks > 0:
        if (whole_ticks % enemy_term) == 0:
            add_enemy(player)
    if whole_ticks > 3600:
        if (whole_ticks % enemy2_term) == 0:
            add_enemy2(player)
    if whole_ticks > 7200:
        if (whole_ticks % enemy3_term) == 0:    
            add_enemy3(player)

    # 플레이어 쿨다운
    if whole_ticks >= player.present_ticks +  hit_cooldown:
        player.cooldown = False

        
    #플레이어 위치 업데이트용
    px = round(player.rect.centerx)
    py = round(player.rect.centery)
    list_cd = [1000, 0 , 0]


    for i in enemies:
        #플레이어와 적 사이의 direction vector (dx, dy) 찾기
        dx, dy = px - i.rect.centerx, py - i.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.

        # 적이 normalized vector을 따라 플레이어를 향해 이동(속도 조절 가능)
        i.rect.x += round(dx * i.speed)
        i.rect.y += round(dy * i.speed)
        if list_cd[0] > dist:
            list_cd[0] = dist
            if i.rect.x - camera_group.offset.x == 0 or i.rect.y - camera_group.offset.y == 0:
                list_cd[1] = i.rect.centerx - camera_group.offset.x + 1
                list_cd[2] = i.rect.centery - camera_group.offset.y+ 1
            else:
                list_cd[1] = i.rect.centerx - camera_group.offset.x
                list_cd[2] = i.rect.centery - camera_group.offset.y

    if whole_ticks == big_bomb.selected_time + big_bomb.cool_time:
        list_cd1[0] = list_cd[1] 
        list_cd1[1] = list_cd[2] 
    
    colllided()
    colllided2()
    colllided3()

    #화면표시
    screen.fill(WHITE)

    big_bomb.run_skill((list_cd1[0], list_cd1[1]), whole_ticks)
    ice_bomb.run_skill((100, 100), whole_ticks)
    basic_skill.run_skill((list_cd1[0], list_cd1[1]), whole_ticks)

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

    a = str(whole_ticks//60)
    counting_text = font.render(a, 1, (0,0,0))
    center0 = int(screen.get_rect().midtop[0]), int(screen.get_rect().midtop[1]) + 200
    counting_rect = counting_text.get_rect(center = center0)
    screen.blit(counting_text, counting_rect)

    gamepoint = int(a)
    game_over = True

    if player.target_health == 0 :
        running = 0
        gamepoint = font.render(a, 1, (0,0,0))
        showGameOverScreen()

    if player.charge_exp < player.max_exp:
        player.current_exp += player.charge_exp
        player.charge_exp = 0

    if player.charge_exp >= player.max_exp or player.current_exp >= player.max_exp:
        player.level_up()
        player.button1.draw()
        player.button2.draw()
        player.button3.draw()
        while player.mmm:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.mmm = False

                player.pop_window()
                
                if player.charge_exp >= player.max_exp and player.window_closed == True:
                    player.get_exp(player.charge_exp - player.max_exp)
                    player.window_closed = False

                elif player.current_exp >= player.max_exp and player.window_closed == True:
                    player.current_exp = player.current_exp - player.max_exp
                    player.level += 1
                    player.max_exp = 100 * (player.level/10)
                    player.window_closed = False
                    
                elif player.window_closed == True:
                    player.current_exp += player.charge_exp 
                    player.charge_exp = 0
                    player.window_closed = False
                    
            pygame.display.update()
        
    whole_ticks += 1
    pygame.display.update()

pygame.time.delay(3000)
pygame.quit()