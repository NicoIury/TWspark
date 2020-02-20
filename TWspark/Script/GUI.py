from tkinter import *
import os

font = ("Arial Black", 10)


class GUI:
    def __init__(self):

        self.window = Tk()
        self.window.title("BD_analisi")

        self.lbl = Label(self.window, text="inserisci parole chiave:", font=font)
        self.lbl.grid(column=0, row=0)

        self.txt = Entry(self.window, width=20)
        self.txt.grid(column=0, row=1)
        self.txt.bind("<Return>", lambda event: self.inserisci_parola())  # send con tasto invio

        self.lbl = Label(self.window, text="inserisci termini", font=font)
        self.lbl.grid(column=0, row=4)

        self.btn = Button(self.window, text="invia", command=self.inserisci_parola, font=font)   #salva button
        self.btn.grid(column=0, row=5)

        self.lbl = Label(self.window, text="Termini inseriti: ", font=font)
        self.lbl.grid(column=0, row=6)

        self.lbl = Label(self.window, text="--Seleziona modalità di esecuzione:", font=font)
        self.lbl.grid(column=1, row=0)

        self.var = IntVar()
        self.testo2 = ""

        self.R1 = Radiobutton(self.window, text="1) Historical", variable=self.var, value=1, command=self.compute)

        self.R1.grid(column=1, row=2)

        self.R2 = Radiobutton(self.window, text="2) Real time", variable=self.var, value=2, command=self.compute)
        self.R2.grid(column=1, row=3)

        self.lbl = Label(self.window, text="", font=font)
        self.lbl.grid(column=0, row=7)

        self.lbl2 = Label(self.window, text="Select mode")
        self.lbl2.grid(column=1, row=4)

        self.lbl3 = Label(self.window, text="Inserisci almeno 1 parola")
        self.lbl3.grid(column=0, row=10)

        self.btn_search = Button(self.window, text="Compute", command=self.callClient)

        self.btn_search.grid(column=1, row=10)
        self.btn_search.config(state="disabled")

        self.window.mainloop()

    def inserisci_parola(self):
        self.testo = self.txt.get()
        print("testo scritto: {}".format(self.testo))

        self.testo2 = self.testo
        self.testo2 = self.testo2.split(' ')
        self.testo2 = list(filter(None, self.testo2))  # per ottenere una lista senza spazi
        self.stringa = ','.join(self.testo2)

        self.lbl.config(text="".format(self.stringa), font=font)

        self.compute()

    def compute(self):
        if str(self.var.get()) == '1':  # Historical mode (almeno 1 parola)
            self.lbl2.config(text="Mode: Historical Tweets")
            if len(self.testo2) < 1:
                self.btn_search.config(state="disabled")
                self.lbl3.config(text="Inserisci almeno 1 parola")
            else:
                self.btn_search.config(state="active")
                self.lbl3.config(text="")

        elif str(self.var.get()) == '2':  # Real time mode (almeno 3 parole)
            self.lbl2.config(text="Mode: RT")
            if len(self.testo2) < 3:
                self.btn_search.config(state="disabled")
                self.lbl3.config(text="Inserisci almeno 3 parole")

            else:   #bottone
                self.btn_search.config(state="active")
                self.lbl3.config(text="")

        elif str(self.var.get()) != '1' and str(self.var.get()) != '2':   # no mode selected
            self.lbl3.config(text="Seleziona una modalità di ricerca")

    def callClient(self):
        path = os.path.join(os.path.dirname(__file__), "TWclient.py")
        os.system("xterm -hold -e python3  {} {} {}".format(path, self.stringa, self.var.get()))


if __name__ == "__main__":
    foo = GUI()
