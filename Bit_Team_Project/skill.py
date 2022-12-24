import pygame
import effect

class Using_Skill(pygame.sprite.Group):
    def __init__(self):                  
        super().__init__()

class Skill(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Skill, self).__init__() # 여기까지 무시해도 됨

        self.skill_image = pygame.image.load(image).convert_alpha() # 레벨업 시 스킬 선택 창에 띄울 이미지
        self.skill_image.set_colorkey((255, 255, 255), RLEACCEL) 
        self.skill_image_rect = self.skill_image.get_rect()
        self.skill_level = 1 # 스킬 레벨
        self.skill_damage = 0 # 스킬 데미지
        self.selected_time = 0
        self.cool_time = 0 # 스킬 쿨타임 60=1초
        self.effect_time = 0 # 스킬 이펙트 시간
        self.effect_call = False

        
    # 스킬 공격 범위
    def make_damage_area(self, rectangle, coordinate):
        self.damage_area = pygame.rect.Rect(screen, (0,0,0), rectangle)
        self.damage_area.topleft = coordinate
        area = pygame.sprite.GroupSingle(self.damage_area)
        for i in pygame.sprite.spritecollide(area, enemies):
            get_damage(self.skill_damage)
        all_sprites.remove(self)
    
    # 스킬 이펙트 발생
    def run_effect(self, skill_effect):
        count_tick = 0
        mass = len(skill_effect)
        if count_tick <= self.effect_time:
            pygame.display_surface.blit(skill_effect[count_tick//mass], self.damage_area.center)
            count_tick += 1
        else:
            self.effect_call = False
            count_tick = 0

    # 스킬이 날아가는 모션
    def throwing_skill(self, throwing_object, coordinate):
        self.i = 0
        self.dun = pygame.image.load(throwing_object).convert_alpha()
        self.dun.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.dun.get_rect()
        self.speed = 10
        target = pygame.math.Vector2(round(coordinate))
        dist = target.normalize()
        count = target.x // dist.x * self.speed
        if self.i < count:
            self.rect.topleft += dist * self.speed
            self.i += 1
        else:
            self.effect_call = True
            self.surf = self.make_damage_area(self.rect.topleft)

    # 스킬 전체 구동
    def run_skill(self, skill_effect, throwing_object, coordinate):

        # 2. 스킬 발동 시각(selected_time)을 갱신하면 서 1번이 더 이상 실행 되지 않음.
        # 스킬 이펙트 발생
        if self.effect_call == True:
            self.selected_time = whole_ticks
            self.run_effect(skill_effect)
            self.i = 0

        # 1. 쿨타임이 지나면 날아가는 모션 실행. 목표 지점에 도착하면 데미지 발생
        if whole_ticks >= self.selected_time + self.cool_time:
            all_sprites.add(self)
            self.throwing_skill(throwing_object, coordinate)


# 스킬 생성 예시
#
# 스킬이름 = Skill(스킬 이미지 파일 위치)
# 스킬이름.skill_damage = 10 # 스킬 데미지
# 스킬이름.cool_time = 6000 # 스킬 쿨타임 60=1초
# 스킬이름.effect_time = 120 # 스킬 이펙트 시간
# 
# 
#
#
#
# 메인코드에서 스킬 사용 예시
# 
# 스킬이름.run_skill(스킬 이펙트, 날아가는 폭탄 이미지, 스킬 발동 지점)
#
#
#
#
#