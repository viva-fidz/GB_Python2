import sqlite3

with sqlite3.connect('company.db3') as conn:
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()

    cursor.execute("""DROP table if exists Terminal""")
    cursor.execute("""DROP table if exists Partner""")
    cursor.execute("""DROP table if exists Payment""")

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
                            summ INTEGER,
                            FOREIGN KEY (terminal_id) REFERENCES Terminal(id) ON DELETE CASCADE,
                            FOREIGN KEY (partner_id) REFERENCES Partner(id) ON DELETE CASCADE
                            );
                     """)

    cursor.execute("""
                     CREATE TABLE if not exists Partner (
                            id INTEGER PRIMARY KEY, 
                            title TEXT, 
                            comment TEXT  
                            );
                     """)


    class Fill_db:
        def terminal(terminal_id, title, configuration):
            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                     insert into Terminal (id, title, configuration)
                     VALUES (?, ?, ?);""",
                               (terminal_id, title, configuration))
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

        def partner(partner_id, title, comment):
            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                 insert into Partner (id, title, comment)
                 VALUES (?, ?, ?);""",
                               (partner_id, title, comment))
                print('partner ok')

        def delete_from_partner(partner_id):
            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                         delete from Partner where id = ?;""",
                               (partner_id,))  # (key, value))
                print('partner id={} delete ok'.format(partner_id))


        def delete_from_terminal(terminal_id):
            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                          delete from Terminal where id = ?;""",
                               (terminal_id,))
                # print(terminal_id)
                print('terminal id={} delete ok'.format(terminal_id))


        def delete_from_payment(transaction_id):
            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                         delete from Payment where id = ?;""",
                               (transaction_id,))
                print('payment delete ok')


        def get_partners_total_sum():
            '''формирует выборку с итоговой задолжностью
            перед каждым из партнёров
            '''

            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                            select title, sum(summ) from Payment
                            inner join Partner on Payment.partner_id = Partner.id
                            group by title"""),
                output = cursor.fetchone()

                while output:
                    print(output)
                    output = cursor.fetchone()


        def get_terminal_total_sum(terminal_id):
            """Общая суммма прошедших через указанный терминал средств
            """

            with sqlite3.connect('company.db3') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                        select sum(summ) from Payment where terminal_id = ?; """,
                               (terminal_id,))

            print('terminal_id =', terminal_id, 'sum =', cursor.fetchone())

