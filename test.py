import pygame, sys
import screen

pygame.init()

clock = pygame.time.Clock()

while True:
    
    screen.screen.fill((255,0,0))
    screen.blit_screen_on_display()

    pygame.display.flip()


    for event in pygame.event.get():
            # Clicking the 'X' of the window ends the game
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


