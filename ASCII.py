import random

from PIL import Image
import pygame


class ASCIIConverter():
    def __init__(self):
        self.ascii_chars = [' ', '.', '+', '*', '~', 'x', '#', 'w', '%', '8', '@']
        self.font_size = 12
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
            list_chars.append(chars[i * self.width:(i + 1) * self.width])

        return list_chars

    def draw_image(self, list_chars):
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill('black')
        for y in range(0, self.width, self.char_step):
            for x in range(0, self.height, self.char_step):
                try:
                    char = list_chars[x][-y]
                    rendered_char = self.font.render(char, False, (255, 255, 255))
                    rendered_char = pygame.transform.rotate(rendered_char, -90)
                    screen.blit(rendered_char, (x, y))
                except Exception:
                    pass
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/processed_image_path.jpg')


class Colored_ASCII(ASCIIConverter):
    def __init__(self):
        self.font_size = 2
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.width = 100
        self.height = 100
        self.ascii_chars = [' ', ':', 'o', 'x', '#', '&', '$', '&', 'W', '8', '@']

    def get_palette(self, image):
        list_colors = []
        colors = []
        pixels = image.getdata()
        for i in pixels:
            colors.append(i)
        for i in range(self.height):
            list_colors.append(colors[i * self.width:(i + 1) * self.width])

        return list_colors

    def draw_image(self, list_chars, list_colors):
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill('black')
        for y in range(0, self.width, self.char_step):
            for x in range(0, self.height, self.char_step):
                try:
                    char = list_chars[x][-y]
                    char_color = list_colors[x][-y]
                    rendered_char = self.font.render(char, False, char_color)
                    rendered_char = pygame.transform.rotate(rendered_char, -270)
                    screen.blit(rendered_char, (x, y))
                except Exception:
                    pass
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/processed_image_path.jpg')

    def draw_pixel_art(self, list_colors):
        screen = pygame.display.set_mode((self.height, self.width))
        screen.fill('black')
        for y in range(0, self.width, self.char_step):
            for x in range(0, self.height, self.char_step):
                try:
                    char_color = list(list_colors[x][-y])
                    rendered_char = self.font.render('▓', False, tuple(char_color))
                    rendered_char = pygame.transform.rotate(rendered_char, -270)
                    screen.blit(rendered_char, (x, y))
                except Exception as e:
                    print(e)
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/processed_image_path.jpg')





app = ASCIIConverter()
color_app = Colored_ASCII()
image = Image.open('static/img/img.png')
resized_image = color_app.resize_image(image, 720)
gray_image = color_app.gray_image(resized_image)
list_chars = color_app.pix_to_ascii(gray_image)
list_colors = color_app.get_palette(resized_image)
color_app.draw_pixel_art(list_colors)

# app = ASCIIConverter()
# color_app = Colored_ASCII()
# image = Image.open('static/img/img.png')
# resized_image = app.resize_image(image, 720)
# gray_image = app.gray_image(resized_image)
# list_chars = app.pix_to_ascii(gray_image)
# app.draw_image(list_chars)