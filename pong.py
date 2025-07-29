from math import sin, cos, pi
import pygame

class Pong:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.n_left_wins = 0
        self.n_right_wins = 0

        self.scale = 5
        self.width = 80
        self.height = 50
        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale))

        self.new_game()

    def new_game(self):
        self.left = Paddle(1, self.height / 2, 10)
        self.right = Paddle(self.width - 1, self.height / 2, 10)
        self.ball = Ball(self.width / 2, self.height / 2, self.scale, (1, 0))
        self.rightup = False
        self.rightdown = False
        self.leftup = False
        self.leftdown = False
        pygame.display.set_caption(f"{self.n_left_wins} - {self.n_right_wins}")

    def draw_screen(self):
        background_color = (0, 0, 0)
        self.screen.fill(background_color)
        self.right.draw(self.screen, self.scale)
        self.left.draw(self.screen, self.scale)
        self.ball.draw(self.screen, self.scale)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.rightup = True
                if event.key == pygame.K_DOWN:
                    self.rightdown = True
                if event.key == pygame.K_w:
                    self.leftup = True
                if event.key == pygame.K_s:
                    self.leftdown = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.rightup = False
                if event.key == pygame.K_DOWN:
                    self.rightdown = False
                if event.key == pygame.K_w:
                    self.leftup = False
                if event.key == pygame.K_s:
                    self.leftdown = False

    def move(self):
        if self.leftdown and self.left.y + self.left.length < self.height:
            self.left.move(1)
        if self.leftup and self.left.y > 0:
            self.left.move(-1)
        if self.rightdown and self.right.y + self.right.length < self.height:
            self.right.move(1)
        if self.rightup and self.right.y > 0:
            self.right.move(-1)
        self.ball.move()

    def bounce(self):
        if collision(self.left, self.ball):
            angle = calculate_angle(self.left, self.ball)
            self.ball.x = self.left.x + 0.5
            self.ball.bounce_x()
            self.ball.change_direction(- angle)

        if collision(self.right, self.ball):
            angle = calculate_angle(self.right, self.ball)
            self.ball.x = self.right.x - 0.5
            self.ball.bounce_x()
            self.ball.change_direction(angle)

    def check_over(self):
        if self.ball.x < 0:
            self.n_right_wins += 1
            self.new_game()
        if self.ball.x > self.width:
            self.n_left_wins += 1
            self.new_game()

    def check_ceiling(self):
        if self.ball.y <= 0 or self.ball.y >= self.height:
            self.ball.bounce_y()

    def play(self):
        while True:
            self.check_over()
            self.check_ceiling()
            self.events()
            self.move()
            self.bounce()
            self.draw_screen()
            self.clock.tick(40)


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

    def bounce_x(self):
        v0, v1 = self.v
        self.v = - v0, v1

    def bounce_y(self):
        v0, v1 = self.v
        self.v = v0, - v1

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

def collision(paddle:Paddle, ball:Ball):
    x_col = paddle.x - 0.5 <= ball.x <= paddle.x + 0.5
    y_col = paddle.y <= ball.y <= paddle.y + paddle.length
    return x_col and y_col

def calculate_angle(paddle:Paddle, ball:Ball):
    coeff = ball.y - paddle.y - paddle.length / 2
    angle = - coeff * pi / 50
    return angle

def rotation(direction_vector:tuple, theta:float):
    x, y = direction_vector
    c, s = cos(theta), sin(theta)
    new_x = x * c - y * s
    new_y = x * s + y * c
    return new_x, new_y

if __name__ == "__main__":
    pong = Pong()
    pong.play()
