import tkinter as tk
import random
import json
from joker import telefonjoker, joker_50_50, publikumsjoker
from tkinter import messagebox

with open("fragenkatalog.json", "r", encoding="utf-8") as f:
    fragen_datenbank = json.load(f)

geldleiter = [
    "100 €", "200 €", "300 €", "500 €", "1.000 €",
    "2.000 €", "4.000 €", "8.000 €", "16.000 €", "32.000 €",
    "64.000 €", "125.000 €", "250.000 €", "500.000 €", "1.000.000 €"
]

farben = {
    "leicht": "#4CAF50",
    "mittel": "#FFC107",
    "schwer": "#F44336"
}


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#1b1f3b")

        self.container = tk.Frame(root, bg="#1b1f3b")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.fade_step = 0.05

        self.show_start_menu()

    def fade_out_in(self, new_frame_class):
        overlay = tk.Frame(self.container, bg="#1b1f3b")
        overlay.place(relwidth=1, relheight=1)

        new_frame = new_frame_class(self.container, self)
        new_frame.place(relwidth=1, relheight=1)

        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame

        # Overlay sanft wegblenden
        def fade(alpha=1.0):
            if alpha <= 0:
                overlay.destroy()
            else:
                grau = int(27 * alpha)
                color = f"#{grau:02x}{grau:02x}{grau:02x}"
                overlay.config(bg=color)
                self.root.after(30, lambda: fade(alpha - 0.1))

        fade()



    def _switch_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.place_forget()
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, self)
        self.current_frame.place(relwidth=1, relheight=1)
        self._fade_in()

    def _fade_out(self, callback):
        #alten Frame löschen und neuen anzeigen
        old_frame = self.current_frame
        self.current_frame = None  # Wichtig: sofort „löschen“, bevor neuer Frame kommt

        if old_frame:
            old_frame.place_forget()
            old_frame.destroy()

        callback()


    def _fade_in(self, alpha=0.0):
        if alpha >= 1:
            self.root.attributes('-alpha', 1)
        else:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self._fade_in(alpha + self.fade_step))

    def show_start_menu(self):
        self.fade_out_in(StartMenu)

    def show_game(self):
        self.fade_out_in(MillionaireGame)

    def show_end(self, gewonnen, betrag, grund=""):
        self.fade_out_in(lambda parent, app: EndScreen(parent, app, gewonnen, betrag, grund))


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


