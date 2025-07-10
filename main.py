import tkinter as tk
from Screens.startmenu import StartMenu
from Screens.spiel import MillionaireGame
from Screens.endscreen import EndScreen

class MainApp:
    def __init__(self, root):
        # Hauptfenster initialisieren
        self.root = root
        self.root.attributes('-fullscreen', True)  # Vollbildmodus aktivieren
        self.root.configure(bg="#1b1f3b")  # Hintergrundfarbe setzen (dunkles Blau)

        # Container-Frame für die Screens
        self.container = tk.Frame(root, bg="#1b1f3b")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None  # Aktuell angezeigter Screen
        self.fade_step = 0.05  # Schrittgröße für Einblend-Effekt

        self.show_start_menu()  # Startmenü direkt anzeigen

    def fade_out_in(self, new_frame_class):
        """
        Übergangseffekt zwischen zwei Screens – mit Overlay, das eingeblendet
        und dann wieder ausgeblendet wird.
        """
        overlay = tk.Frame(self.container, bg="#1b1f3b")  # Overlay in dunkler Farbe
        overlay.place(relwidth=1, relheight=1)

        # Neuen Frame erzeugen und platzieren
        new_frame = new_frame_class(self.container, self)
        new_frame.place(relwidth=1, relheight=1)

        # Alten Frame entfernen
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame

        # Funktion für sanftes Ausblenden des Overlays
        def fade(alpha=1.0):
            if alpha <= 0:
                overlay.destroy()  # Overlay entfernen, wenn ganz durchsichtig
            else:
                # Farbe schrittweise aufhellen (Übergangseffekt)
                grau = int(27 * alpha)
                color = f"#{grau:02x}{grau:02x}{grau:02x}"
                overlay.config(bg=color)
                self.root.after(30, lambda: fade(alpha - 0.1))

        fade()

    def _switch_frame(self, new_frame_class):
        """
        Wechselt den aktuellen Frame ohne Overlay-Effekt (nicht verwendet, aber vorbereitet)
        """
        if self.current_frame:
            self.current_frame.place_forget()
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, self)
        self.current_frame.place(relwidth=1, relheight=1)
        self._fade_in()

    def _fade_out(self, callback):
        """
        Blendet aktuellen Frame aus und ruft dann Callback für nächsten Frame auf
        """
        old_frame = self.current_frame
        self.current_frame = None  # Wichtig: zuerst "freigeben", bevor der neue Frame erscheint

        if old_frame:
            old_frame.place_forget()
            old_frame.destroy()

        callback()

    def _fade_in(self, alpha=0.0):
        """
        Blendet das Fenster langsam ein (Transparenz steigern)
        """
        if alpha >= 1:
            self.root.attributes('-alpha', 1)
        else:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self._fade_in(alpha + self.fade_step))

    def show_start_menu(self):
        # Zeigt das Startmenü an
        self.fade_out_in(StartMenu)

    def show_game(self):
        # Startet das eigentliche Spiel
        self.fade_out_in(MillionaireGame)

    def show_end(self, gewonnen, betrag, grund=""):
        # Zeigt den Endscreen mit Spielausgang
        self.fade_out_in(lambda parent, app: EndScreen(parent, app, gewonnen, betrag, grund))


def main():
    # Einstiegspunkt der Anwendung
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
