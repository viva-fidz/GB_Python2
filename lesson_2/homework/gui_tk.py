from tkinter import *
# from db import Fill_db, Get_from_db
import sqlite3


def sql_get_payments():
    """ SQL-заглушка
    """
    with sqlite3.connect('c.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Payment"""),
        output = cursor.fetchall()
        return output


def sql_get_terminals():
    """ SQL-заглушка
    """
    with sqlite3.connect('c.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Terminal"""),
        output = cursor.fetchall()
        return output


def sql_get_partners():
    with sqlite3.connect('c.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Partner"""),
        output = cursor.fetchall()
        return output


class TableGrid(Frame):
    ''' Заготовка для создания табличного вида
    '''

    def __init__(self, parent=None, titles=None, rows=0, *args):
        super().__init__(parent, relief=GROOVE, width=w, height=h, bd=1)
        self.w = w
        self.h = h  # Создаем основное окно программы

        for index, title in enumerate(titles):
            Label(self, text=title).grid(row=0, column=index)

        # self.rebuild(0, 0)
        # self.pack()

        self.rebuild(1, len(titles))
        self.grid(columnspan=len(titles))

    def rebuild(self, rows=0, columns=0):

        self.cells = []
        self.vars = []

        for i in range(1, rows + 1):
            self.vars.append([])

            for j in range(columns):
                var = StringVar()  # TK-интеровская переменная
                cell = Entry(self, textvariable=var)
                cell.grid(row=i, column=j)
                self.vars[i - 1].append(var)
                self.cells.append(cell)

    def get_terminals(self):
        sql_data = sql_get_terminals()
        self.rebuild(len(sql_data), len(sql_data[0]))
        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)

    def get_partners(self):
        sql_data = sql_get_partners()
        self.rebuild(len(sql_data), len(sql_data[0]))
        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)

    def get_payments(self):
        sql_data = sql_get_payments()
        self.rebuild(len(sql_data), len(sql_data[0]))
        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)

    def update_data(self, data_func):
        """ Заполнение таблицы данными.
        Заполнение производится через связанные переменные.
        """
        sql_data = data_func()

        for index, data in enumerate(sql_data):
            for i, d in enumerate(data):
                self.vars[index][i].set(d)


main_window = Tk()
frame = Frame(main_window)

# Вычисляем координаты середины экрана.
# Сначала определим ширину и высоту:
ws = main_window.winfo_screenwidth()
hs = main_window.winfo_screenheight()

w = 800
h = 400

# Затем вычислим координаты при выбранных ширине и высоте:
x = ws // 2 - w // 2
y = hs // 2 - h // 2

# Зададим размеры и расположение окна:
main_window.geometry('{}x{}+{}+{}'.format(w, h, x, y))

main_window.title('БД - админ')
grid_term = TableGrid(main_window, ('id', 'title', 'config', 'cmnt'), 4)
grid_part = TableGrid(main_window, ('partner_id', 'partner_name', 'cmnt'), 3)
grid_pay = TableGrid(main_window, ('№', 'дата', 'terminal_id', 'transaction_id', 'partner_id', 'сумма'), 6)

# Для создания меню сначала создаётся корневой элемент:
main_menu = Menu(main_window)
file_menu = Menu(main_menu)
file_menu.add_command(label='Terminals/Все терминалы', command=lambda g=grid_term: g.get_terminals())
file_menu.add_command(label='Partners/Все партнеры', command=lambda g=grid_part: g.get_partners())
file_menu.add_command(label='Partners/Все платежи', command=lambda g=grid_pay: g.get_payments())
main_menu.add_cascade(label='База данных', menu=file_menu)


# Добавление меню главному окну:
main_window.config(menu=main_menu)

# Запуск основного цикла программы:
mainloop()
