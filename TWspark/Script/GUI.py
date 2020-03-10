from tkinter import *
import os
import threading

font = ("Arial Black", 10)


class GUI:
    def __init__(self, root):
        self.window = root
        self.window.title("Tweets Analysis")

        self.lbl = Label(self.window, text="Insert keywords:", font=font)
        self.lbl.grid(column=0, row=0)

        self.txt = Entry(self.window, width=25, bg='white')
        self.txt.grid(column=0, row=1)
        self.txt.bind("<Return>", lambda event: self.insert_word())  # send with "send" key

        self.btn = Button(self.window, text="Enter", command=self.insert_word)   #save button
        self.btn.grid(column=1, row=1)

        self.lbl = Label(self.window, text="Inserted terms: ")
        self.lbl.grid(column=0, row=3)
        self.show = Label(self.window, text="")
        self.show.grid(column=0, row=4)

        self.lbl = Label(self.window, text="--Select search mode:", font=font)
        self.lbl.grid(column=2, row=0)

        self.var = IntVar()
        self.testo2 = ""

        self.R1 = Radiobutton(self.window, text="1) Historical", variable=self.var, value=1, command=self.compute)

        self.R1.grid(column=2, row=2)

        self.R2 = Radiobutton(self.window, text="2) Real time", variable=self.var, value=2, command=self.compute)
        self.R2.grid(column=2, row=3)

        self.lbl = Label(self.window, text="", font=font)
        self.lbl.grid(column=0, row=7)

        self.lbl3 = Label(self.window, text="Enter at least one word")
        self.lbl3.grid(column=0, row=10)

        self.btn_search = Button(self.window, text="Compute", command=self.get_command, font=font)

        self.btn_search.grid(column=2, row=10)
        self.btn_search.config(state="disabled")

    def insert_word(self):
        self.testo = self.txt.get()
        print("testo scritto: {}".format(self.testo))

        self.testo2 = self.testo
        self.testo2 = self.testo2.split(' ')
        self.testo2 = list(filter(None, self.testo2))  # list without whitespaces
        self.stringa = ','.join(self.testo2)

        self.show.config(text="{}".format(self.stringa))

        self.compute()

    def compute(self):
        if str(self.var.get()) == '1':  # Historical mode (at least one word)
            #self.lbl2.config(text="Mode: Historical Tweets")
            if len(self.testo2) < 1:
                self.btn_search.config(state="disabled")
                self.lbl3.config(text="Enter at least one word")
            else:
                self.btn_search.config(state="active")
                self.lbl3.config(text="")

        elif str(self.var.get()) == '2':  # Real time mode (at least three words)
            #self.lbl2.config(text="Mode: RT")
            if len(self.testo2) < 3:
                self.btn_search.config(state="disabled")
                self.lbl3.config(text="Enter at least three words")

            else:   # button
                self.btn_search.config(state="active")
                self.lbl3.config(text="")

        elif str(self.var.get()) != '1' and str(self.var.get()) != '2':   # no mode selected
            self.lbl3.config(text="Select a search mode")

    def call_client(self):
        path = os.path.join(os.path.dirname(__file__), "TWclient.py")
        plat = sys.platform
        try:
            if plat.startswith("linux"):
                print("[+] Linux system detected")
                os.system("xterm -hold -e python3  {} {} {}".format(path, self.stringa, self.var.get()))
            elif plat.startswith("win"):
                print("[+] Widows system detected")
                os.system("START cmd /k py -3  {} {} {}".format(path, self.stringa, self.var.get()))  # WINDOWS

            elif plat.startswith('darwin'):
                print("[+] Mac system detected...")
                os.system("osascript -e 'tell app \"terminale\" "
                          "to do script \"python3 {} {} {}\"'".format(path, self.stringa, self.var.get()))  # MAC OS

            else:
                print("[!] Not a valid system")

        except Exception as e:
            print(e)

    def get_command(self):
        threading.Thread(target=self.call_client).start()


if __name__ == "__main__":
    root = Tk()
    foo = GUI(root)
    root.mainloop()
