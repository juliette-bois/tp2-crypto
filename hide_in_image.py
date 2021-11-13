from PIL import Image


# Question 1 : cacher un message dans une image

def hide_text(img, text):
    """
    :param img:
    :type img: any
    :param text:
    :type text: str
    :return: void
    :rtype:
    """
    text_size = len(text)
    i = 0
    y = 0
    pixels = img.load()  # tableau des pixels

    # afin d'éviter d'utiliser un paramètre nb_bytes,
    # on stocke la taille du texte dans les 4 premiers pixels de l'image
    # car on en a besoin pour récupérer les données à la lecture
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
    """
    :param pixels: image pixels array
    :type pixels: :ref:`PixelAccess` or :py:class:`PIL.PyAccess`
    :param x: pixel X position
    :type x: int
    :param y: pixel Y position
    :type y: int
    :param bytes: current written byte
    :type bytes: byte
    :return: void
    :rtype:
    """
    r, g, b = pixels[x, y]
    r = (r & 0b11110000) | (bytes & 0b00001111)
    g = (g & 0b11110000) | (bytes >> 4)
    pixels[x, y] = r, g, b


def store_in_pixel(pixels, x, y, char):
    """
    :param pixels: image pixels array
    :type pixels: :ref:`PixelAccess` or :py:class:`PIL.PyAccess`
    :param x: pixel X position
    :type x: int
    :param y: pixel Y position
    :type y: int
    :param char: current written char
    :type char: char
    :return: void
    :rtype:
    """
    store_bytes_in_pixel(pixels, x, y, ord(char))


def main(filename, output, text):
    """
    :param filename: file path to image
    :type filename: str
    :param output: file path to output image
    :type output: str
    :param text: message to hide
    :type text: str
    :return: void
    :rtype:
    """
    img = Image.open(filename)  # ouverture de l'image contenue dans un fichier
    hide_text(img, text)
    img.save(output)  # sauvegarde de l'image obtenue dans un autre fichier


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
