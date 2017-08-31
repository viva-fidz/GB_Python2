import socketserver
import struct
from threading import Thread, current_thread
from collections import namedtuple
from random import randint
from db import Terminal, Payment, Partner


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024)
        transaction_rsvd = struct.unpack('!2s6s6s4s4s4s4s4s', self.data)

        Transaction = namedtuple('Transaction',
                                 ('tr_header', 'tr_date', 'tr_time', 'tr_type', 'tr_data', 'tr_transaction_id',
                                  'partner_id', 'payment'))
        data = Transaction(*transaction_rsvd)

        # дата
        trdate = int(data.tr_date, 16)
        tr_year = (trdate & 0xfe00) >> 9
        tr_month = (trdate & 0x1e0) >> 5
        tr_day = (trdate & 0x1f) & 31
        tr_decoded_date = '20{}-{}-{} '.format(tr_year, tr_month, tr_day)

        # время
        trtime = int(data.tr_time, 16)
        tr_hour = (trtime & 0x1f000) >> 12
        tr_min = (trtime & 0xfc0) >> 6
        tr_sec = trtime & 0x3f
        tr_decoded_time = tr_hour * 3600 + tr_min * 60 + tr_sec  # + 10800 for Moscow

        datetime = '{} {}:{}:{}'.format(tr_decoded_date, tr_hour, tr_min, tr_sec)

        # id транзакции
        tr_transaction_id = int(data.tr_transaction_id, 16)

        # тип транзакции
        tr_type = tr_data = str
        if data.tr_type == b'0x00':
            tr_type = 'сервисная транзакция'
        else:
            pass

        # данные транзакции
        if data.tr_data == b'0x00':
            tr_data = 'включение'
        elif data.tr_data == b'0x01':
            tr_data = 'перезагрузка'
        elif data.tr_data == b'0x02':
            tr_data = 'выключение'
        elif data.tr_data == b'0x03':
            tr_data = 'активация датчика X'
        elif data.tr_data == b'0x04':
            tr_data = 'блокировка, требуется инкассация'

        # id терминала
        terminal_id = randint(111, 999)

        partner_id = int(data.partner_id, 16)
        partner_name = "emobi"
        payment = int(data.payment, 16)
        cmnt = 'cmnt'

        msg = "Дата: {} {} терминал: {};\nтранзакция: id {}; тип: {}; данные: {}\n ".format(
            tr_decoded_date, tr_decoded_time, terminal_id, tr_transaction_id, tr_type, tr_data)
        print("Поток: {} \nОт клиента {} получено: \n{}".format(current_thread(), self.client_address[0], msg))

        t = Terminal()
        prt = Partner()
        pay = Payment()

        t.insert(terminal_id, tr_type, "'conf':'conf'")
        prt.insert(partner_id, partner_name, cmnt)
        pay.insert(datetime, terminal_id, tr_transaction_id, partner_id, payment)

        pay.get_all_data()
        t.get_total_sum(terminal_id)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
        Потоковый сервер. Достаточно создать класс без "внутренностей"
    """
    pass


if __name__ == "__main__":
    # Порт 0 позволяет выбрать незанятый порт автоматически
    ip, port = "localhost", 9999

    server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address
        # Запускаем поток для цикла сервера.
        # Этот поток будет создавать поток для каждого клиента
        server_thread = Thread(target=server.serve_forever,
                                         name='thread.server')
        cur_thread = current_thread()
        # Ставим флаг daemon, чтобы сервер завершился, когда завершится основная программа
        server_thread = Thread(target=server.serve_forever,
                                         name='thread.server')
        server_thread.daemon = True
        server_thread.start()
        print("Сервер запущен в потоке: {} по адресу {}:{}".format(server_thread.name, ip, port))

        server.serve_forever()
