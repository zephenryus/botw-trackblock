import os
import struct

from PIL import Image, ImageDraw

logfile = open('log.txt', 'w+')
background_map = Image.open("tracker-map.png")
# background_map = Image.new("RGB", (12000, 12000), (0, 0, 0))

last_point_stack = [
    {
        'xy': (0, 0),
        'type': -1
    },
    {
        'xy': (0, 0),
        'type': -1
    },
    {
        'xy': (0, 0),
        'type': -1
    },
    {
        'xy': (0, 0),
        'type': -1
    },
    {
        'xy': (0, 0),
        'type': -1
    }
]

draw_line = False


def add_point(last_point):
    last_point_stack[4] = last_point_stack[3]
    last_point_stack[3] = last_point_stack[2]
    last_point_stack[2] = last_point_stack[1]
    last_point_stack[1] = last_point_stack[0]
    last_point_stack[0] = last_point


def read_trackblock(path):
    with open(path, 'rb') as infile:
        global logfile, background_map, last_point_stack, draw_line
        print("Reading {0}...".format(path))

        infile.seek(64)

        stop_after = 5

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
                x = (data & 0x1ffe000) >> 13
                flag = (data & 0xfc000000) >> 26

                # print("({0}, {1})".format(x, y))

                flag_0 = (data & 0x1000) >> 12
                flag_1 = (data & 0x2000000) >> 25
                flag_2 = flag & 0b000001
                flag_3 = (flag & 0b000010) >> 1
                flag_4 = (flag & 0b000100) >> 2
                flag_5 = (flag & 0b001000) >> 3
                flag_6 = (flag & 0b010000) >> 4
                flag_7 = (flag & 0b100000) >> 5

                point_type = 0

                if flag_3 == 1:
                    point_type = 3
                if flag_4 == 1:
                    point_type = 4
                if flag_5 == 1:
                    point_type = 5

                # logfile.write("{0}:{1}: {2} | ({3}, {4})\n".format(
                #     path,
                #     hex(pos),
                #     hex(flag),
                #     x,
                #     y
                # ))

                r = 0
                g = 255
                b = 108

                if flag_1 == 1:
                    x += 4096

                if flag_0 == 0 and flag_2 == 0:
                    pass

                if flag_0 == 1 and flag_2 == 0:
                    y *= -1

                if flag_0 == 0 and flag_2 == 1:
                    x *= -1

                if flag_0 == 1 and flag_2 == 1:
                    x *= -1
                    y *= -1

                color = (r, g, b, 64)

                if flag_7:
                    draw_line = True

                    # if last_point_stack[0]['type'] in [-1, 4]:
                    #     print('last: {0}, current: {1}'.format(last_point_stack[0]['type'], point_type))
                    #     color = (r, g, b, 0)

                    if last_point_stack[0]['type'] == 5:
                        draw_line = False

                    if last_point_stack[0]['type'] == 4:
                        color = (0, 255, 255, 255)  # blue
                        background_map.putpixel((x + 5999, y + 5999), color)
                        background_map.putpixel((x + 6000, y + 5999), color)
                        background_map.putpixel((x + 6001, y + 5999), color)
                        background_map.putpixel((x + 5999, y + 6000), color)
                        background_map.putpixel((x + 6000, y + 6000), color)
                        background_map.putpixel((x + 6001, y + 6000), color)
                        background_map.putpixel((x + 5999, y + 6001), color)
                        background_map.putpixel((x + 6000, y + 6001), color)
                        background_map.putpixel((x + 6001, y + 6001), color)

                    if draw_line:
                        draw = ImageDraw.Draw(background_map, 'RGBA')
                        draw.line([last_point_stack[0]['xy'], (x + 6000, y + 6000)], fill=color, width=3)
                        del draw

                    # background_map.putpixel((x + 6000, y + 6000), color)

                    if flag_3 == 1 or flag_4 == 1 or flag_5:
                        if flag_3 == 1:
                            color = (204, 0, 255, 255)  # purple
                        if flag_4 == 1:
                            color = (0, 255, 255, 255)  # blue
                        if flag_5 == 1:
                            color = (255, 0, 0, 255)  # red
                        background_map.putpixel((x + 5999, y + 5999), color)
                        background_map.putpixel((x + 6000, y + 5999), color)
                        background_map.putpixel((x + 6001, y + 5999), color)
                        background_map.putpixel((x + 5999, y + 6000), color)
                        background_map.putpixel((x + 6000, y + 6000), color)
                        background_map.putpixel((x + 6001, y + 6000), color)
                        background_map.putpixel((x + 5999, y + 6001), color)
                        background_map.putpixel((x + 6000, y + 6001), color)
                        background_map.putpixel((x + 6001, y + 6001), color)

                    last_point = {
                        'xy': (x + 6000, y + 6000),
                        'type': point_type
                    }

                    add_point(last_point)

            if infile.tell() >= 0xe440:
                break

            stop_after -= 1
            if stop_after <= 0:
                break


def main():
    # path = r"C:\botw-data\decompressed\save\80000001\tracker"
    #     # print('Scanning {0}/'.format(path))
    #     #
    #     # for (dirpath, dirnames, filenames) in os.walk(path):
    #     #     directory = dirpath.replace('\\', '/') + '/'
    #     #
    #     #     for filename in filenames:
    #     #         if filename == 'trackblock_hard00.sav':
    #     #             continue
    #     #
    #     #         current_file = directory + filename
    #     #         read_trackblock(current_file)

    read_trackblock(r"C:\botw-data\decompressed\save\80000001\tracker\trackblock00.sav")

    logfile.close()
    background_map.save('output/test.tiff')


if __name__ == "__main__":
    main()
