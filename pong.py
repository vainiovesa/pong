from math import sin, cos, pi
import pygame

class Pong:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.n_left_wins = 0
        self.n_right_wins = 0

        self.scale = 10
        self.width = 40
        self.height = 25
        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale))

        self.new_game()

    def new_game(self):
        self.left = Paddle(1, 0, 5)
        self.right = Paddle(self.width - 1, 0, 5)
        self.ball = Ball(self.width / 2, self.height / 2, self.scale, (1, 0))
        pygame.display.set_caption(f"Left {self.n_left_wins} - Right {self.n_right_wins}")

    def draw_screen(self):
        background_color = (0, 0, 0)
        self.screen.fill(background_color)
        self.right.draw(self.screen, self.scale)
        self.left.draw(self.screen, self.scale)
        self.ball.draw(self.screen, self.scale)
        pygame.display.flip()

    def events(self):
        leftmove, rightmove = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rightmove -= 1
                if event.key == pygame.K_DOWN:
                    rightmove += 1
                if event.key == pygame.K_w:
                    leftmove -= 1
                if event.key == pygame.K_s:
                    leftmove += 1
        return leftmove, rightmove

    def move(self, leftmove, rightmove):
        self.left.move(leftmove)
        self.right.move(rightmove)
        self.ball.move()

    def play(self):
        while True:
            leftmove, rightmove = self.events()
            self.move(leftmove, rightmove)
            self.draw_screen()
            self.clock.tick(30)


class Ball:
    def __init__(self, x:float, y:float, r:int, v:tuple):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = (255, 10, 10)

    def move(self):
        v0, v1 = self.v
        self.x += v0
        self.y += v1

    def change_direction(self, angle:float):
        self.v = rotation(self.v, angle)

    def draw(self, screen, scale):
        pygame.draw.circle(screen, self.color, (self.x * scale, self.y * scale), self.r)

class Paddle:
    def __init__(self, x:float, y:float, length:int):
        self.x = x
        self.y = y
        self.length = length
        self.color = (255, 255, 255)

    def move(self, y):
        self.y += y

    def draw(self, screen, scale):
        x, y, l, s = self.x, self.y, self.length, scale
        x, y, l = x * s, y * s, l * s
        pygame.draw.rect(screen, self.color, pygame.Rect(x - (s / 2), y, s, l))

def rotation(direction_vector:tuple, theta:float):
    x, y = direction_vector
    c, s = cos(theta), sin(theta)
    new_x = x * c - y * s
    new_y = x * s + y * c
    return new_x, new_y
