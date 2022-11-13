import pygame
import sys
 
pygame.init()
pygame.display.set_caption("BIT_GAME")
screen_width=400
screen_height=560
screen = pygame.display.set_mode((screen_width, screen_height))
done = False
is_blue = True
x = screen_width* 0.4
y = screen_height * 0.8

clock = pygame.time.Clock()

img = pygame.image.load("player.png")

rect = img.get_rect()


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                        
                rect.left = x
                rect.top = y
 
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP]: y -= 10
                if pressed[pygame.K_DOWN]: y += 10
                if pressed[pygame.K_LEFT]: x -= 10
                if pressed[pygame.K_RIGHT]:  x += 10

                screen.fill((255, 255, 255))        
                screen.blit(img, rect)
                
                pygame.display.flip()
                clock.tick(60)



screen_width = 480
screen_height = 640
shuttle_width = 53
shuttle_height = 111


def startGame():
    global screen, clock, shuttle
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BIT_GAME')
    shuttle = pygame.image.load('player.png')
    clock = pygame.time.Clock()


def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))


def runGame():


    
    x = screen_width * 0.40
    y = screen_height * 0.75
    x_change = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5

        screen.fill((255, 255, 255))

        x += x_change
        if x < 0:
            x = 0
        elif x > screen_width - shuttle_width:
            x = screen_width - shuttle_width
      
        drawObject(shuttle, x, y)

        pygame.display.update()
        clock.tick(60)




def startGame():
    global screen, clock, shuttle, missile

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BIT_GAME')
    shuttle = pygame.image.load('player.png')
    missile = pygame.image.load('New Piskel.png')
    clock = pygame.time.Clock()


def drawObject(obj, x, y):
    global screen
    screen.blit(obj, (x, y))


def runGame():

    
    missile_xy = []

    
    x = screen_width * 0.40
    y = screen_height * 0.75
    x_change = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                elif event.key == pygame.K_SPACE:
                    if len(missile_xy) <2:
                        missile_x = x + shuttle_width/2
                        missile_y = y - shuttle_height/4
                        missile_xy.append([missile_x,missile_y])

           
        screen.fill((255, 255, 255))

      
        x += x_change
        if x < 0:
            x = 0
        elif x > screen_width - shuttle_width:
            x = screen_width - shuttle_width
      
        drawObject(shuttle, x, y)
        
        if len(missile_xy) != 0:
            for i, bxy in enumerate(missile_xy):
                bxy[1] -= 10
                missile_xy[i][1] = bxy[1]

              
                if bxy[1] <= 0:
                    try:
                        missile_xy.remove(bxy)
                    except:
                        pass
        if len(missile_xy) != 0:
            for bx, by in missile_xy:
                drawObject(missile, bx, by)
       
        pygame.display.update()
        clock.tick(60)

startGame()
runGame()
