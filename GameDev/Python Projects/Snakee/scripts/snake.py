import pygame
import random
import math

pygame.init()

CELL_SIZE = 20
GAME_BOARD_WIDTH = 600
BEST_RESULTS_WIDTH = 200

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

game_board_rect = pygame.Rect(0, 0, 600, 800)
best_results_rect = pygame.Rect(0, 0, 200, 800)


class SnakeGame:
    def __init__(self, menu, res):
        self.res = res
        self.menu = menu
        self.sql = self.menu.sql
        pygame.init()

        self.screen = pygame.display.set_mode((res.WIDTH, res.HEIGHT))
        pygame.display.set_caption("Arcades/Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.game_name = "Snake"

        self.game_board_surface = pygame.Surface((GAME_BOARD_WIDTH, res.HEIGHT))
        self.best_results_surface = pygame.Surface((BEST_RESULTS_WIDTH, res.HEIGHT))

        self.snake = [(5, 5)]
        self.speed = 10
        self.direction = RIGHT
        self.food = self.generate_food()
        self.food_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)

        self.running = True
        self.score = 0

        self.username = self.menu.username

    def generate_food(self):
        while True:
            x = random.randint(0, GAME_BOARD_WIDTH // CELL_SIZE - 1)
            y = random.randint(0, self.res.HEIGHT // CELL_SIZE - 1)
            if (x, y) not in self.snake:
                return x, y

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.game_board_surface, self.res.COLOR1,
                             (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    @staticmethod
    def get_animated_alpha():
        ticks = pygame.time.get_ticks()
        alpha = 50 + (math.sin(ticks * 0.002) * 0.5 + 0.5) * (255 - 50)
        return int(alpha)

    def draw_food(self):
        alpha = self.get_animated_alpha()
        self.food_surface.fill((self.res.COLOR1_rgb[0], self.res.COLOR1_rgb[1], self.res.COLOR1_rgb[2], alpha))
        self.game_board_surface.blit(self.food_surface,
                                     (self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE))

    def move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= GAME_BOARD_WIDTH // CELL_SIZE or
                new_head[1] < 0 or new_head[1] >= self.res.HEIGHT // CELL_SIZE):
            self.sql.update_score(self.username, self.score, self.game_name)
            self.running = False

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
            if self.score % 3 == 0:
                self.speed += 5
        else:
            self.snake.pop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu.play_music("data/menu.mp3")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def run(self):
        pygame.init()
        while self.running:
            self.clock.tick(self.speed)

            self.handle_events()
            self.move_snake()

            pygame.draw.rect(self.game_board_surface, self.res.COLOR2, game_board_rect)
            pygame.draw.rect(self.best_results_surface, self.res.COLOR1, best_results_rect)

            self.draw_snake()
            self.draw_food()

            self.sql.get_top_scores(self, self.res)

            self.screen.blit(self.game_board_surface, (0, 0))
            self.screen.blit(self.best_results_surface, (GAME_BOARD_WIDTH, 0))

            pygame.display.flip()

        pygame.quit()
