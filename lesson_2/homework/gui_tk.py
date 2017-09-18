from tkinter import *
import sqlite3


def sql_get_payments():
    """ SQL-заглушка
    """
    with sqlite3.connect('company.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Payment"""),
        output = cursor.fetchall()
        return output


def sql_get_terminals():
    with sqlite3.connect('company.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Terminal"""),
        output = cursor.fetchall()
        return output


def sql_get_partners():
    with sqlite3.connect('company.db3') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            select * from Partner"""),
        output = cursor.fetchall()
        return output


class TableGrid(Frame):
    """ Заготовка для создания табличного вида
    """

    def __init__(self, parent=None, titles=None, rows=0, *args, **kwargs ):
        w = kwargs.get('w', 800)
        h = kwargs.get('h', 150)
        super().__init__(parent, relief=GROOVE, width=w, height=h, bd=1, bg='green')
        self.w = w
        self.h = h

        # Создаем возможность вертикальной прокрутки таблицы:
        self._create_scroll()

        # Размещаем заголовки
        for index, title in enumerate(titles):
            Label(self.frame, text=title).grid(row=0, column=index)

        # Создаём пустые строки (для наглядности, что это таблица)
        self.rebuild(len(titles), rows)

        # Размещаем текущий объект self в родительском виджете parent
        self.grid(columnspan=5)

    def _create_scroll(self):
        """ Обёртка для создания прокрутки внутри Frame.
        Дело в том, что элемент Scrollbar можно привязать
        только к "прокручиваемым" виджетам (Canvas, Listbox, Text),
        в то время как наша "таблица" создана на основе Frame.
        Чтобы решить эту задачу, нужно внутри нашего фрейма создать дополнительные
        виджеты: Canvas и Frame.
        """
        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)

        # Сам по себе Scrollbar - хитрый...
        # Нужно сделать связь не только в Scrollbar, но и в привязанном Canvas'е:
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # "Упаковываем" Canvas и Scrollbar - один слева, другой справа:
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left")

        # Отрисовываем новый фрейм на Canvas'е
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # При событии <Configure> будет происходить перерисовывание Canvas'а.
        # Событие <Configure> - базовое событие для виджетов;
        # происходит, когда виджет меняет свой размер или местоположение.
        self.frame.bind("<Configure>", lambda e: self._scroll())

    def _scroll(self):
        """
            Перерисовка канвы и области прокрутки
        """
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.w, height=self.h)

    def rebuild(self, rows=0, columns=0):
        """
            Пересоздание таблицы полей ввода.
        """
        self.vars = []
        self.cells = []

        for i in range(1, rows + 1):
            self.vars.append([])
            for j in range(columns):
                # Создаём связанную переменную, которая будет "передавать" данные в виджет
                var = StringVar()
                # Внутри нашего виджета будет таблица связанных переменных  (почти MVC шаблон)
                self.vars[i - 1].append(var)

                # Создаём ячейку таблицы - это простое текстовое поле Entry с привязанной переменной
                cell = Entry(self.frame, textvariable=var)
                cell.grid(row=i, column=j)

                # Все ячейки тоже "запомним" внутри нашего виджета (чтобы можно было их удалять)
                self.cells.append(cell)

    def get_data(self, sql_data):
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

main_window.title('БД - админ')
grid_term = TableGrid(main_window, ('id', 'title', 'config', 'cmnt'), 4)
grid_part = TableGrid(main_window, ('partner_id', 'partner_name', 'cmnt'), 3)
grid_pay = TableGrid(main_window, ('id', 'дата', 'terminal_id', 'transaction_id', 'partner_id', 'сумма'), 6)

# Для создания меню сначала создаётся корневой элемент:
main_menu = Menu(main_window)
file_menu = Menu(main_menu)
file_menu.add_command(label='Показать терминалы', command=lambda g=grid_term: g.get_data(sql_get_terminals()))
file_menu.add_command(label='Показать партнеров', command=lambda g=grid_part: g.get_data(sql_get_partners()))
file_menu.add_command(label='Показать платежи', command=lambda g=grid_pay: g.get_data(sql_get_payments()))
main_menu.add_cascade(label='База данных', menu=file_menu)

# Добавление меню главному окну:
main_window.config(menu=main_menu)


# Запуск основного цикла программы:
mainloop()


# кнопки https://metanit.com/python/tutorial/9.2.php
