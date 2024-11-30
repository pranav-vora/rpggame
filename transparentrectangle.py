import pygame
import sys
pygame.init()
screen=pygame.display.set_mode((800,600))
screen.fill((30, 30, 30))

pygame.display.set_caption('transparent rectangle example')
transparent_color = (255, 0, 0, 50)
rect_surface=pygame.Surface((200, 150), pygame.SRCALPHA)
pygame.draw.rect(rect_surface, transparent_color, (0, 0, 200, 255))
pygame.draw.rect(rect_surface, (255,0,0), (0, 0, 0, 255))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color
    screen.fill((30, 30, 30))

    # Blit the transparent surface onto the screen
    screen.blit(rect_surface, (100, 75))
    rectangle=pygame.rect(0,0,10,10)
    # Update the display
    pygame.display.flip()

pygame.quit()