class MillionaireGame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1b1f3b")
        self.app = app
        self.frage_index = 0
        self.alle_fragen = self.generate_questions()
        self.timer_seconds = 0
        self.timer_id = None

        self.setup_ui()
        self.naechste_frage()

    def generate_questions(self):
        return (
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["leicht"], 5)
        )

    # def setup_ui(self):
    #     self.main_frame = tk.Frame(self, bg="#1b1f3b")
    #     self.main_frame.pack(side="left", fill="both", expand=True)

    #     self.frage_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 22, "bold"),
    #                                 wraplength=900, fg="white", bg="#1b1f3b", justify="center")
    #     self.frage_label.pack(pady=30)

    #     self.buttons_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
    #     self.buttons_frame.pack()

    #     self.buttons = []
    #     for i in range(4):
    #         btn = tk.Button(self.buttons_frame, text="", font=("Segoe UI", 16), width=35, height=2,
    #                         bg="#3a3f78", fg="white", activebackground="#6c63ff", bd=0,
    #                         command=lambda i=i: self.antwort_pruefen(i))
    #         btn.grid(row=i//2, column=i % 2, padx=20, pady=15)
    #         self.buttons.append(btn)

    #     self.timer_label = tk.Label(self.main_frame, text="", font=("Segoe UI", 16, "bold"),
    #                                 bg="#1b1f3b", fg="white")
    #     self.timer_label.pack(pady=20)

    #     #Telefonjoker Button
    #     self.sidebar = tk.Frame(self, width=200, bg="#121428")
    #     self.sidebar.pack(side="right", fill="y")
        
    #     self.joker_frame = tk.Frame(self.sidebar, bg="#121428")
    #     self.joker_frame.pack(pady=10)

    #     self.joker_btn = tk.Button(self.joker_frame, text="📞 Telefonjoker", font=("Segoe UI", 12),
    #                                bg="#2196F3", fg="white", padx=10, pady=5,
    #                                command=self.nutze_telefonjoker, width = 20)
    #     self.joker_btn.pack(pady=5)

    #     #50-50Joker Button
    #     self.joker_btn_5050 = tk.Button(self.joker_frame, text="🧮 50:50 Joker", font=("Segoe UI", 12),
    #                             bg="#9C27B0", fg="white", padx=10, pady=5,
    #                             command=self.nutze_5050_joker, width = 20)
    #     self.joker_btn_5050.pack(pady=5)

    #     #Publikumsjoker Button
    #     self.joker_btn_pub = tk.Button(self.joker_frame, text="📊 Publikumsjoker", font=("Segoe UI", 12),
    #                            bg="#FF9800", fg="white", padx=10, pady=5,
    #                            command=self.nutze_publikumsjoker, width = 20)
    #     self.joker_btn_pub.pack(pady=5)

    #     self.geldleiter_labels = []
    #     for i, betrag in reversed(list(enumerate(geldleiter))):
    #         lbl = tk.Label(self.sidebar, text=f"{i+1}. {betrag}", font=("Segoe UI", 12),
    #                        bg="#121428", fg="white", anchor="w", padx=10)
    #         lbl.pack(fill="x", pady=2)
    #         self.geldleiter_labels.insert(0, lbl)
    def setup_ui(self):
        self.main_frame = tk.Frame(self, bg="#1b1f3b")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        # Fragebereich im "Card"-Stil
        self.frage_rahmen = tk.Frame(self.main_frame, bg="#2c2f4c", bd=4, relief="ridge")
        self.frage_rahmen.pack(pady=30, fill="x")

        self.frage_label = tk.Label(self.frage_rahmen, text="", font=("Segoe UI", 26, "bold"),
                                wraplength=900, fg="white", bg="#2c2f4c", justify="center",
                                padx=20, pady=20)
        self.frage_label.pack(fill="both", expand=True)

        # Antwortbuttons
        self.buttons_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.buttons_frame.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Segoe UI", 16, "bold"),
                width=30,
                height=2,
                bg="#3a3f78",
                fg="white",
                activebackground="#6c63ff",
                activeforeground="white",
                bd=0,
                relief="flat",
                highlightthickness=0,
                command=lambda i=i: self.antwort_pruefen(i)
            )
            btn.grid(row=i//2, column=i % 2, padx=20, pady=15)
            self.buttons.append(btn)

        # Timerbereich mit Balken
        self.timer_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.timer_frame.pack(pady=10)

        self.timer_bar_canvas = tk.Canvas(self.timer_frame, height=20, width=400, bg="#444", bd=0, highlightthickness=0)
        self.timer_bar_canvas.pack()
        self.timer_text = tk.Label(self.timer_frame, text="", font=("Segoe UI", 14, "bold"), fg="white", bg="#1b1f3b")
        self.timer_text.pack(pady=5)

        # Sidebar rechts
        self.sidebar = tk.Frame(self, width=220, bg="#121428")
        self.sidebar.pack(side="right", fill="y", padx=10)

        # Joker-Bereich
        self.joker_frame = tk.LabelFrame(self.sidebar, text="Joker", font=("Segoe UI", 12, "bold"),
                                        bg="#121428", fg="white", bd=2, relief="groove", labelanchor="n")
        self.joker_frame.pack(pady=15, padx=10, fill="x")

        self.joker_btn = tk.Button(self.joker_frame, text="📞 Telefonjoker", font=("Segoe UI", 12),
                                bg="#2196F3", fg="white", padx=10, pady=8,
                                command=self.nutze_telefonjoker)
        self.joker_btn.pack(pady=5, fill="x")

        self.joker_btn_5050 = tk.Button(self.joker_frame, text="➗ 50:50 Joker", font=("Segoe UI", 12),
                                        bg="#9C27B0", fg="white", padx=10, pady=8,
                                        command=self.nutze_5050_joker)
        self.joker_btn_5050.pack(pady=5, fill="x")

        self.joker_btn_pub = tk.Button(self.joker_frame, text="📊 Publikumsjoker", font=("Segoe UI", 12),
                                    bg="#FF9800", fg="white", padx=10, pady=8,
                                    command=self.nutze_publikumsjoker)
        self.joker_btn_pub.pack(pady=5, fill="x")

        # Geldleiter
        geld_frame = tk.LabelFrame(self.sidebar, text="Gewinnstufen", font=("Segoe UI", 12, "bold"),
                                bg="#121428", fg="white", bd=2, relief="groove", labelanchor="n")
        geld_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.geldleiter_labels = []
        for i, betrag in reversed(list(enumerate(geldleiter))):
            lbl = tk.Label(geld_frame, text=f"{i+1}. {betrag}", font=("Segoe UI", 12),
                        bg="#121428", fg="white", anchor="w", padx=10)
            lbl.pack(fill="x", pady=1)
            self.geldleiter_labels.insert(0, lbl)


    def get_schwierigkeit(self):
        if self.frage_index < 5:
            return "leicht"
        elif self.frage_index < 10:
            return "mittel"
        else:
            return "schwer"

    def naechste_frage(self):
        if self.frage_index >= len(self.alle_fragen):
            self.app.show_end(True, geldleiter[-1])
            return

        frage = self.alle_fragen[self.frage_index]
        schwierigkeit = self.get_schwierigkeit()

        self.timer_seconds = {"leicht": 10, "mittel": 20, "schwer": 30}[schwierigkeit]

        self.frage_label.config(
            text=f"Frage {self.frage_index + 1}: {frage['frage']}",
            fg=farben[schwierigkeit]
        )

        # Antworten mischen
        antworten = frage["antworten"][:]
        random.shuffle(antworten)

        # Neue richtige Antwort merken
        frage["gemischte_antworten"] = antworten
        frage["richtig"] = frage["richtig"]  # bleibt gleich, aber prüfen gegen neue Liste

        # Buttons setzen
        for i in range(4):
            self.buttons[i].config(text=antworten[i], state="normal", bg="#3a3f78")


        self.highlight_geldstufe()
        self.update_timer()

    def update_timer(self):
        # if self.timer_seconds <= 5:
        #     self.timer_label.config(fg="red" if self.timer_seconds % 2 == 0 else "white")
        # else:
        #     self.timer_label.config(fg="white")

        # self.timer_label.config(text=f"⏱️ Zeit: {self.timer_seconds}s")
        # if self.timer_seconds > 0:
        #     self.timer_seconds -= 1
        #     self.timer_id = self.after(1000, self.update_timer)
        # else:
        #     self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Zeit abgelaufen!")
        max_time = {"leicht": 10, "mittel": 20, "schwer": 30}[self.get_schwierigkeit()]
        width = int((self.timer_seconds / max_time) * 400)
        color = "#4CAF50" if self.timer_seconds > 10 else "#FFC107" if self.timer_seconds > 5 else "#F44336"

        self.timer_bar_canvas.delete("all")
        self.timer_bar_canvas.create_rectangle(0, 0, width, 20, fill=color, width=0)

        self.timer_text.config(text=f"⏱️ Zeit: {self.timer_seconds}s", fg=color)

        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Zeit abgelaufen!")

    def antwort_pruefen(self, index):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        frage = self.alle_fragen[self.frage_index]
        ausgewaehlt = self.buttons[index].cget("text")
        richtig = frage["richtig"]

        for btn in self.buttons:
            btn.config(state="disabled")

        if ausgewaehlt == richtig:
            self.buttons[index].config(bg="#4CAF50")
            self.after(1000, self.frage_richtig)
        else:
            self.buttons[index].config(bg="#F44336")
            for btn in self.buttons:
                if btn.cget("text") == richtig:
                    btn.config(bg="#4CAF50")
            self.after(1500, lambda: self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Falsche Antwort"))

    def frage_richtig(self):
        self.frage_index += 1
        self.naechste_frage()

    def highlight_geldstufe(self):
        for i, lbl in enumerate(self.geldleiter_labels):
            if i == self.frage_index:
                lbl.config(bg="#FFD700", fg="#000")
            else:
                lbl.config(bg="#121428", fg="white")

    def nutze_telefonjoker(self):
        frage = self.alle_fragen[self.frage_index]
        aktuelle_frage = frage["frage"]
        richtige_antwort = frage["richtig"]
        falsche_antworten = [a for a in frage["antworten"] if a != richtige_antwort]

        ergebnisse = telefonjoker(aktuelle_frage, richtige_antwort, falsche_antworten)

        meldung = "\n".join(
            f"{e['name']} ({e['wissen']} %): Ich denke, es ist '{e['antwort']}'." for e in ergebnisse
        )

        tk.messagebox.showinfo("Telefonjoker", meldung)
        self.joker_btn.config(state="disabled")

    def nutze_5050_joker(self):
        frage = self.alle_fragen[self.frage_index]
        richtige_antwort = frage["richtig"]
        gemischt = frage["gemischte_antworten"]

        falsche = [a for a in gemischt if a != richtige_antwort]
        verbleibend = joker_50_50(richtige_antwort, falsche)

        # Verstecke zwei falsche Buttons
        for btn in self.buttons:
            if btn.cget("text") not in verbleibend:
                btn.config(state="disabled", text="")

        self.joker_btn_5050.config(state="disabled")
    
    def nutze_publikumsjoker(self):
        frage = self.alle_fragen[self.frage_index]
        richtige = frage["richtig"]
        gemischt = frage["gemischte_antworten"]
        falsche = [a for a in gemischt if a != richtige]

        stimmen = publikumsjoker(richtige, falsche)

        # Sortiere nach Stimmen absteigend
        sortiert = sorted(stimmen.items(), key=lambda x: x[1], reverse=True)

        meldung = "\n".join([f"{a}: {s} Stimmen" for a, s in sortiert])
        messagebox.showinfo("📊 Publikumsjoker", f"Das Publikum hat abgestimmt:\n\n{meldung}")

        self.joker_btn_pub.config(state="disabled")


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


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
