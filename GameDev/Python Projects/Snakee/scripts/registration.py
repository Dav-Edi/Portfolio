import tkinter as tk
from tkinter import messagebox


class Registration:
    def __init__(self, root, sql, res):
        self.res = res
        self.root = root
        self.sql = sql
        self.root.title("Arcades/Registration")
        self.root.configure(background=self.res.COLOR2)
        self.res.center_window(self.root, self.res.WIDTH, self.res.HEIGHT)

        self.nickname = None
        self.password = None

        self.nickname_label = tk.Label(root, text="Nickname:", font=self.res.FONT1, bg=self.res.COLOR2, fg=self.res.COLOR1)
        self.nickname_label.pack(expand=False, fill="both", padx=20, pady=20)
        self.nickname_entry = tk.Entry(root, width=30, font=self.res.FONT1, fg=self.res.COLOR1, bg=self.res.COLOR2, highlightthickness=2, highlightbackground=self.res.COLOR1)
        self.nickname_entry.pack(expand=False, fill="both", padx=20, pady=20)

        self.password_label = tk.Label(root, text="Password:", font=self.res.FONT1, bg=self.res.COLOR2, fg=self.res.COLOR1)
        self.password_label.pack(expand=False, fill="both", padx=20, pady=20)
        self.password_entry = tk.Entry(root, show="*", width=30, font=self.res.FONT1, bg=self.res.COLOR2, fg=self.res.COLOR1, highlightthickness=2, highlightbackground=self.res.COLOR1)
        self.password_entry.pack(expand=False, fill="both", padx=20, pady=20)

        self.submit_button = tk.Button(root, text="Submit", width=15, height=2, font=self.res.FONT2, bg=self.res.COLOR1, fg="white", bd=0, relief=tk.FLAT, command=self.submit_registration)
        self.submit_button.pack(expand=False, fill="both", padx=20, pady=20)

    def submit_registration(self):
        self.nickname = self.nickname_entry.get()
        self.password = self.password_entry.get()

        if not self.nickname or not self.password:
            messagebox.showerror("Error", "Please enter both nickname and password.")
            return

        if self.sql.save_user(self.nickname, self.password):
            self.res.FLAG = True
            self.root.destroy()
        else:
            messagebox.showinfo("Error", "Wrong password!")
