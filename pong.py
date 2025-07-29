import pygame

class Pong:
    def __init__(self):
        pygame.init()

        self.scale = 10
        self.width = 40
        self.height = 25
        self.screen = pygame.display.set_mode(
            (self.width * self.scale, self.height * self.scale))

        self.paddle_height = 5
        self.left_paddle_y = self.height / 2 - self.paddle_height / 2
        self.left_paddle_y = int(self.left_paddle_y)

        self.right_paddle_y = self.height / 2 - self.paddle_height / 2
        self.right_paddle_y = int(self.right_paddle_y)

        self.ball_xy = (self.width // 2, self.height // 2)

        screen_color = (0, 0, 0)
        paddle_color = (255, 255, 255)
        ball_color = (255, 10, 10)
        self.colors = {0: screen_color, 1: paddle_color, 2: ball_color}
        self.new_game()

    def new_game(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        paddle_margin = 2
        for i in range(self.paddle_height):
            self.board[self.left_paddle_y + i][paddle_margin] = 1
            self.board[self.right_paddle_y + i][- paddle_margin] = 1
        ball_x, ball_y = self.ball_xy
        self.board[ball_y][ball_x] = 2

    def draw_screen(self):
        s = self.scale
        for y in range(self.height):
            for x in range(self.width):
                obj = self.board[y][x]
                color = self.colors[obj]
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(x * s, y * s, s, s))
        pygame.display.flip()
