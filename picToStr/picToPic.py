from PIL import Image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("file", help = 'the path of input file')
parser.add_argument("-W", "--width", help = 'the width of output', type = int, default = 80)
parser.add_argument("-H", "--height", help = 'the length of output', type = int, default= 80)
parser.add_argument("-O", "--output", help = "the path of output file")
parser.add_argument("-V", "--verbose", help = 'increase the output verbosity', action = "store_true")

args = parser.parse_args()
ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def getChar(r, g, b, alpha = 256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

def main():
    im = Image.open(args.file)
    im.resize((args.width, args.height), resample = Image.NEAREST)
    txt = ''
    for i in range(args.width):
        for j in range(args.height):
            txt += getChar(*im.getpixel((i, j)))
        txt += '\n'
    print(txt)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(txt)
    else:
        with open('./output.txt', 'w') as f:
            f.write(txt)
if __name__ == "__main__":
    main()    
