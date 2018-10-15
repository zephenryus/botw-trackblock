import os
import struct

from PIL import Image

logfile = open('log.txt', 'w+')
# background_map = Image.open("tracker-map.png")
background_map = Image.new("RGB", (12000, 12000), (255, 255, 255))


def read_trackblock(path):
    with open(path, 'rb') as infile:
        global logfile, background_map
        infile.seek(64)

        while True:
            pos = infile.tell()
            timestamp1, timestamp2 = struct.unpack('>2I8x', infile.read(16))

            if timestamp1 == 0 and timestamp2 == 0:
                break

            logfile.write(
                "{0}:{1}\ntimestamp1: {2} / timestamp2: {3}\n".format(
                    path,
                    hex(pos),
                    timestamp1,
                    timestamp2
                )
            )

            for _ in range(300):
                pos = infile.tell()
                data = struct.unpack('>I', infile.read(4))[0]
                y = data & 0xfff
                y_sign = (data & 0x1000) >> 0x0c
                x = (data & 0x1ffe000) >> 0x0d
                x_sign = (data & 0x2000000) >> 0x19
                flag = (data & 0xfc000000) >> 0x1a

                flag_0 = flag & 0b000001
                flag_1 = (flag & 0b000010) >> 1
                flag_2 = (flag & 0b000100) >> 2
                flag_3 = (flag & 0b001000) >> 3
                flag_4 = (flag & 0b010000) >> 4
                flag_5 = (flag & 0b100000) >> 5

                x = x if x_sign == 0 else -1 * x
                x = x if flag_0 == 0 else -1 * x

                y = y if y_sign == 0 else -1 * y

                logfile.write("{0}:{1}: {2} | ({3}, {4})\n".format(
                    path,
                    hex(pos),
                    hex(flag),
                    x,
                    y
                ))

                r = 0
                g = 0
                b = 0

                if flag_5 == 1:
                    r = 0
                    g = 179
                    b = 255
                else:
                    r = 255
                    g = 136
                    b = 0

                # if flag == 0x0:
                #     color = (0, 0, 0)
                # elif flag == 0x1:
                #     color = (255, 0, 0)
                # elif flag == 0x20:
                #     color = (0, 0, 0)
                # elif flag == 0x21:
                #     color = (255, 0, 0)
                # elif flag == 0x22:
                #     color = (0, 0, 0)
                # elif flag == 0x23:
                #     color = (0, 0, 0)
                # elif flag == 0x24:
                #     color = (0, 0, 0)
                # elif flag == 0x25:
                #     color = (0, 0, 0)
                # elif flag == 0x28:
                #     color = (0, 0, 0)
                # elif flag == 0x29:
                #     color = (0, 0, 0)
                # elif flag == 0x30:
                #     color = (0, 0, 0)
                # elif flag == 0x31:
                #     color = (0, 0, 0)

                color = (r, g, b)

                if color != (0, 0, 0):
                    background_map.putpixel((x + 6000, y + 6000), color)

            if infile.tell() >= 0xe440:
                break


def main():
    path = r"C:\botw-data\decompressed\save\80000001\tracker"
    print('Scanning {0}/'.format(path))

    for (dirpath, dirnames, filenames) in os.walk(path):
        directory = dirpath.replace('\\', '/') + '/'

        for filename in filenames:
            if filename == 'trackblock_hard00.sav':
                continue

            current_file = directory + filename
            read_trackblock(current_file)

    logfile.close()
    background_map.save('flag_5.tiff')


if __name__ == "__main__":
    main()
