import pygame
import random

SCREEN_HEIGHT = 800
GAME_BOARD_WIDTH = 600
BEST_RESULTS_WIDTH = 200
game_board_rect = pygame.Rect(0, 0, 600, 800)
best_results_rect = pygame.Rect(0, 0, 200, 800)

CELL_SIZE = 40
GRID_WIDTH = GAME_BOARD_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 5
SHAPES = [
    [[1, 1, 1, 1]],                  # I-shape
    [[1, 1],
     [1, 1]],                       # O-shape
    [[1, 1, 1],
     [0, 1, 0]],                    # T-shape
    [[1, 1, 1],
     [1, 0, 0]],                    # L-shape
    [[1, 1, 1],
     [0, 0, 1]],                    # J-shape
    [[0, 1, 1],
     [1, 1, 0]],                    # S-shape
    [[1, 1, 0],
     [0, 1, 1]]                     # Z-shape
]


class TetrisGame:
    def __init__(self, sql, username, res):
        self.res = res
        pygame.init()
        self.screen = pygame.display.set_mode((self.res.WIDTH, self.res.HEIGHT))
        self.game_board_surface = pygame.Surface((GAME_BOARD_WIDTH, self.res.HEIGHT))
        self.best_results_surface = pygame.Surface((BEST_RESULTS_WIDTH, self.res.HEIGHT))

        pygame.display.set_caption("Arcades/Tetris")
        self.game_name = "Tetris"
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_piece = None
        self.next_piece = self.get_random_piece()
        self.game_over = False
        self.score = 0
        self.sql = sql
        self.username = username

    def get_random_piece(self):
        shape = random.choice(SHAPES)
        color = self.res.COLOR1
        return Tetromino(shape, color)

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    self.rotate_piece()

    def update(self):
        if self.current_piece is None:
            self.current_piece = self.next_piece
            self.next_piece = self.get_random_piece()
            if not self.current_piece.is_valid(self.board):
                self.game_over = True
                self.sql.update_score(self.username, self.score, self.game_name)

        if not self.game_over:
            if not self.current_piece.move(0, 1, self.board):
                self.board.add_piece(self.current_piece)
                lines_cleared = self.board.clear_lines()
                self.score += lines_cleared * 10
                self.current_piece = None

    def draw(self):
        pygame.draw.rect(self.game_board_surface, self.res.COLOR2, game_board_rect)
        pygame.draw.rect(self.best_results_surface, self.res.COLOR1, best_results_rect)

        self.board.draw(self.game_board_surface)
        if self.current_piece:
            self.current_piece.draw(self.game_board_surface)

        self.sql.get_top_scores(self, self.res)

        self.screen.blit(self.game_board_surface, (0, 0))
        self.screen.blit(self.best_results_surface, (GAME_BOARD_WIDTH, 0))

        pygame.display.flip()

    def move_piece(self, dx, dy):
        if self.current_piece:
            self.current_piece.move(dx, dy, self.board)

    def rotate_piece(self):
        if self.current_piece:
            self.current_piece.rotate(self.board)


class Board:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def add_piece(self, piece):
        for row in range(piece.height):
            for col in range(piece.width):
                if piece.shape[row][col]:
                    self.grid[piece.y + row][piece.x + col] = piece.color

    def clear_lines(self):
        lines_cleared = 0
        for row in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[row]):
                del self.grid[row]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
        return lines_cleared

    def draw(self, screen):
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col]:
                    pygame.draw.rect(screen, self.grid[row][col], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.height = len(shape)
        self.width = len(shape[0])
        self.x = GRID_WIDTH // 2 - self.width // 2
        self.y = 0

    def move(self, dx, dy, board):
        if self.can_move(dx, dy, board):
            self.x += dx
            self.y += dy
            return True
        return False

    def can_move(self, dx, dy, board):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col]:
                    new_x = self.x + col + dx
                    new_y = self.y + row + dy
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT) or board.grid[new_y][new_x]:
                        return False
        return True

    def rotate(self, board):
        rotated_shape = [[self.shape[col][row] for col in range(self.height - 1, -1, -1)] for row in range(self.width)]
        if self.can_rotate(rotated_shape, board):
            self.shape = rotated_shape
            self.height, self.width = self.width, self.height

    def can_rotate(self, rotated_shape, board):
        new_width = len(rotated_shape[0])
        new_height = len(rotated_shape)
        for row in range(new_height):
            for col in range(new_width):
                if rotated_shape[row][col]:
                    new_x = self.x + col
                    new_y = self.y + row
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT) or board.grid[new_y][new_x]:
                        return False
        return True

    def is_valid(self, board):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col]:
                    if not (0 <= self.x + col < GRID_WIDTH and 0 <= self.y + row < GRID_HEIGHT) or board.grid[self.y + row][self.x + col]:
                        return False
        return True

    def draw(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col]:
                    pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE + col * CELL_SIZE, self.y * CELL_SIZE + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
