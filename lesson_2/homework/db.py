import sqlite3

with sqlite3.connect('company.db3') as conn:
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    cursor.execute("""
                     CREATE TABLE if not exists Terminal (
                            id  INTEGER primary key, 
                            title TEXT, 
                            configuration TEXT,
                            comment TEXT,
                            pub_key TEXT   
                            );
                     """)
    cursor.execute("""               
                     CREATE TABLE if not exists Payment (
                            id  INTEGER primary key, 
                            datetime DATETIME, 
                            terminal_id  INTEGER,
                            transaction_id  INTEGER,
                            partner_id  INTEGER,
                            summ INTEGER
                            );
                     """)
    cursor.execute("""
                     CREATE TABLE if not exists Partner (
                            id  INTEGER primary key, 
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
            print('db ok')

    def payment(id, datetime, terminal_id, transaction_id, partner_id, summ):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Payment (
                id, datetime, terminal_id, transaction_id, partner_id, summ)
                VALUES (?, ?, ?, ?, ?, ?);""",
                           (id, datetime, terminal_id, transaction_id, partner_id, summ))

    def partner(id, title, comment):
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                insert into Terminal (id, title, comment)
                VALUES (?, ?, ?);""",
                           (id, title, comment))



if __name__ == '__main__':
    pass
