import os

def openFile():
    path = './sample.txt'

    mode = 0o666

    flags = os.O_RDWR | os.O_CREAT

    fd = os.open(path, flags, mode)

    print("File path opened successfully.")
