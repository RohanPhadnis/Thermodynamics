import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1200, 780))
pygame.display.set_caption("Electrostatics")


def show_text(text, x, y, color=(255, 255, 255), size=50):
    font = pygame.font.SysFont('freesans', size)
    textobj = font.render(text, False, color)
    screen.blit(textobj, (x, y))


class Button:
    def __init__(self, pos, dim, color, text):
        self.pos = pos
        self.dim = dim
        self.color = color
        self.text = text
        self.figure = None

    def draw(self):
        self.figure = pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.dim[0], self.dim[1]))
        show_text(self.text, self.pos[0] + 10, self.pos[1] + 10, size=20)


class Particle:
    def __init__(self, x, y, s):
        self.pos = [x, y]
        self.figure = None
        self.sign = s
        self.motion = False
        if self.sign == '-':
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)

    def draw(self):
        self.figure = pygame.draw.circle(screen, self.color, self.pos, 10)
        show_text(self.sign, self.pos[0] - 8, self.pos[1] - 18, size=30)

    def move(self, charge_list):
        pass

    def event_handler(self, event):
        if event.type == MOUSEBUTTONDOWN and self.figure.collidepoint(event.pos):
            self.motion = True
        elif event.type == MOUSEBUTTONUP:
            self.motion = False
        elif event.type == MOUSEMOTION and self.motion:
            self.pos = event.pos


charges = []
main_charge = Particle(100, 390, '+')
main_charge.color = (0, 0, 0)

add_pos = Button([900, 50], [150, 50], (255, 0, 0), 'add positive')
add_neg = Button([900, 150], [150, 50], (0, 0, 255), 'add negative')
add_pos.draw()
add_neg.draw()


pygame.draw.line(screen, (0, 0, 0), (800, 0), (780, 780), 4)

while True:
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 780))

    goal = [
        pygame.draw.line(screen, (0, 255, 0), [700, 360], [720, 360], 4),
        pygame.draw.line(screen, (0, 255, 0), [700, 420], [720, 420], 4),
        pygame.draw.line(screen, (0, 255, 0), [720, 360], [720, 420], 4)
    ]

    for charge in charges:
        charge.draw()

    main_charge.draw()

    for event in pygame.event.get():
        for charge in charges:
            charge.event_handler(event)

        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if add_pos.figure.collidepoint(event.pos):
                charges.append(Particle(50, 50, '+'))
            elif add_neg.figure.collidepoint(event.pos):
                charges.append(Particle(50, 50, '-'))

    pygame.display.update()
