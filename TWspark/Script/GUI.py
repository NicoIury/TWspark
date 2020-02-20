from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk

font=("Arial Black",10)

class GUI:
    def main(self):
        self.root_win()

    def root_win(self):

        self.window= Tk()
        self.window.title("BD_analisi")
        self.window.geometry('900x350')

        self.lbl = Label(self.window, text="inserisci 3 parole chiave:", font=font)
        self.lbl.grid(column=0, row=0)

        self.txt = Entry(self.window, width=20)
        self.txt.grid(column=0, row=1)
        self.txt.bind("<Return>", lambda event: self.inserisci_parola()) # send con tasto invio

        self.lbl = Label(self.window, text="inserisci termini", font=font)
        self.lbl.grid(column=0, row=4)

        self.btn = Button(self.window, text="invia", command=self.inserisci_parola, font=font)   #salva button
        self.btn.grid(column=0, row=5)

        self.lbl = Label(self.window, text="Termini inseriti: ", font=font)
        self.lbl.grid(column=0, row=6)

        self.lbl = Label(self.window, text="--Seleziona modalità di esecuzione:", font=font)
        self.lbl.grid(column=1, row=0)

        self.var = IntVar()

        def sel():
            selection = "Mode: " + str(self.var.get())
            self.lbl2.config(text=selection)
            self.compute()

        self.R1 = Radiobutton(self.window, text="1) Historical", variable=self.var, value=1, command=sel)

        self.R1.grid(column=1,row=2)

        self.R2 = Radiobutton(self.window, text="2) Real time", variable=self.var, value=2, command=sel)
        self.R2.grid(column=1,row=3)

        self.lbl2 = Label(self.window, text="Select mode")
        self.lbl2.grid(column=1, row=4)

        self.window.mainloop()

    def inserisci_parola(self):

        self.testo=self.txt.get()
        print(f"testo scritto: '{self.testo}'")

        self.testo2=self.testo
        self.testo2=self.testo2.split(' ')
        self.testo2=list(filter(None,self.testo2)) #per ottenere una lista senza spazi
        self.stringa= ' '.join(self.testo2)

        self.lbl = Label(self.window, text=f"\t\t\t\t\t", font=font)
        self.lbl.grid(column=0, row=7)

        self.lbl = Label(self.window, text=f"'{self.stringa}'", font=font)
        self.lbl.grid(column=0, row=7)

        self.lbl = Label(self.window, text=f"'numero parole: {len(self.testo2)}'", font=font)
        self.lbl.grid(column=0, row=8)
        self.btn_search = Button(self.window, text="Compute")
        self.btn_search.grid(column=1, row=10)
        self.btn_search.config(state="disabled")
        self.compute()

    def compute(self):

        if str(self.var.get()) == '1': # Historical mode (almeno 1 parola)

            if len(self.testo2)<1:
                self.btn_search.config(state="disabled")
                self.lbl3 = Label(self.window, text="\tInserisci almeno 1 parola\t")
                self.lbl3.grid(column=0, row=10)
            else:
                self.btn_search.config(state="active")
                self.lbl3 = Label(self.window, text="\t\t\t\t")
                self.lbl3.grid(column=0, row=10)
                self.btn_search = Button(self.window, text="Compute")
                self.btn_search.grid(column=1, row=10)

        elif str(self.var.get()) == '2':  # Real time mode (almeno 3 parole)

            if len(self.testo2) < 3:
                self.btn_search.config(state="disabled")
                self.lbl3 = Label(self.window, text="\tInserisci almeno 3 parole\t")
                self.lbl3.grid(column=0, row=10)
                #self.btn_search.grid_forget()
            else:   #bottone
                self.btn_search.config(state="active")
                self.lbl3 = Label(self.window, text="\t\t\t\t")
                self.lbl3.grid(column=0, row=10)
                self.btn_search = Button(self.window, text="Compute")
                self.btn_search.grid(column=1, row=10)

        elif str(self.var.get()) != '1' and str(self.var.get()) != '2':   #no mode selected

            self.lbl3 = Label(self.window, text="Seleziona una modalità di ricerca")
            self.lbl3.grid(column=0, row=10)


g=GUI()
g.main()
