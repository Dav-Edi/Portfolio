import tkinter as tk
from tkinter import ttk
import sqlite3

class ResultsWindow:
	def __init__(self, root, sql, res):
		self.res = res
		self.root = root
		self.sql = sql

		self.results = self.fetch_scores_from_db()

		self.window = tk.Toplevel(root, bg=self.res.COLOR2)
		self.window.title("Arcades/Results")

		self.table_frame = ttk.Frame(self.window)
		self.table_frame.pack(padx=20, pady=20, fill='both', expand=True)

		self.create_table()

	def fetch_scores_from_db(self):
		try:
			self.sql.cursor.execute("SELECT username, snake_score, tetris_score FROM users")
			rows = self.sql.cursor.fetchall()
			return rows
		except sqlite3.Error as e:
			print("Error fetching data:", e)
			return []

	def create_table(self):
		tree = ttk.Treeview(self.table_frame, columns=("Username", "Snake", "Tetris"), show="headings")
		tree.heading("Username", text="Username")
		tree.heading("Snake", text="Snake")
		tree.heading("Tetris", text="Tetris")

		tree.tag_configure("oddrow", background=self.res.COLOR2, foreground=self.res.COLOR1)
		tree.tag_configure("evenrow", background=self.res.COLOR1, foreground=self.res.COLOR2)

		for index, (username, snake_score, tetris_score) in enumerate(self.results, start=1):
			tags = ('oddrow', 'evenrow')[index%2]
			tree.insert("", "end", values=(username, snake_score, tetris_score), tags=tags)

		tree.pack(fill="both", expand=True)
