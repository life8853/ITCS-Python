import pygame
import random
import sys

window_size = (500, 500)

pygame.init()
main_window = pygame.display.set_mode(window_size)

main_window.fill("white")

for i in range(500):

    rgb_value = random.randint(0, 0xFFFFFFFF)
    color = pygame.color.Color(rgb_value)

    circle_radius = random.randint(10, 20)

    circle_center = (random.randint
                     (circle_radius, window_size[0] - circle_radius),
                     random.randint
                     (circle_radius, window_size[1] - circle_radius))

    pygame.draw.circle(main_window, color, circle_center, circle_radius)


while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT,
                          pygame.KEYDOWN):
            pygame.quit()
            sys.exit()

    pygame.display.flip()
