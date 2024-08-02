import pygame
import tkinter as tk

from scripts.snake import SnakeGame
from scripts.tetris import TetrisGame
from scripts.results import ResultsWindow


class Menu:
    def __init__(self, root, sql, username, res):
        self.res = res
        self.sql = sql
        self.username = username
        self.root = root
        self.root.title("Snake Game Menu")
        self.root.configure(background=self.res.COLOR2)
        self.res.center_window(self.root, self.res.WIDTH, self.res.HEIGHT)

        self.play_button = tk.Button(self.root, text="Snake", bg=self.res.COLOR1, command=self.play_snake)
        self.play_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Tetris", bg=self.res.COLOR1, command=self.play_tetris)
        self.play_button.pack(pady=10)

        self.results_button = tk.Button(self.root, text="Results", bg=self.res.COLOR1, command=self.view_results)
        self.results_button.pack(pady=10)

        self.music_button = tk.Button(self.root, text="Turn Music Off", bg=self.res.COLOR1, command=self.toggle_music)
        self.music_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", bg=self.res.COLOR1, fg=res.COLOR2, command=self.quit)
        root.protocol("WM_DELETE_WINDOW", self.quit)
        self.quit_button.pack(pady=10)

    def quit(self):
        self.res.FLAG = False
        self.root.destroy()

    def play_snake(self):
        game = SnakeGame(self, self.res)
        self.stop_music()
        if self.res.MUSIC_ON:
            self.play_music(self.res.SNAKE_MUS)
        self.root.destroy()
        game.run()

    def play_tetris(self):
        game = TetrisGame(self.sql, self.username, self.res)
        self.stop_music()
        if self.res.MUSIC_ON:
            self.play_music(self.res.TETRIS_MUS)
        self.root.destroy()
        game.run()

    def view_results(self):
        ResultsWindow(self.root, self.sql, self.res)

    def toggle_music(self):
        if self.res.MUSIC_ON:
            self.stop_music()
            self.music_button.config(text="Turn Music On")
            self.res.MUSIC_ON = False
        else:
            self.play_music(self.res.MENU_MUS)
            self.music_button.config(text="Turn Music Off")
            self.res.MUSIC_ON = True

    @staticmethod
    def play_music(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()
