import sys
import time
import json
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
                cprint(f'[*] Tentativo di connessione con {host}:{port}... ', 'yellow', end='')
                sock.connect((host, port))
            except TimeoutError:
                cprint('Timeout.', 'red')
                time.sleep(2)
            except ConnectionRefusedError:
                cprint('Connessione rifiutata.', 'red')
                time.sleep(2)
            else:
                cprint('Connessione riuscita.', 'green')
                break

        return cls(sock)

    @classmethod
    def get_server(cls, host, port):
        sock = socket()
        sock.bind((host, port))
        sock.listen()

        cprint(f'[*] In ascolto su porta {port}... ', 'yellow', end='')
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

        header = {
            'protocol': 'send_file',
            'filename': path.split('\\')[-1]
        }

        self.send(json.dumps(header).encode() + b'<END_OF_JSON_HEADER>' + data)


def tcp_to_file(data: bytes):
    split_data = data.split(b'<END_OF_JSON_HEADER>')
    header = json.loads(split_data[0])
    data_bytes = split_data[1]

    if header['protocol'] == 'send_file':
        with open(header['filename'], 'wb') as file:
            file.write(data_bytes)


def print_error(msg: str, block: bool = True):
    if block:
        input(colored(f'[!] {msg}...', 'red'))
    else:
        cprint(f'[!] {msg}.', 'red')


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
