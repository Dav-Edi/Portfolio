import sqlite3
from sqlite3 import Error
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class SQL:
    def __init__(self, db_file='../data/scores.db'):
        self.db_file = db_file
        self.conn = self.create_connection(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    @staticmethod
    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def create_table(self):
        """ Create 'users' table if it doesn't exist """
        create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                snake_score INTEGER DEFAULT 0,
                tetris_score INTEGER DEFAULT 0
            )
        """
        try:
            self.cursor.execute(create_users_table_sql)
        except Error as e:
            print(e)

    def save_user(self, username, password):
        """ Save or update user information based on username """
        hashed_password = hash_password(password)

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = self.cursor.fetchone()

        if not existing_user:
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                print("Username already exists. Please choose a different username.")
        else:
            stored_password = existing_user[2]
            if hashed_password == stored_password:
                return True
            else:
                return False

    def update_score(self, username, new_score, game_name):
        if game_name == "Snake":
            self.cursor.execute("SELECT snake_score FROM users WHERE username = ?", (username,))
            score = self.cursor.fetchone()
            if new_score > score[0]:
                self.cursor.execute("UPDATE users SET snake_score = ? WHERE username = ?", (new_score, username))
                self.conn.commit()
        if game_name == "Tetris":
            self.cursor.execute("SELECT tetris_score FROM users WHERE username = ?", (username,))
            score = self.cursor.fetchone()
            if new_score > score[0]:
                self.cursor.execute("UPDATE users SET tetris_score = ? WHERE username = ?", (new_score, username))
                self.conn.commit()

    def get_top_scores(self, game, res, limit=10):
        if game.game_name == "Snake":
            self.cursor.execute("SELECT username, snake_score FROM users ORDER BY snake_score DESC LIMIT ?", (limit,))
        elif game.game_name == "Tetris":
            self.cursor.execute("SELECT username, tetris_score FROM users ORDER BY tetris_score DESC LIMIT ?", (limit,))

        top_scores = self.cursor.fetchall()
        font = game.font
        y = 50
        for rank, (username, score) in enumerate(top_scores, start=1):
            text = f"{rank}. {username}: {score}"
            text_surface = font.render(text, True, res.COLOR2)
            game.best_results_surface.blit(text_surface, (50, y))
            y += 30

        your_result = font.render(f"Your score: {game.score}", True, res.COLOR2)
        game.best_results_surface.blit(your_result, (50, y + 100))
        your_best = font.render(f"Your best: {game.sql.get_your_result(game.username, game.game_name)}", True, res.COLOR2)
        game.best_results_surface.blit(your_best, (50, y + 30))

    def get_your_result(self, username, game_name):
        if game_name == "Snake":
            self.cursor.execute("SELECT username, snake_score FROM users WHERE username = ?",
                                (username,))
        elif game_name == "Tetris":
            self.cursor.execute("SELECT username, tetris_score FROM users WHERE username = ?",
                                (username,))
        result = self.cursor.fetchone()
        return result

    def __del__(self):
        self.conn.close()
