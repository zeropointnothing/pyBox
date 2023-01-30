import customtkinter as ctk
import random
import pyperclip

class App:
    def __init__(self, master: ctk.CTk) -> None:
        self.word_start = [
            "stupendous",
            "superb",
            "strange",
            "exotic",
            "interesting",
            "stunning",
            "super"
        ]
        ##words that can be used for the end portion of the password.
        self.word_end = [
            "bread",
            "chicken",
            "pizza",
            "cheese",
            "tornado",
            "house",
            "kitchen",
            "butters",
            "mountain",
            "dinosaur",
            "meats"
        ]
        
        self.pas = None

        self.master = master
        ## The size of the window created.
        self.master.geometry('600x400')
        self.master.resizable(False, False)
        self.master.wm_title('Password Generator')

        self.welc = ctk.CTkLabel(self.master, text='Welcome! Choose an option below:', font=('Arial', 16))
        self.welc.place(relx=0.5, rely=0.1, anchor='center')

        self.button1 = ctk.CTkButton(self.master, text='String(MOST SECURE)', command=self.generate_string)
        self.button1.place(relx=0.5, rely=0.3, anchor='center')
        
        self.button2 = ctk.CTkButton(self.master, text='2word(MOST MEMORABLE)', command=self.generate_2word)
        self.button2.place(relx=0.5, rely=0.4, anchor='center')

        self.welc = ctk.CTkLabel(self.master, text='Generated Password: ', font=('Arial', 12))
        self.welc.place(relx=0.5, rely=0.6, anchor='center')


        self.copy = ctk.CTkButton(self.master, text='Copy Password', command=self.copy)
        self.copy.place(relx=0.5, rely=0.8, anchor='center')

    def copy(self):
        pyperclip.copy(self.pas)

    def update_text(self):
        self.welc.configure(text=f'Generated Password: {self.pas}')

    def generate_string(self):
        pass_length = 14
        ##Creates the password.
        ##Characters that can appear in the password.
        ##The more of one that exists, the more common it will be.
        lower_case = "aaabbccddddefghiiijkllllmnoooopppqrrrrstuuuvwxxxxyz"
        upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number = "123456789873458734587634567834867678"
        symbols = "!!!___##"
        tag = '_' + "".join(random.sample(upper_case, 1))
        ##Combines the possible characters.
        comb = symbols + lower_case + upper_case + number
        ##Takes the 'comb' variable and randomly selects characters to keep
        ##with the max amount determined by pass_length
        password = "".join(random.sample(comb, pass_length))
        self.pas = password + tag
        self.update_text()
    
    def generate_2word(self):
        start = random.choice(self.word_start) #Chooses a random value from the list.
        end = random.choice(self.word_end)
        ##Joins start and end together to make the word combo.
        comb = "_".join([start, end])
        num = "".join(random.sample("1234567894254936747", 4)) #Grabs characters randomly.
        char = "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1))
        output = comb + '!!!' + num + char
        self.pas = output
        self.update_text()



if __name__ == '__main__':
    app = ctk.CTk()
    gui = App(master=app)
    app.mainloop()