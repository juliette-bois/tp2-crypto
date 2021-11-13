from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Question 3


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
    img.save(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("usage: {} image msg output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
