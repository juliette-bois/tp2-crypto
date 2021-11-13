import io

import OpenSSL
from OpenSSL.crypto import X509, verify
from PIL import Image
from OpenSSL import crypto
import base64

# Question 2

# Private key
private_key_file = open("./.private_key.pem", "r")
private_key = private_key_file.read()
private_key_file.close()
password = "coucou"

# Public key
public_key_file = open("./public_key.pem", "r")
public_key = public_key_file.read()
public_key_file.close()


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


def sign(file):
    """
    :param file: file to sign
    :type file: any
    :return: A file signature
    :rtype: bytes
    """
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key, password.encode('ascii'))
    sign = OpenSSL.crypto.sign(pkey, image_to_byte_array(file), "sha256")
    return base64.b64encode(sign)


def verify_signature(file, signature):
    """
    :param file:
    :type file: any
    :param signature:
    :type signature: bytes
    :return: void
    :rtype:
    """
    pkey = crypto.load_publickey(crypto.FILETYPE_PEM, public_key)
    x509 = X509()
    x509.set_pubkey(pkey)
    result = verify(x509, base64.b64decode(signature), image_to_byte_array(file), "sha256")
    if result is None:
        print("Verified OK")
    else:
        print("Signature not verified")


def main(filename):
    """
    :param filename: file path to image
    :type filename: str
    :return: void
    :rtype:
    """
    img = Image.open(filename)
    signature = sign(img)
    verify_signature(img, signature)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} image msg output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
