from PIL import Image
import pygame


class ASCIIConverter():
    def __init__(self, font_size):
        self.ascii_chars = [' ', '.', '+', '*', '~', 'x', '#', 'w', '%', '8', '@']
        self.font_size = font_size
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
            chars.append(self.ascii_chars[i // len(self.ascii_chars)])
        chars = ''.join(chars)
        list_chars = []
        for i in range(self.height):
            list_chars.append(chars[i * self.width:(i + 1) * self.width])

        return list_chars


class ImageFilter(ASCIIConverter):
    def __init__(self):
        self.font_size = 10
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.width = 100
        self.height = 100
        self.ascii_chars = [' ', ':', 'o', 'x', '#', '&', '$', '&', 'W', '8', '@']
        self.fields = [['Размер шрифта', self.font_size, 1], ['Набор символов', self.ascii_chars, 2]]

    def field_1(self, new_font_size):
        self.font_size = int(new_font_size)
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        print(self.font_size)
        print(self.font)
        print(self.char_step)


    def field_2(self, new_ascii_chars):
        s = []
        for i in new_ascii_chars:
            s.append(i)
        self.ascii_chars = s

    def draw_image(self, list_chars):
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill('black')
        for y in range(0, self.width, self.char_step):
            for x in range(0, self.height, self.char_step):
                try:
                    char = list_chars[x][-y]
                    print(char)
                    rendered_char = self.font.render(char, False, (255, 255, 255))
                    rendered_char = pygame.transform.rotate(rendered_char, -90)
                    screen.blit(rendered_char, (x, y))
                except Exception:
                    pass
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/processed_image.png')

    def make_image(self, file):
        image = Image.open(file)
        image_width, image_height = image.size
        self.width, self.height = image_width, image_height
        resized_image = self.resize_image(image, self.width)
        gray_image = self.gray_image(resized_image)
        list_chars = self.pix_to_ascii(gray_image)
        self.draw_image(list_chars)