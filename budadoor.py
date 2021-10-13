import sys


def usage():
    print('Utilizzo corretto:')
    print('budadoor server <port>')
    print('budadoor client <server_ip> <port>')


def main():
    try:
        method = sys.argv[1]
        if method == 'client':
            import client
            client.run(sys.argv[2], int(sys.argv[3]))
        elif method == 'server':
            import server
            server.run(int(sys.argv[2]))
        else:
            usage()
    except ValueError:
        print('Il parametro "port" deve essere un numero intero')
    except IndexError:
        usage()


if __name__ == '__main__':
    main()
