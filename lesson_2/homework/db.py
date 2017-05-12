import sqlite3

with sqlite3.connect('company.db3') as conn:
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    cursor.execute("""DROP table if exists terminal""")
    cursor.execute("""DROP table if exists partner""")
    cursor.execute("""DROP table if exists payment""")

    cursor.execute("""
                     CREATE TABLE if not exists Terminal (
                            id  INTEGER PRIMARY KEY,
                            title TEXT, 
                            configuration TEXT,
                            comment TEXT,
                            pub_key TEXT   
                            );
                     """)

    cursor.execute("""               
                     CREATE TABLE if not exists Payment (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            datetime TEXT, 
                            terminal_id  INTEGER, 
                            transaction_id  INTEGER,
                            partner_id  INTEGER,
                            summ INTEGER
                            );
                     """)

    cursor.execute("""
                     CREATE TABLE if not exists Partner (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            title TEXT, 
                            comment TEXT  
                            );
                     """)


class Fill_db:

    def terminal(transaction_id, title, configuration):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Terminal (id, title, configuration)
                VALUES (?, ?, ?);""",
                           (transaction_id, title, configuration))
            print('trans ok')


    def payment(datetime, terminal_id, transaction_id, partner_id, summ):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Payment (
                datetime, terminal_id, transaction_id, partner_id, summ)
                VALUES (?, ?, ?, ?, ?);""",
                           (datetime, terminal_id, transaction_id, partner_id, summ))
            print('payment ok')


    def partner(title, comment):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Terminal (title, comment)
                VALUES (?, ?);""",
                           (title, comment))
            print('partner ok')


if __name__ == '__main__':
    Fill_db()