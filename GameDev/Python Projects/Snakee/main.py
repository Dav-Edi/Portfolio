import tkinter as tk

import pygame

from scripts.registration import Registration
from scripts.menu import Menu
from scripts.sql import SQL
from scripts.res import RES


if __name__ == '__main__':
	res = RES()
	sql = SQL()
	root = tk.Tk()
	registration = Registration(root, sql, res)
	root.mainloop()
	username = registration.nickname

	while res.FLAG:
		pygame.init()
		pygame.mixer.init()
		root = tk.Tk()
		menu = Menu(root, sql, username, res)
		if res.MUSIC_ON:
			menu.play_music(res.MENU_MUS)
		root.mainloop()
