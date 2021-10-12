import os.path

import helpers as hlp
from termcolor import cprint
from helpers import BudaSocket

if __name__ == '__main__':
    host = '0.0.0.0'
    port = hlp.argv_or_default(1, 12345)

    with BudaSocket.get_server(host, port) as server:
        try:
            while True:
                cwd = server.recv_str()

                if not cwd:
                    hlp.print_error('Nessuna risposta dal client')
                    break

                while True:
                    cmd = input(cwd + '>').strip()

                    if cmd.startswith('sendfile'):
                        if cmd == 'sendfile':
                            print('Percorso file mancante\n')
                        else:
                            path = cmd.removeprefix('sendfile').lstrip()
                            if os.path.isfile(path):
                                server.send_file(path)
                                break
                            else:
                                print('Percorso file inesistente\n')
                    else:
                        server.send(cmd)
                        break

                if cmd == 'gn':
                    cprint('Buonanotte', 'magenta')
                    break
                elif cmd == 'exit':
                    cprint('Chiusura server, client rimane acceso', 'green')
                    break

                print(server.recv_str())
        except ConnectionResetError:
            hlp.print_error('Connessione resettata dal client')
        except ConnectionRefusedError:
            hlp.print_error('Connessione rifiutata dal client')
