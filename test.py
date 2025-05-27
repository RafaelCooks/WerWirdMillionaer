import tkinter as tk
from random import randint, choice
from functools import partial


QUESTIONS = {
    1: {
        "Question": "In welcher deutschen Stadt wurde der Reichstag verhÃ¼llt?",
        "Answers": [
                ['A:', 'Bonn', False], 
                ['B:', 'Berlin', True],
                ['C:', 'Hamburg', False],
                ['D:', 'MÃ¼nchen', False]]},
    
        
                
    2: {
        "Question": "Welches Tier hat das Baden WÃ¼rttenberg im Wappen?",
        "Answers": [
                ['A:', 'Adler', False], 
                ['B:', 'Fisch', False],
                ['C:', 'BÃ¤r', False],
                ['D:', 'LÃ¶we', True]]},
                
    3: {
        "Question": "Was gilt als KÃ¶nig der Tiere ?",
        "Answers": [
                ['A:', 'Vogel', False], 
                ['B:', 'LÃ¶we', True],
                ['C:', 'Katze', False],
                ['D:', 'Schwein', False]]},
                
    4: {
        "Question": "Welches Tier rollt sich bei Gefahr zu einer Kugel?",
        "Answers": [
                ['A:', 'Pferd', False], 
                ['B:', 'Katze', False],
                ['C:', 'Igel', True],
                ['D:', 'Affe', False]]},

    5:  {
        "Question": "Wenn das Wetter gut ist, wird der Bauer bestimmt den Eber, das Ferkel und ...?",
        "Answers": [
                ['A:', 'einen drauf machen', False],
                ['B:', 'die Nacht durchmache', False],
                ['C:', 'die sau rauslassen', True],
                ['D:', 'auf die Kacke hauen', False]]},
    

    6:  {
        "Question": "Was war bereits seit Mai 1969 ein beliebtes Zahlungsmittel im europÃ¤ischen Raum?",
        "Answers":  [
                ['A:', 'Euronoten', False],
                ['B:', 'Eurocheques', True],
                ['C:', 'Euroscheine', False],
                ['D:', 'EuromÃ¼nzen', False]]},

    7:  {
        "Question": "Malu Dreyer profitierte Anfang des Jahres von ...?",
        "Answers":  [
                ['A:', 'Oettingers Sattelstang', False],
                ['B:', 'Veltins Fahrradkette', False],
                ['C:', 'Diebels Vorderreifen', False],
                ['D:', 'Becks RÃ¼cktritt', True]]}
    
            }

def create_dialog(key, callback):
    
    dialog_win = tk.Toplevel()
    dialog_win.title('Frage-{0}'.format(key))
    
    
    question = QUESTIONS[key]["Question"]
    
    frame = tk.Frame(dialog_win)
    frame.pack(padx=20, pady=10)
    
    tk.Label(frame, text=question, font=('Helvetica', 14, 'bold'),
        fg='red').pack(padx=20, pady=10)
    
    [tk.Button(frame, text=nr+answer, command=partial(callback, check,
        dialog_win)).pack(fill='x', padx=40, pady=30)
            for nr, answer, check in QUESTIONS[key]["Answers"]]    

def ask_question(check=None, dialog=None):
    
    if check is None:
        create_dialog(choice(QUESTIONS.keys()), ask_question)
        return
    
    dialog.destroy()
        
    if check:
        create_dialog(choice(QUESTIONS.keys()), ask_question)
    
    
app_win=tk.Tk()
app_win.title("Wer wird MillionÃ¤r!")

back_gnd = tk.Canvas(app_win)
back_gnd.pack(expand=True, fill='both')

#back_gnd_image = tk.PhotoImage(file="www.gif")
#back_gnd.create_image(0, 0, anchor='nw', image=back_gnd_image)


tk.Button(app_win,text='Spielen',command=ask_question).pack(expand=True)
tk.Button(app_win,text='Verlassen',command=app_win.destroy).pack(expand=True)

app_win.geometry('250x150-650+200')
app_win.mainloop()
