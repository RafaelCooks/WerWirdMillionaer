import tkinter as tk
from Screens.startmenu import StartMenu
from Screens.spiel import MillionaireGame
from Screens.endscreen import EndScreen

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


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
