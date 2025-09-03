import pygame, sys
from image import Image

pygame.init()

screen = pygame.display.set_mode((1600,900))


w,h = health.w,health.h
n=0

while True:
    screen.fill((0,0,0))

    
    screen.blit(empty_bar.surface,(0,0))
    screen.blit(health.surface,(19,18), area=(0,0,n/45*w,h))

    #screen.blit(image.scale_by(2).surface,(0,0))
    pygame.display.flip()


    for event in pygame.event.get():
            # Clicking the 'X' of the window ends the game
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    n = max(0,n-1)
                if event.key == pygame.K_RIGHT:
                    n = min(45,n+1)


