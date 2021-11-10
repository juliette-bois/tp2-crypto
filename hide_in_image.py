from PIL import Image


def hide_text(img, text):
    text_size = len(text)
    i = 0
    y = 0
    pixels = img.load()  # tableau des pixels

    bytes = text_size.to_bytes(4, 'big')
    store_bytes_in_pixel(pixels, 0, y, bytes[0])
    store_bytes_in_pixel(pixels, 1, y, bytes[1])
    store_bytes_in_pixel(pixels, 2, y, bytes[2])
    store_bytes_in_pixel(pixels, 3, y, bytes[3])
    x = 4
    while i < text_size and y < img.height:
        while i < text_size and x < img.width:
            store_in_pixel(pixels, x, y, text[i])
            x += 1
            i += 1
        x = 0
        y += 1

def store_bytes_in_pixel(pixels, x, y, bytes):
    r, g, b = pixels[x, y]
    r = (r & 0b11110000) | bytes
    g = (g & 0b11110000) | (bytes >> 4)
    pixels[x, y] = r, g, b

def store_in_pixel(pixels, x, y, char):
    store_bytes_in_pixel(pixels, x, y, ord(char))

def main(filename, output, text):
    img = Image.open(filename)  # ouverture de l'image contenue dans un fichier
    hide_text(img, text)
    img.save(output)  # sauvegarde de l'image obtenue dans un autre fichier



if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
