import tkinter as tk

class EndScreen(tk.Frame):
    def __init__(self, parent, app, gewonnen, betrag, grund=""):
        super().__init__(parent, bg="#1b1f3b")
        msg = ""
        if gewonnen:
            msg = f"🎉 Herzlichen Glückwunsch!\nDu hast {betrag} gewonnen!"
        else:
            msg = f"❌ Spiel beendet!\nDu hast {betrag} gewonnen."
            if grund:
                msg += f"\n\nGrund: {grund}"

        label = tk.Label(self, text=msg, font=("Segoe UI", 20), bg="#1b1f3b", fg="white", wraplength=800, justify="center")
        label.pack(pady=100)

        button_frame = tk.Frame(self, bg="#1b1f3b")
        button_frame.pack(pady=40)

        quit_btn = tk.Button(button_frame, text="Beenden", font=("Segoe UI", 14),
                             bg="#f44336", fg="white", padx=20, pady=10,
                             command=app.root.quit)
        quit_btn.pack(side="left", padx=20)

        restart_btn = tk.Button(button_frame, text="Neustart", font=("Segoe UI", 14),
                                bg="#4CAF50", fg="white", padx=20, pady=10,
                                command=app.show_start_menu)
        restart_btn.pack(side="left", padx=20)
