import pygame, sys
from random import randint

class Player(pygame.sprite.Sprite):  #player class
	def __init__(self,pos,group):
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

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2
		# ground
		self.ground_surf = pygame.image.load('ground.png').convert_alpha() #ground 이미지를 띠우게 하는 코드
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		# zoom 
		self.zoom_scale = 1
		self.internal_surf_size = (2500,2500)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def custom_draw(self,player):
		
		self.center_target_camera(player)

		self.internal_surf.fill('#71ddee')

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
		self.internal_surf.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image,offset_pos)

		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

		self.display_surface.blit(scaled_surf,scaled_rect)


pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.event.set_grab(True)

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
