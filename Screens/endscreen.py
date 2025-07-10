import tkinter as tk

# Endbildschirm – Wird angezeigt nach Spielende

class EndScreen(tk.Frame):
    def __init__(self, parent, app, gewonnen, betrag, grund=""):   #Konstruktor für den Endbildschirm
        super().__init__(parent, bg="#1b1f3b")  # Hintergrundfarbe wie im Hauptdesign

        # --- Nachricht vorbereiten ---
        msg = ""
        if gewonnen:
            msg = f"🎉 Herzlichen Glückwunsch!\nDu hast {betrag} gewonnen!"
        else:
            msg = f"❌ Spiel beendet!\nDu hast {betrag} gewonnen."
            if grund:
                msg += f"\n\nGrund: {grund}"  # Optionaler Zusatz, falls vorhanden

        # --- Textlabel für Endnachricht ---
        label = tk.Label(
            self,
            text=msg,
            font=("Segoe UI", 20),
            bg="#1b1f3b",
            fg="white",
            wraplength=800,
            justify="center"
        )
        label.pack(pady=100)  # Großer Abstand zum oberen Rand

        # --- Button-Bereich (Beenden & Neustart) ---
        button_frame = tk.Frame(self, bg="#1b1f3b")
        button_frame.pack(pady=40)

        # Button: Spiel beenden (App schließen)
        quit_btn = tk.Button(
            button_frame,
            text="Beenden",
            font=("Segoe UI", 14),
            bg="#f44336",  # Rot
            fg="white",
            padx=20,
            pady=10,
            command=app.root.quit
        )
        quit_btn.pack(side="left", padx=20)

        # Button: Neustart – Zurück zum Startmenü
        restart_btn = tk.Button(
            button_frame,
            text="Neustart",
            font=("Segoe UI", 14),
            bg="#4CAF50",  # Grün
            fg="white",
            padx=20,
            pady=10,
            command=app.show_start_menu
        )
        restart_btn.pack(side="left", padx=20)
