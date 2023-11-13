import pygame
import sys

window_size = (600, 600)

pygame.init()
main_window = pygame.display.set_mode(window_size)

main_window.fill("white")

checkerboard_rows = 8
checkerboard_cols = 8

color = pygame.color.Color("black")

rect_dimensions = (window_size[0]/checkerboard_cols,
                   window_size[1]/checkerboard_rows)

for i in range(checkerboard_rows):
    print(i)
    for j in range(checkerboard_cols):
        if (((i+1) % 2 == 1 and (j+1) % 2 == 0)
           or ((i+1) % 2 == 0 and (j+1) % 2 == 1)):
            rect_origin = (rect_dimensions[0] * j, rect_dimensions[1] * i)
            rect = (rect_origin, rect_dimensions)
            pygame.draw.rect(main_window, color, rect)


while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT,
                          pygame.KEYDOWN):
            pygame.quit()
            sys.exit()

    pygame.display.flip()
