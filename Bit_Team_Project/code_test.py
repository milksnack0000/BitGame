import pygame, sys
from random import randint

class Player(pygame.sprite.Sprite):  #player class
	def __init__(self,pos,group): #그룹을 넣으면 self가 그 그룹안에 들어감.
		super().__init__(group)
		self.image = pygame.image.load('player.png').convert_alpha() #player 이미지 띄우게 하는 코드
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()   
		self.speed = 5 #player speed 5로 설정

	def input(self):         #키보드에서 방향키를 눌렀을때 방향키에 따라 Player를 이동시키는 함수
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:   #위쪽 화살표를 눌렀을때
			self.direction.y = -1 #카마라를 y축에서 -1만큼 이동
		elif keys[pygame.K_DOWN]: #아래쪽 화살표를 눌렀을때
			self.direction.y = 1#카메라를 y축에서 1만큼 이동
		else:
			self.direction.y = 0#아무것도 눌러진 것이 없으면 카메라를 y축에서 0만큼 이동

		if keys[pygame.K_RIGHT]:#오른쪽 화살표를 눌렀을때
			self.direction.x = 1#카메라를 x축에서 -1만큼 이동
		elif keys[pygame.K_LEFT]:#왼쪽 화살표를 눌렀을때
			self.direction.x = -1#카메라를 x축의 -1만큼 이동
		else:
			self.direction.x = 0#아무것도 눌러진 것이 없으면 카메라를 x축에서 0만큼 이동

	def update(self):  #카메라 속도와 방향을 키보드를 눌렀을 때의 속도와 방향을 곱한것으로 한다.
		self.input()
		self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):    #카메라를 띠우는 클래스
	def __init__(self):                  
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		# camera offset(offset: 거리차)
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2   #ground의 이미지의 넓이의 크키를 조정
		self.half_h = self.display_surface.get_size()[1] // 2   #ground의 이미지의 높이의 크기를 조정
		
        # ground
		self.ground_surf = pygame.image.load('enemy.png').convert_alpha() #ground 이미지를 띠우게 하는 코드
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

	def center_target_camera(self,target):   
		self.offset.x = target.rect.centerx - self.half_w #카메라를 x축 방향으로 움직이면 카메라에서 이미지크키를 뺀 것으로 한다.
		self.offset.y = target.rect.centery - self.half_h #카메라를 y축 방향으로 움직이면 카메라에서 이미지크기를 뺀 것으로 한다.

	def custom_draw(self,player):
		
		self.center_target_camera(player) #centet_target_carmera에서 player가 동작할수 있도록 하는 코드

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset 
		self.display_surface.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery): #스프라이트가 겹칠 때 y가 높으면 앞에오도록 한 코드
			offset_pos = sprite.rect.topleft - self.offset 
			self.display_surface.blit(sprite.image,offset_pos)

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()


# setup 
camera_group = CameraGroup()
player = Player((640,360),camera_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)