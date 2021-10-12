import sys
import time
import chardet
import colorama
from typing import Union
from socket import socket
from termcolor import cprint, colored


class BudaSocket:
    def __init__(self, sock: socket = None):
        self.sock: socket = socket() if sock is None else sock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    @classmethod
    def get_client(cls, host, port):
        sock = socket()

        while True:
            try:
                cprint(f'In attesa di connessione con {host}:{port}', 'yellow')
                sock.connect((host, port))
            except ConnectionRefusedError:
                time.sleep(2)
            else:
                cprint('Connessione riuscita', 'green')
                break

        return cls(sock)

    @classmethod
    def get_server(cls, host, port):
        sock = socket()
        sock.bind((host, port))
        sock.listen()

        cprint(f'In ascolto su porta {port}', 'yellow')
        conn, addr = sock.accept()
        cprint(f'Connessione accettata con {addr[0]}:{addr[1]}', 'green')

        return cls(conn)

    def recv(self, blocking: bool = False):
        self.sock.setblocking(blocking)

        if blocking:
            return self.sock.recv(4096)

        data = b''
        while True:
            try:
                buff = self.sock.recv(4096)
                data += buff
            except BlockingIOError:
                if data:
                    return data

    def recv_str(self):
        return decode(self.recv())

    def send(self, data: Union[str, bytes]):
        self.sock.sendall(data.encode() if type(data) is str else data)

    def send_file(self, path: str):
        with open(path, 'rb') as file:
            data = file.read()

        file_name = path.split('\\')[-1]
        header = f'<filename>{file_name}</filename>'

        self.send(header.encode() + data)


def print_error(msg: str, block: bool = True):
    if block:
        input(colored(f'[!] {msg}...', 'red'))
    else:
        cprint('[!] ' + msg, 'red')


def decode(data: bytes):
    enc = chardet.detect(data)['encoding']
    return data.decode(enc) if enc else data.decode()


def argv_or_default(argv_index: int, default):
    try:
        return sys.argv[argv_index]
    except IndexError:
        return default


def fix_white_spaces(string: str):
    return ' '.join(string.split())


colorama.init()