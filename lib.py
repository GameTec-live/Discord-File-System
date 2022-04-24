import binascii
import os

def cleanup(file_number):
    for i in range(1, file_number):
        os.remove("split_" + str(i))
    try:
        os.remove("tmp.hex")
    except:
        pass
    os.remove("index.txt")


def encode(file_name):
    file = file_name
    CHUNK_SIZE = 500000
    file_number = 1

    with open(file, "rb") as f:
        data = f.read()
        data = binascii.hexlify(data)

    with open("tmp.hex", "wb") as f:
        f.write(data)

    with open("tmp.hex", "rb") as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            with open('split_' + str(file_number), "wb") as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(CHUNK_SIZE)
    with open("index.txt", "w") as f:
        f.write(str(file_number) + "\n")
        f.write(str(file) + "\n")

    os.remove("tmp.hex")
    os.remove(file)

def decode(index):
    with open(index, "r") as f:
        file_number = int(f.readline())
        file_name = f.readline()
        file_name = file_name.rstrip()

    with open("tmp.hex", "wb") as f:
        for i in range(1, file_number):
            with open("split_" + str(i), "rb") as chunk_file:
                chunk = chunk_file.read()
                f.write(chunk)

    with open("tmp.hex", "rb") as f:
        data = f.read()
        data = binascii.unhexlify(data)
    with open(file_name, "wb") as f:
        f.write(data)

    cleanup(file_number)

