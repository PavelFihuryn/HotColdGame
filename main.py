from tkinter import *
from tkinter import messagebox
from bagels import *


class GameWindow:
    def __init__(self):
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200
        # root.geometry('530x450+{}+{}'.format(w, h))  # size window
        root.title('Горячо-Холодно')
        root.maxsize(width=600, height=520)
        root.minsize(width=530, height=450)
        root.iconphoto(False, PhotoImage(file=r'icon.png'))

        self.max_guess = 10
        self.num_digits = 3

        self.fra = Frame(root, width=220, height=380, bg="white", bd=3)
        self.fra.grid(row=1, column=0, padx=10, pady=10, rowspan=5)

        self.lbl = Label(root, text='Результат:', font="Arial 12")
        self.lbl.grid(row=0, column=0, padx=10, pady=5, sticky=S + W)

        self.lbl2 = Label(root, font="Arial 12")
        self.lbl2.grid(row=0, column=2, columnspan=2, rowspan=2, pady=10)
        self.lbl2.configure(text=f'Угадайте\n{self.num_digits}-х значное число\nс {self.max_guess} попыток')

        self.lbl3 = Label(root, font="Arial 14")
        self.lbl3.grid(row=2, column=2, columnspan=2)

        self.ent = Entry(root, width=self.num_digits, font="Arial 24", bd=3)
        self.ent.grid(row=3, column=2, pady=0, sticky=E)
        self.ent.bind("<Return>", self.button_ok)
        self.ent.focus_set()

        self.btn = Button(root, text='Ok', width=10, height=1)
        self.btn.bind("<Button-1>", self.button_ok)
        self.btn.bind("<Return>", self.button_ok)
        self.btn.grid(row=3, column=3, padx=20, pady=10)

        self.btn3 = Button(root, text='Заново', width=10, height=1)
        self.btn3.bind("<Button-1>", self.button_return)
        self.btn3.bind("<Return>", self.button_return)
        self.btn3.grid(row=5, column=3, sticky=S, pady=10)

        self.txt = Text(self.fra, font="Arial 11", width=33, height=22, wrap=WORD)
        self.txt.configure(state=DISABLED)
        self.txt.grid(row=0, column=1, padx=7, pady=7, sticky=N)

        self.max_guess = IntVar()
        self.max_guess.set(10)

        self.num_digits = IntVar()
        self.num_digits.set(3)

        self.val = 0
        self.secret_number = '0'
        self.menu()
        self.start_game()

    def start_game(self):
        self.num_digits.get()
        self.max_guess.get()
        self.ent.focus_set()
        self.lbl2.configure(text=f'Угадайте\n{self.num_digits.get()}-х значное число\nс {self.max_guess.get()} попыток')
        self.lbl3.configure(text=f'Попытка №1:', fg='black')
        self.btn3.configure(state=DISABLED)
        self.val = count_attempts(self.max_guess.get())
        self.secret_number = get_secret_number(self.num_digits.get())
        self.btn.configure(state=NORMAL)
        self.clear_text()
        self.ent.configure(width=self.num_digits.get())

    def button_rules(self):
        rules = f"Я загадл {self.num_digits.get()}-х значное чило, которое вы должны отгадать.\n" \
                "Я буду двать подсказки...\n\n" \
                "Когда я говорю\n" \
                "'Холодно', то это означает что ни одна цифра не отгадана\n" \
                "'Тепло' - одна цифра отгадана, но не отгадана позиция\n" \
                "'Горячо' - одна цифра и ее позиция отгаданы\n\n" \
                "Итак, я загадал число.\n\n" \
                f"У Вас есть {self.max_guess.get()} попыток, чтобы его отгадать"
        messagebox.showinfo("Правила", rules)

    def write_text(self, text):
        self.txt.configure(state=NORMAL)
        self.txt.insert(END, text)
        self.txt.see(END)
        self.txt.configure(state=DISABLED)

    def clear_text(self):
        self.txt.configure(state=NORMAL)
        self.txt.delete(0.0, END)
        self.txt.configure(state=DISABLED)

    def clear_entry(self):
        self.ent.delete(0, END)

    def button_return(self, event):
        self.start_game()

    def button_ok(self, event):
        try:
            player_number = self.get_player_move(self.val)
            result = is_number(self.secret_number, player_number)
            self.write_text(f'{player_number}\n')
            self.write_text(f'{result}\n')
            self.is_win(player_number)
        except RuntimeError:
            pass
        self.clear_entry()

    def is_win(self, player_number):
        if player_number == self.secret_number:
            self.lbl3.configure(text=f"Вы победили!\nЗагаданное число\nдействительно: {player_number}", fg='blue')
            self.write_text('\nПоздравляю! Вы побелили!!!')
            self.btn.configure(state=DISABLED)
            self.btn3.configure(state=NORMAL)
            self.btn3.focus_set()

    def game_over(self):
        self.lbl3.configure(text=f"Вы проиграли.\nЗагаданное число\nбыло: {self.secret_number}", fg='red')
        self.btn3.configure(state=NORMAL)
        self.btn.configure(state=DISABLED)
        self.btn3.focus_set()

    def get_player_move(self, num):
        value = self.ent.get()
        try:
            if len(value) == self.num_digits.get() and value.isdigit():
                pass
            else:
                raise TypeError
            self.ent.focus_set()
            number = next(num)
            if number < self.max_guess.get():
                self.lbl3.configure(text=f'Попытка №{number + 1}: ')
            else:
                self.game_over()
            self.write_text(f'Попытка №{number}: ')
        except TypeError:
            messagebox.showerror('Ошибка',
                                 f'Вводить необходимо {self.num_digits.get()}-значное число!')
            raise RuntimeError
        return value

    def menu(self):
        main_menu = Menu(root)
        sub_menu = Menu(root)
        sub_menu2 = Menu(root)
        sub_menu3 = Menu(root)
        root.config(menu=main_menu)
        sub_menu2.add_radiobutton(label='5', variable=self.max_guess, value=5, command=self.start_game)
        sub_menu2.add_radiobutton(label='10', variable=self.max_guess, value=10,command=self.start_game)
        sub_menu2.add_radiobutton(label='15', variable=self.max_guess, value=15, command=self.start_game)
        sub_menu3.add_radiobutton(label='3', variable=self.num_digits, value=3, command=self.start_game)
        sub_menu3.add_radiobutton(label='4', variable=self.num_digits, value=4, command=self.start_game)

        main_menu.add_command(label='Правила', command=self.button_rules)
        main_menu.add_cascade(label='Настройки', menu=sub_menu)
        sub_menu.add_cascade(label='Количество попыток', menu=sub_menu2)
        sub_menu.add_cascade(label='Количество цифр', menu=sub_menu3)
        main_menu.add_command(label='О программе', command=self.button_about)

    def button_settings(self):
        print('hello', self.max_guess.get(), self.num_digits.get())
        self.start_game()

    @staticmethod
    def button_about():
        messagebox.showinfo('О программе',
                            'Игра "Горячо-Холодно"\n\n'
                            'Создана по мотивам книги\n\n'
                            'Invent Your Own Computer Games with Python,\n'
                            '4th Edition, ISBN 978-1-59327-795-6,\n'
                            'published by No Starch Press\n\n\n'
                            'Разработал:     Фигурин Павел\n\n'
                            'Минск, ноябрь 2020')


if __name__ == '__main__':
    root = Tk()
    wind = GameWindow()
    root.mainloop()


