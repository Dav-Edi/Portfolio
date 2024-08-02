class RES:
	def __init__(self):
		self.WIDTH: int = 800
		self.HEIGHT: int = 800
		self.FONT1: tuple = ("Arial", 12, "normal")
		self.FONT2: tuple = ("Arial", 14, "bold")
		self.COLOR1: str = "#93b1a7"
		self.COLOR1_rgb: tuple = (147, 177, 167)
		self.COLOR2: str = "#040d12"
		self.FLAG: bool = False
		self.MUSIC_ON: bool = True
		self.SNAKE_MUS: str = "../data/snake.mp3"
		self.TETRIS_MUS: str = "../data/tetris.mp3"
		self.MENU_MUS: str = "../data/menu.mp3"

	def switch_mode(self, color1, color2):
		self.COLOR1 = color1
		self.COLOR2 = color2

	@staticmethod
	def center_window(window, width, height):
		screen_width = window.winfo_screenwidth()
		screen_height = window.winfo_screenheight()

		x = (screen_width // 2) - (width // 2)
		y = (screen_height // 2) - (height // 2)

		window.geometry(f"{width}x{height}+{x}+{y}")
