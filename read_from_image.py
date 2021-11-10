from PIL import Image

def read_from_pixel(pixels, x, y):
    return chr(read_bytes_from_pixel(pixels, x, y))

def read_bytes_from_pixel(pixels, x, y):
    r, g, b = pixels[x, y]
    return (0b00001111 & r) | ((0b00001111 & g) << 4)

def read_hidden(img):
    pixels = img.load()  # tableau des pixels
    y = 0
    i = 0
    bsize = bytearray()
    bsize.append(read_bytes_from_pixel(pixels, 0, y))
    bsize.append(read_bytes_from_pixel(pixels, 1, y))
    bsize.append(read_bytes_from_pixel(pixels, 2, y))
    bsize.append(read_bytes_from_pixel(pixels, 3, y))
    text_size = int.from_bytes(bsize, "big")
    x = 4
    text = ''
    while i < text_size and y < img.height:
        while i < text_size and x < img.width:
            text += read_from_pixel(pixels, x, y)
            x += 1
            i += 1
        x = 0
        y += 1
    return text

def main(filename):
    img = Image.open(filename)  # ouverture de l'image contenue dans un fichier
    text = read_hidden(img)
    print(text)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])