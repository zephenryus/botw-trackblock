import math
import os
import struct

logfile = open('log.txt', 'w+')
previous = 0
count = 0
deltaSum = 0
average = 0


def read_trackblock(path):
    with open(path, 'rb') as infile:
        global logfile, previous, count, deltaSum, average
        infile.seek(64)

        while True:
            infile.seek(12, 1)
            pos = infile.tell()

            logfile.write("{0}:{1} - {2}\n".format(
                path,
                hex(pos),
                hex(struct.unpack('>I', infile.read(4))[0])
            ))

            infile.seek(0x4b0, 1)

            if infile.tell() >= 0xe440:
                break


def main():
    path = r"C:\botw-data\decompressed\save\80000001\tracker"
    print('Scanning {0}/'.format(path))

    for (dirpath, dirnames, filenames) in os.walk(path):
        directory = dirpath.replace('\\', '/') + '/'

        for filename in filenames:
            current_file = directory + filename
            read_trackblock(current_file)


    logfile.close()


if __name__ == "__main__":
    main()
