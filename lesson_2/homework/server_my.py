import socketserver
import struct
from collections import namedtuple


class TCPHandler(socketserver.BaseRequestHandler):


    def handle(self):


        self.data = self.request.recv(1024)
        transaction_rsvd = struct.unpack('2s6s6s4s4s', self.data)
        Transaction = namedtuple('Transaction', ('tr_header', 'tr_date', 'tr_time', 'tr_type', 'tr_data'))
        data = Transaction(*transaction_rsvd)

        tr_header = data.tr_header.decode('cp1251')

        # дата
        trdate = int(data.tr_date, 16)
        tr_year = (trdate & 0xfe00) >> 9
        tr_month = (trdate &  0x1e0) >> 5
        tr_day = (trdate & 0x1f) & 31
        tr_decoded_date = '{}.{}.20{} '.format(tr_day, tr_month, tr_year)

        # тип транзакции
        if data.tr_type == b'0x00':
            tr_type = 'сервисная транзакция'

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


        msg = "Заголовок пакета: {}, дата: {}; тип транзакции: {}; данные: {}".format(
                                      tr_header, tr_decoded_date, tr_type, tr_data)

        print("От клиента {} получено: \n{}".format(self.client_address[0], msg))


HOST, PORT = 'localhost', 9999

server = socketserver.TCPServer((HOST, PORT), TCPHandler)
print('Сервер запущен')

server.serve_forever()
