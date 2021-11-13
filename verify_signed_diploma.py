import io
from OpenSSL.crypto import X509, verify
from PIL import Image
from OpenSSL import crypto
import base64
import cv2

# Question 5

# Public key
public_key_file = open("./public_key.pem", "r")
public_key = public_key_file.read()
public_key_file.close()

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


def verify_signature(signature, toverify):
    """
    :param signature:
    :type signature: bytes
    :param toverify: data to compare with signature
    :type toverify: bytes
    :return: void
    :rtype:
    """
    pkey = crypto.load_publickey(crypto.FILETYPE_PEM, public_key)
    x509 = X509()
    x509.set_pubkey(pkey)
    try:
        result = verify(x509, base64.b64decode(signature), toverify, "sha256")
        if result is None:
            print("Diploma Verified")
        else:
            print("Diploma not verified")
    except Exception:
        print("Diploma not verified")


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
    r, g, b, a = pixels[x, y]
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
    signature = read_hidden_text(img)
    # get data from qrcode
    qrimg = cv2.imread(filename)
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(qrimg)
    verify_signature(signature, bytes(DIPLOMA_PASS_PHRASE + val, 'UTF-8'))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
