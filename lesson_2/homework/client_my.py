import socket
import struct
import random
import datetime


now = datetime.datetime.now()
# datetime.today() # текущая дата  00:00

# Данные транзакции

tr_header = b'zz'
tr_date = hex(((now.year - 2000 << 9) | (now.month << 5) | (now.day & 31)) & 0xFFFF).encode('utf-8')
tr_type = '0x00'.encode('utf-8')
data = ['0x00', '0x01', '0x02', '0x03', '0x04']
tr_data = random.choice(data).encode('utf-8')
transaction = struct.pack('2s6s6s4s4s', tr_header, tr_date, tr_type, tr_data)


HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall(transaction)
print('Данные отправлены')
sock.close()

