import socket
import struct
import random
import datetime


now = datetime.datetime.now()


def id_gen(int_from=1111, int_to=9999):
    """Генерирует случайное число в заданом диапазоне 
     transaction_id
    """
    m = [i for i in range(int_from, int_to)]
    random.shuffle(m)
    for id in m:
        yield id


for id in id_gen():
    transaction_id = id


# Данные транзакции
tr_header = b'zz'
tr_date = hex(((now.year - 2000 << 9) | (now.month << 5) | (now.day & 31)) & 0xFFFF).encode('utf-8')
tr_time =  hex((now.hour << 12) | (now.minute << 6) | (now.second & 60)).encode('utf-8')
tr_type = '0x00'.encode('utf-8')
data = ['0x00', '0x01', '0x02', '0x03', '0x04']
tr_data = random.choice(data).encode('utf-8')

transaction_id = hex(transaction_id).encode('utf-8')

transaction = struct.pack('2s6s6s4s4s6s', tr_header, tr_date, tr_time, tr_type, tr_data, transaction_id)


HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))
sock.sendall(transaction)
print('Данные отправлены')
sock.close()

