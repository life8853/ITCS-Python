import math
import pygame
import random
import sys

window_size = (500, 500)

pygame.init()
main_window = pygame.display.set_mode(window_size)

main_window.fill("white")

circle_list = []

for i in range(100):
    is_touching = 1

    while is_touching == 1:
        rgb_value = random.randint(0, 0xFFFFFFFF)
        color = pygame.color.Color(rgb_value)

        circle_radius = random.randint(10, 40)

        circle_center = (random.randint
                         (circle_radius, window_size[0] - circle_radius),
                         random.randint
                         (circle_radius, window_size[1] - circle_radius))

        for circle in circle_list:
            x_distance = circle_center[0] - circle[0][0]
            y_distance = circle_center[1] - circle[0][1]
            distance = math.sqrt(pow(x_distance, 2) + pow(y_distance, 2))

            if distance <= circle_radius + circle[1]:
                is_touching = 1
                break
            else:
                is_touching = 0

        if len(circle_list) == 0:
            is_touching = 0

    circle_list.append([circle_center, circle_radius])

    pygame.draw.circle(main_window, color, circle_center, circle_radius)


while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT,
                          pygame.KEYDOWN):
            pygame.quit()
            sys.exit()

    pygame.display.flip()
