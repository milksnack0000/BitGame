import pygame
pygame.init()

import random  

screen  = pygame.display.set_mode((700,700))
snow = []

for i in range(50):
    x = random.randrange(0,700)
    y = random.randrange(0,700)
    snow.append([x,y])



clock = pygame.time.Clock() 

while True:                          
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill('sky blue')
    for ice in range(len(snow)):
        pygame.draw.circle(screen, 'white', snow[ice],2)
        snow[ice][1]+=1  
        if snow[ice][1]>700: 
            snow[ice][1] = random.randrange(-50,-10)
            snow[ice][0] = random.randrange(0,700)
    pygame.display.update()
    clock.tick(40)
