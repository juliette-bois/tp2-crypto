from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def add_text(img, text, x, y, size):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("images/sans.ttf", size)
    draw.text((x, y), text, "black", font)


def main(name, average, output):
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