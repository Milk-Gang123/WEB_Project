from PIL import Image
import pygame


class ASCIIConverter():
    def __init__(self):
        self.ascii_chars = [' ', '.', '+', '*', '~', 'x', '#', 'w', '%', '8', '@']
        self.font_size = 20
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.width = 100
        self.height = 100

    def resize_image(self, image, new_width=100):
        width, height = image.size
        ratio = height / width
        new_height = int(new_width * ratio)
        new_image = image.resize((new_width, new_height))
        self.width = new_width
        self.height = new_height
        return new_image

    def gray_image(self, image):
        new_image = image.convert('L')
        return new_image

    def pix_to_ascii(self, image):
        pixels = image.getdata()
        chars = []
        for i in pixels:
            chars.append(self.ascii_chars[i // 25])
        chars = ''.join(chars)
        list_chars = []
        for i in range(self.height):
            list_chars.append(chars[i * self.width: (i + 1) * self.width])

        return list_chars

    def draw_image(self, list_chars):
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill('black')
        for y in range(0, self.width, self.char_step):
            for x in range(0, self.height, self.char_step):
                try:
                    char = list_chars[x][-y]
                    rendered_char = self.font.render(char, False, (255, 255, 255))
                    screen.blit(rendered_char, (x, y))
                except Exception:
                    pass
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/processed_image_path.jpg')


app = ASCIIConverter()
image = Image.open('static/img/img.png')
resized_image = ASCIIConverter.resize_image(app, image, 800)
gray_image = ASCIIConverter.gray_image(app, resized_image)
list_chars = ASCIIConverter.pix_to_ascii(app, gray_image)
for i in list_chars:
    print(i)
ASCIIConverter.draw_image(app, list_chars)