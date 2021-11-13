from PIL import Image


# Question 1 : récupérer le message caché dans l'image

def read_from_pixel(pixels, x, y):
    """
    :param pixels: image pixels array
    :type pixels: :ref:`PixelAccess` or :py:class:`PIL.PyAccess`
    :param x: pixel X position
    :type x: int
    :param y: pixel Y position
    :type y: int
    :return: the character hidden in the pixel
    :rtype: str
    """
    return chr(read_bytes_from_pixel(pixels, x, y))


def read_bytes_from_pixel(pixels, x, y):
    """
    :param pixels: image pixels array
    :type pixels: :ref:`PixelAccess` or :py:class:`PIL.PyAccess`
    :param x: pixel X position
    :type x: int
    :param y: pixel Y position
    :type y: int
    :return: ASCII value of the character
    :rtype: int
    """
    r, g, b = pixels[x, y]
    return (0b00001111 & r) | ((0b00001111 & g) << 4)


def read_hidden_text(img):
    """
    :param img:
    :type img: any
    :return: the hidden message
    :rtype: str
    """
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
    """
    :param filename: file path to image
    :type filename: str
    :return: void
    :rtype:
    """
    img = Image.open(filename)  # ouverture de l'image contenue dans un fichier
    text = read_hidden_text(img)
    print(text)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
