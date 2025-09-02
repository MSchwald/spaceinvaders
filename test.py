import pygame, sys
from image import Image

pygame.init()



screen = pygame.display.set_mode((1200,800))

while True:
    screen.fill((0,0,0))

    '''health = pygame.image.load("images/Health bar/health.png")
                w,h=health.get_size()
                empty_bar = pygame.image.load("images/Health bar/empty_bar.png")
                screen.blit(empty_bar,(0,0))
                screen.blit(health,(19,18), area=(0,0,5/15*w,h))'''

    image = Image.load('images/ship/a-1.png')

    screen.blit(image.scale_by(2).surface,(0,0))
    pygame.display.flip()






    for event in pygame.event.get():
            # Clicking the 'X' of the window ends the game
            if event.type == pygame.QUIT:
                sys.exit()
