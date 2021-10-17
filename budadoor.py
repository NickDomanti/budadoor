import sys
import getopt


def usage():
    print(f'Opzioni di {sys.argv[0]}:')
    print('-m, = modalità ("server" o "client")')
    print('-i, = indirizzo IP del server, da usare solo con "-m client"')
    print('-p, = porta del socket')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'm:i:p:')

        for opt, arg in opts:
            if opt == '-m':
                mode = arg
            elif opt == '-i':
                ip = arg
            elif opt == '-p':
                port = int(arg)

        if mode == 'client':
            import client
            client.run(ip, port)
        elif mode == 'server':
            import server
            server.run(port)
        else:
            usage()
    except ValueError:
        print('-p deve essere un numero intero')
    except (UnboundLocalError, IndexError, getopt.GetoptError):
        usage()


if __name__ == '__main__':
    main()
