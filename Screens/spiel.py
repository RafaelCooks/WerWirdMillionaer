# Imports für GUI, Zufallsfunktionen und Dateizugriff
import tkinter as tk
import random
import json
from joker import telefonjoker, joker_50_50, publikumsjoker
from tkinter import messagebox
import sys
import os

# Funktion für Zugriff auf Ressourcen (z.B. JSON-Dateien) – wichtig für PyInstaller (.exe-Erstellung)
def resource_path(relative_path):
    """Gibt den absoluten Pfad zur Ressource zurück – funktioniert auch nach dem Kompilieren mit PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Laden der Fragen aus externer JSON-Datei
with open(resource_path("fragenkatalog.json"),"r", encoding="utf-8") as f:
    fragen_datenbank = json.load(f)

# Definierte Gewinnstufen von 100 € bis 1 Million €
geldleiter = [
    "100 €", "200 €", "300 €", "500 €", "1.000 €",
    "2.000 €", "4.000 €", "8.000 €", "16.000 €", "32.000 €",
    "64.000 €", "125.000 €", "250.000 €", "500.000 €", "1.000.000 €"
]

# Farbzuweisung je nach Schwierigkeitsgrad
farben = {
    "leicht": "#4CAF50",     # Grün
    "mittel": "#FFC107",     # Gelb
    "schwer": "#F44336"      # Rot
}

# Hauptklasse für das Spiel – enthält Spiellogik & UI
class MillionaireGame(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#1b1f3b")
        self.app = app  # Referenz zur Hauptanwendung
        self.frage_index = 0  # Start bei Frage 0
        self.alle_fragen = self.generate_questions()  # Fragen mischen
        self.timer_seconds = 0
        self.timer_id = None
        self.timer_aktiv = True  # Timer ist standardmäßig aktiv

        self.setup_ui()      # Benutzeroberfläche erstellen
        self.naechste_frage()  # Erste Frage anzeigen

    # Mischt aus jeder Schwierigkeitsstufe 5 Fragen zusammen
    def generate_questions(self):
        return (
            random.sample(fragen_datenbank["leicht"], 5) +
            random.sample(fragen_datenbank["mittel"], 5) +
            random.sample(fragen_datenbank["schwer"], 5)
        )

    # Aufbau der Benutzeroberfläche (UI)
    def setup_ui(self):
        # Hauptbereich links (Frage + Antworten)
        self.main_frame = tk.Frame(self, bg="#1b1f3b")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=40, pady=20)

        # Fragebereich in Kachel-Stil
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

        # Zeitbalken
        self.timer_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.timer_frame.pack(pady=10)

        self.timer_bar_canvas = tk.Canvas(self.timer_frame, height=20, width=400, bg="#444", bd=0, highlightthickness=0)
        self.timer_bar_canvas.pack()

        self.timer_text = tk.Label(self.timer_frame, text="", font=("Segoe UI", 14, "bold"), fg="white", bg="#1b1f3b")
        self.timer_text.pack(pady=5)

        # Publikumsjoker-Visualisierung (initial unsichtbar)
        self.publikums_frame = tk.Frame(self.main_frame, bg="#1b1f3b")
        self.publikums_frame.pack(pady=10, fill="x", expand=True)
        self.publikums_frame.pack_forget()  # erst anzeigen, wenn genutzt

        self.publikums_canvas = tk.Canvas(self.publikums_frame, width=650, height=200, bg="#1b1f3b", highlightthickness=0)
        self.publikums_canvas.pack(fill="x", padx=50)

        # Rechte Seitenleiste (Joker + Gewinnstufen)
        self.sidebar = tk.Frame(self, width=220, bg="#121428")
        self.sidebar.pack(side="right", fill="y", padx=10)

        # Joker-Bereich
        self.joker_frame = tk.LabelFrame(self.sidebar, text="Joker", font=("Segoe UI", 12, "bold"),
                                         bg="#121428", fg="white", bd=2, relief="groove", labelanchor="n")
        self.joker_frame.pack(pady=15, padx=10, fill="x")

        # Joker-Buttons
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

        # Geldleiter-Anzeige (unten = erste Frage, oben = Million)
        geld_frame = tk.LabelFrame(self.sidebar, text="Gewinnstufen", font=("Segoe UI", 12, "bold"),
                                   bg="#121428", fg="white", bd=2, relief="groove", labelanchor="n")
        geld_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.geldleiter_labels = []
        for i, betrag in reversed(list(enumerate(geldleiter))):
            lbl = tk.Label(geld_frame, text=f"{i+1}. {betrag}", font=("Segoe UI", 12),
                           bg="#121428", fg="white", anchor="w", padx=10)
            lbl.pack(fill="x", pady=1)
            self.geldleiter_labels.insert(0, lbl)  # umdrehen

    # Gibt Schwierigkeitsgrad anhand der aktuellen Frage zurück
    def get_schwierigkeit(self):
        if self.frage_index < 5:
            return "leicht"
        elif self.frage_index < 10:
            return "mittel"
        else:
            return "schwer"

    # Zeigt die nächste Frage und setzt alles zurück
    def naechste_frage(self):
        self.publikums_frame.pack_forget()  # ggf. Balkendiagramm ausblenden

        # Spielende erreicht?
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

        # Neue Antwortliste speichern
        frage["gemischte_antworten"] = antworten

        # Buttons beschriften und aktivieren
        for i in range(4):
            self.buttons[i].config(text=antworten[i], state="normal", bg="#3a3f78")

        self.highlight_geldstufe()

        # Vorherigen Timer stoppen, neuen starten
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_aktiv = True
        self.update_timer()

    # Timer herunterzählen und Balken aktualisieren
    def update_timer(self):
        if not self.timer_aktiv or self.frage_index >= len(self.alle_fragen):
            return

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
            self.timer_id = None
            self.app.show_end(False, geldleiter[self.frage_index - 1] if self.frage_index > 0 else "0 €", "Zeit abgelaufen!")

    # Prüft, ob die Antwort richtig ist, markiert Buttons
    def antwort_pruefen(self, index):
        self.timer_aktiv = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

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

    # Bei richtiger Antwort: nächste Frage laden
    def frage_richtig(self):
        self.frage_index += 1
        self.naechste_frage()

    # Hebt aktuelle Gewinnstufe hervor
    def highlight_geldstufe(self):
        for i, lbl in enumerate(self.geldleiter_labels):
            if i == self.frage_index:
                lbl.config(bg="#FFD700", fg="#000")
            else:
                lbl.config(bg="#121428", fg="white")


    # ================================================
    # 🃏 Joker-Funktionen
    # ================================================

    # 📞 Telefonjoker (Auswahlfenster für Kontaktpersonen)
    def nutze_telefonjoker(self):
        self.joker_btn.config(state="disabled")  # Joker-Button deaktivieren
        if self.timer_id:
            self.after_cancel(self.timer_id)  # Falls aktiv: Timer stoppen
            self.timer_id = None
        self.timer_aktiv = False  # Timer-Zustand aktualisieren

        # Frame für Joker-Auswahl (neues Untermenü)
        self.telefon_frame = tk.Frame(self.main_frame, bg="#1b1f3b", bd=2)
        self.telefon_frame.pack(pady=(10, 5))  # Abstand etwas reduziert

        # Überschrift
        label = tk.Label(self.telefon_frame, text="📞 Wen möchtest du anrufen?", font=("Segoe UI", 16, "bold"),
                        fg="white", bg="#1b1f3b")
        label.pack(pady=10)

        # Buttons für fiktive Gesprächspartner
        for name in ["Albert Einstein", "Mama", "Papa", "Harald Lesch"]:
            btn = tk.Button(
                self.telefon_frame,
                text=name,
                font=("Segoe UI", 12),
                width=18,
                bg="#3a3f78",
                fg="white",
                command=lambda n=name: self.startelefonjoker(n)  # Auswahl übergibt Name
            )
            btn.pack(pady=5)

    # 📞 Telefonjoker – Gespräch starten mit gewählter Person
    def startelefonjoker(self, name):
        self.telefon_frame.destroy()  # Auswahl-Frame ausblenden

        # Frage und Antworten abrufen
        frage = self.alle_fragen[self.frage_index]
        richtige_antwort = frage["richtig"]
        falsche_antworten = [a for a in frage["antworten"] if a != richtige_antwort]

        # Antwort generieren über Hilfsfunktion
        ergebnis = telefonjoker(name, richtige_antwort, falsche_antworten)

        # Rahmen für Sprechblase
        self.sprechblase = tk.Frame(self.main_frame, bg="#2c2f4c", bd=2, relief="groove")
        self.sprechblase.pack(pady=20, padx=30)

        # Label für den Text des Gesprächs
        self.gespraech_label = tk.Label(
            self.sprechblase,
            text="",
            font=("Segoe UI", 20),
            fg="white",
            bg="#2c2f4c",
            wraplength=800,
            justify="left",
            padx=20,
            pady=20
        )
        self.gespraech_label.pack(pady=20)

        # Textsätze für Gespräch
        satzliste = [
            f"📞 {ergebnis['name']} ist jetzt am Telefon...",
            f"{ergebnis['name']}: {ergebnis['sicherheit']} " +
            f"\n👉 «{ergebnis['antwort']}»",
        ]

        # Gespräch anzeigen (mit Pausen)
        self.zeige_gespraech(satzliste, 0)

    # 🎙 Gespräch mit Joker – Satzweise anzeigen mit Pausen
    def zeige_gespraech(self, saetze, index):
        if index >= len(saetze):
            # Nach letzter Zeile: Blase nach kurzer Zeit ausblenden
            self.gespraech_label.after(2000, self.sprechblase.destroy)

            # Falls weitere Fragen vorhanden sind, Timer fortsetzen
            if self.frage_index < len(self.alle_fragen) and not self.timer_aktiv:
                self.timer_aktiv = True
                self.after(500, self.update_timer)
            return

        # Zeige aktuellen Satz
        self.gespraech_label.config(text=saetze[index])

        # Weiter zum nächsten Satz nach 3 Sekunden
        self.after(3000, lambda: self.zeige_gespraech(saetze, index + 1))


    # ➗ 50:50-Joker – zwei falsche Antworten entfernen
    def nutze_5050_joker(self):
        frage = self.alle_fragen[self.frage_index]
        richtige_antwort = frage["richtig"]
        gemischt = frage["gemischte_antworten"]

        # Alle falschen Antworten bestimmen
        falsche = [a for a in gemischt if a != richtige_antwort]

        # Zwei zufällige falsche entfernen
        verbleibend = joker_50_50(richtige_antwort, falsche)

        # Buttons aktualisieren – nur verbleibende sichtbar/aktiv
        for btn in self.buttons:
            text = btn.cget("text")
            if text in verbleibend:
                btn.config(state="normal")
            else:
                btn.config(state="disabled", text="")

        self.joker_btn_5050.config(state="disabled")  # Joker-Button deaktivieren


    # 📊 Publikumsjoker – Umfrage auslösen und visualisieren
    def nutze_publikumsjoker(self):
        frage = self.alle_fragen[self.frage_index]
        richtige = frage["richtig"]
        gemischt = frage["gemischte_antworten"]
        falsche = [a for a in gemischt if a != richtige]

        # Stimmverteilung abrufen
        stimmen = publikumsjoker(richtige, falsche)

        # Visualisierung anzeigen
        self.zeige_publikumsdiagramm(stimmen)

        self.joker_btn_pub.config(state="disabled")  # Joker-Button deaktivieren


    # 📊 Balken animieren (einzelne Antwort)
    def animate_bar(self, bar, value_text, bottom, target_height, final_value, step):
        if step > target_height:
            # Wenn Endhöhe erreicht: finalen Prozentwert anzeigen
            self.publikums_canvas.itemconfig(value_text, text=f"{final_value} %")
            return

        # Neue Höhe berechnen und Balken sowie Text aktualisieren
        new_top = bottom - step
        self.publikums_canvas.coords(bar, self.publikums_canvas.coords(bar)[0], new_top, self.publikums_canvas.coords(bar)[2], bottom)
        self.publikums_canvas.coords(value_text, (self.publikums_canvas.coords(bar)[0] + self.publikums_canvas.coords(bar)[2]) / 2, new_top - 10)

        # Wiederhole Animation nach 10ms (stufenweise wachsen)
        self.after(10, lambda: self.animate_bar(bar, value_text, bottom, target_height, final_value, step + 5))


    # 📊 Zeige Publikumsergebnis als Balkendiagramm
    def zeige_publikumsdiagramm(self, stimmen_dict):
        self.publikums_frame.pack()  # Sichtbar machen
        self.publikums_canvas.delete("all")  # Vorherige Grafik löschen

        # Einstellungen
        bar_width = 60
        spacing = 100
        max_height = 120
        x_start = 60
        bottom = 140

        max_stimmen = max(stimmen_dict.values())  # Für relative Höhe
        farben = ["#4CAF50", "#2196F3", "#FFC107", "#F44336"]  # Farben A–D

        # Zeichne für jede Antwort einen Balken
        for i, (antwort, stimmen) in enumerate(sorted(stimmen_dict.items())):
            x = x_start + i * (bar_width + spacing)
            hoehe = int((stimmen / max_stimmen) * max_height)
            farbe = farben[i % len(farben)]

            # Lege leeren Balken an
            bar = self.publikums_canvas.create_rectangle(x, bottom, x + bar_width, bottom, fill=farbe, width=0)
            text = self.publikums_canvas.create_text(x + bar_width / 2, bottom + 15, text=antwort, fill="white", font=("Segoe UI", 12))
            value_text = self.publikums_canvas.create_text(x + bar_width / 2, bottom - hoehe - 10, text="", fill="white", font=("Segoe UI", 12))

            # Animierter Balkenaufbau
            self.animate_bar(bar, value_text, bottom, hoehe, stimmen, 0)


__all__ = ["MillionaireGame"]  # Export für externen Import
