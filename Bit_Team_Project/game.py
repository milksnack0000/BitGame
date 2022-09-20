#플레이어 움직이기
import pygmae
pygame.init()
fps = pygame.time.clock()
x_pos = background.get_size()[0]
y_pos = background.get_size()[1]
to_x = 0
to_y = 0
#체력바
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

screen.blit(healthbar, (5,5))
for health1 in range(healthvalue):
    screen.blit(health, (health1+8,8))
#체력감소(적=enemy)
badrect=pygame.Rect(enemyimg.get_rect())
badrect.top=enemy[1]
badrect.left=enemy[0]
if badrect.(플레이어):
    healthvalue -= random.randint(5,20)
    enemy.pop(index)

play = True
while play:
    deltaTime = fps.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_pos = y_pos - 10
            elif event.key == pygame.KEYDOWN:
                y_pos = y_pos + 10
            elif event.key == pygame.k_RIGHT:
                x_pos = x_pos + 10
            elif event.key == pygame.K_LEET:
                to_x = -1
        if event.type == pygame.KEYUP
            if event.key == pygame.k_UP:
                to_y == 0
            elif event.key == pygame.k_DOWN:
                to_y == 0
            elif event.key == pygame.k_RIGHT:
                 to_x = -1
            elif event.key == pygame.k_LEET:
                 to_x = -1
    x_pos += to_x
    y_pos += to_y
    pygame.quit()
            


