# importing libraries
import math
import pygame
import random
from pygame.locals import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1400, 700))
pygame.display.set_caption("Thermodynamics")
clock = pygame.time.Clock()


# show text
def show_text(text, x, y, color=(255, 255, 255), size=50):
    font = pygame.font.SysFont('freesans', size)
    textobj = font.render(text, False, color)
    screen.blit(textobj, (x, y))


# particle class
class Particle:

    def __init__(self, x, y, vel, mass, color):
        self.pos = [x, y]
        self.vel = vel
        self.dir = random.randint(0, 359) + random.random()
        self.vector = [self.vel * math.cos(math.radians(self.dir)), self.vel * math.sin(math.radians(self.dir))]
        self.mass = mass
        self.figure = None
        self.color = color

    def draw(self, window):
        self.figure = pygame.draw.circle(window, self.color, self.pos, self.mass)

    def move(self):
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]
        self.dir = math.degrees(math.tan(self.vector[1] / self.vector[0]))
        self.vel = math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)


# global variables
particles = [Particle(random.randint(100, 680), random.randint(100, 680), 5, 10, (0, 255, 0)) for _ in range(10)]

piston_pos = 50
piston_move = False
container = [
    pygame.draw.line(screen, (0, 0, 0), (100, 100), (100, 680), 5),
    pygame.draw.line(screen, (0, 0, 0), (100, 680), (680, 680), 5),
    pygame.draw.line(screen, (0, 0, 0), (680, 100), (680, 680), 5),
    pygame.draw.rect(screen, (255, 0, 0), (100, piston_pos, 580, 50))
]
collisions = []

# main loop
while True:

    # drawing
    screen.fill((0, 0, 0))
    container = [
        pygame.draw.line(screen, (255, 255, 255), (100, 100), (100, 680), 5),
        pygame.draw.line(screen, (255, 255, 255), (100, 680), (680, 680), 5),
        pygame.draw.line(screen, (255, 255, 255), (680, 100), (680, 680), 5),
        pygame.draw.rect(screen, (255, 0, 0), (100, piston_pos, 580, 50))
    ]

    # particle loop
    for particle in particles:

        particle.draw(screen)
        particle.move()

        if particle.figure.colliderect(container[0]):
            particle.vector[0] = abs(particle.vector[0])
        elif particle.figure.colliderect(container[1]):
            particle.vector[1] = -1 * abs(particle.vector[1])
        elif particle.figure.colliderect(container[2]):
            particle.vector[0] = -1 * abs(particle.vector[0])
        elif particle.figure.colliderect(container[3]):
            particle.vector[1] = abs(particle.vector[1])

        for particle2 in particles:
            if (particle.figure != None and particle2.figure != None and
                    particle.figure.colliderect(particle2.figure) and
                    particle != particle2 and
                    [particle, particle2] not in collisions and
                    [particle2, particle] not in collisions):
                if particle.mass == particle2.mass:
                    particle.vector, particle2.vector = particle2.vector, particle.vector
                collisions.append([particle, particle2])

    for collision in collisions:
        if not collision[0].figure.colliderect(collision[1].figure):
            collisions.remove([collision[0], collision[1]])

    # event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        elif event.type == MOUSEBUTTONDOWN:
            piston_move = True

        elif event.type == MOUSEBUTTONUP:
            piston_move = False

        elif event.type == MOUSEMOTION:
            if piston_move:
                piston_pos = event.pos[1]

    # display update
    pygame.display.update()
    clock.tick(30)
