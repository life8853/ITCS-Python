import math
import pygame
import sys

BLACK = (0,0,0)
WHITE = (255,255,255)

SCALE_MAIN = 0.90
SCALE_SIDE = 0.37

NUM_OF_LEVELS = 23

# Center Branch
PHI1 = math.radians(9)
PHI2 = math.radians(70)
PHI3 = math.radians(-70)

def drawline(xa, ya, xb, yb, width):
    s1, s2 = (display.centerx+xa, display.height-ya), (display.centerx+xb, display.height-yb)
    pygame.draw.line(window, BLACK, s1, s2, width)

def drawtree(x1, y1, x2, y2, n):
    drawline(x1, y1, x2, y2, n)

    # your code to compute x3,y3,x4,y4
    dx = (x2-x1) * SCALE_MAIN
    dy = (y2-y1) * SCALE_MAIN

    dx_side = (x2-x1) * SCALE_SIDE
    dy_side = (y2-y1) * SCALE_SIDE

    x3 = x2 + dx*math.cos(PHI1) - dy*math.sin(PHI1)
    y3 = y2 + dx*math.sin(PHI1) + dy*math.cos(PHI1)

    x4 = x2 + dx_side*math.cos(PHI2) - dy_side*math.sin(PHI2)
    y4 = y2 + dx_side*math.sin(PHI2) + dy_side*math.cos(PHI2)

    x5 = x2 + dx_side*math.cos(PHI3) - dy_side*math.sin(PHI3)
    y5 = y2 + dx_side*math.sin(PHI3) + dy_side*math.cos(PHI3)

    if n > 1:
        drawtree(x2, y2, x3, y3, n-1)
        drawtree(x2, y2, x4, y4, math.floor(n*0.7))
        drawtree(x2, y2, x5, y5, math.floor(n*0.7))

pygame.init()
window = pygame.display.set_mode((1300,1000))
display = window.get_rect()

window.fill(WHITE)

drawtree(0, 0, 0, 120, NUM_OF_LEVELS)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                sys.exit()