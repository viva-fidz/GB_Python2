import hashlib


def hesh_sum(line, algorithm):
    '''вычисление заданной хэш-суммы для строки 
    '''
    if algorithm == 'md5':
        h = hashlib.md5()
    elif algorithm == 'sha512':
        h = hashlib.sha512()
    elif algorithm == 'sha1':
        h = hashlib.sha1()
    line = line.encode('koi8-r')
    h.update(line)
    return h.hexdigest()


with open('need_hashes.csv', 'rb') as f:
    res = ''
    for line in f:
       hline = line.decode().split(';')
       hashed_line = '{}; {}; {}; {}'.format(
                   hline[0], hline[1], hesh_sum(hline[0], hline[1]), '\n')
       res += hashed_line


with open('need_hashes.csv', 'w') as f:
    f.write(res)


