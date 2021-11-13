import io
from PIL import Image, ImageFont, ImageDraw
import OpenSSL
from OpenSSL import crypto
import base64
import qrcode

# Question 4

# Private key
private_key_file = open("./.private_key.pem", "r")
private_key = private_key_file.read()
private_key_file.close()
password = "coucou"

DIPLOMA_PASS_PHRASE = '@@#123456#DIPLOMA_EXERCISE_PASSPHRASE#654321#@@'

def image_to_byte_array(image):
    """
    :param image:
    :type image: any
    :return:
    :rtype: bytearray
    """
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def sign(data):
    """
    :param data: data to sign
    :type data: str
    :return: A file signature
    :rtype: bytes
    """
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key, password.encode('ascii'))
    sign = OpenSSL.crypto.sign(pkey, bytes(DIPLOMA_PASS_PHRASE + data, 'UTF-8'), "sha256")
    return base64.b64encode(sign)


def hide_text(img, text):
    """
    :param img:
    :type img: any
    :param text:
    :type text: bytes
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
            store_bytes_in_pixel(pixels, x, y, text[i])
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
    r, g, b, a = pixels[x, y]
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


def add_text(img, text, x, y, size):
    """
    :param img:
    :type img: any
    :param text:
    :type text: str
    :param x: the X position on the img
    :type x: int
    :param y: the Y position on the img
    :type y: int
    :param size: Font size
    :type size: int
    :return: void
    :rtype:
    """
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("images/sans.ttf", size)
    draw.text((x, y), text, "black", font)


def add_QR_code(img, data):
    """
    :param img:
    :type img: any
    :param data:
    :type data:
    :return:
    :rtype:
    """
    qrimg = qrcode.make(data)
    type(qrimg)  # qrcode.image.pil.PilImage
    img.paste(qrimg.resize((130, 130)))


def main(name, average, output):
    """
    :param name: Name of student
    :type name: str
    :param average:
    :type average: float
    :param output: Diploma
    :type output: str
    :return: void
    :rtype:
    """
    img = Image.open('images/diplome-BG.png')  # ouverture de l'image contenue dans un fichier
    add_text(img, 'Diplôme', 350, 150, 60)
    add_text(img, 'Master d\'origami', 310, 250, 40)
    add_text(img, name + ' à réussi la formation', 230, 350, 32)
    add_text(img, 'avec une moyenne de ' + str(average), 300, 420, 25)
    data = name + ',' + str(average)
    add_QR_code(img, data)
    signature = sign(data)
    hide_text(img, signature)
    img.save(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("usage: {} image msg output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
