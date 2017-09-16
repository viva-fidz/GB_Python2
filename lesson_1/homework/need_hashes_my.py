import hashlib


def hash_sum(line, algorithm):
    """вычисление заданной хэш-суммы для строки
    """
    if algorithm == 'md5':
        h = hashlib.md5()
    elif algorithm == 'sha512':
        h = hashlib.sha512()
    elif algorithm == 'sha1':
        h = hashlib.sha1()
    line = line.encode()
    h.update(line)
    return h.hexdigest()


if __name__ == '__main__':

    with open('need_hashes.csv', 'rb') as f:
        res = ''
        for line in f:
            hline = line.decode().split(';')
            hashed_line = '{}; {}; {}; {}'.format(
                hline[0], hline[1], hash_sum(hline[0], hline[1]), '\n')
            res += hashed_line

    with open('need_hashes.csv', 'w') as f:
        f.write(res)
