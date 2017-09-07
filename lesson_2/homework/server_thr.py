import socketserver
from threading import Thread, current_thread
from db import Terminal, Payment, Partner
import sqlite3
from data_decoder import decoder


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # получаем данные транзакции
        self.data = self.request.recv(1024)

        # декодируем данные
        data = decoder(self.data)

        print("\nПоток: {} \nОт клиента {} получено: \n{}\n".format(current_thread(), self.client_address[0], data))

        # Заносим данные в БД

        t = Terminal()
        prt = Partner()
        pay = Payment()


        try:
            prt.insert(data.partner_id, data.partner_name, data.cmnt)
        except sqlite3.IntegrityError:
            print('partner exists')

        t.insert(data.terminal_id, data.tr_type, "'conf':'conf'")
        pay.insert(data.datetime, data.terminal_id, data.tr_transaction_id, data.partner_id, data.payment)

        pay.get_all_data()
        t.get_total_sum(data.terminal_id)


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
