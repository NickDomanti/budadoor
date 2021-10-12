import PyInstaller.__main__

if __name__ == '__main__':
    args = ['server.py', '-F', '--specpath', './specs']
    PyInstaller.__main__.run(args)

    args[0] = 'client.py'
    PyInstaller.__main__.run(args)
