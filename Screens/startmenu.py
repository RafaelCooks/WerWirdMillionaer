import tkinter as tk

class StartMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1b1f3b")
        self.app = app

        title = tk.Label(self, text="💰 Wer wird Millionär 💰", font=("Segoe UI", 42, "bold"),
                         fg="white", bg="#1b1f3b")
        title.pack(pady=120)

        start_button = tk.Button(self, text="Spiel starten", font=("Segoe UI", 20),
                                 bg="#4CAF50", fg="white", padx=30, pady=15,
                                 command=app.show_game)
        start_button.pack()