import pygame


SIZE = width,height = 800,600

screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))

pygame.init()

# t0 = time.time()
font1 = pygame.font.SysFont(None,30)
# print('time needed for Font Creation : ', time.time() - t0)
img1 = font1.render('HELLO WOLRD! 안녕하세요!',True,(0, 0, 0))
screen.blit(img1, (50,50))



font3 = pygame.font.SysFont('batangbatangchegungsuhgungsuhche',30)
img3 = font3.render('HELLO WOLRD! 안녕하세요!',True,(0, 0, 0))
screen.blit(img3, (50,150))

font4 = pygame.font.SysFont('malgungothicsemilight',20)
img4 = font4.render('HELLO WOLRD! 안녕하세요!',True,(0, 0, 0))
screen.blit(img4, (50,200))

font5 = pygame.font.SysFont('notosanscjkkrblack',50)
img5 = font5.render('HELLO WOLRD! 안녕하세요!',True,(0, 0, 0))
rect5= img5.get_rect()
pygame.draw.rect(img5,(0, 0, 0),rect5,1)
screen.blit(img5, (50,250))

font6 = pygame.font.SysFont('notosansmonocjkkrregular',15)
img6 = font6.render('HELLO WOLRD! 안녕하세요!',True,(0, 0, 0))
screen.blit(img6, (50,350))

pygame.display.update()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()