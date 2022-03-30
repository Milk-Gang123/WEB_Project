from PIL import Image
import pygame


class ASCIIConverter():
    def __init__(self, width, height, font_size):
        self.ascii_chars = [' ', '.', '+', '*', '~', 'x', '#', 'w', '%', '8', '@']
        self.font_size = font_size
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.width = width
        self.height = height

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

    def draw_image(self, list_chars, route):
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
        pygame.image.save(screen, route)


class Colored_ASCII(ASCIIConverter):
    def __init__(self, width, height, font_size):
        self.font_size = font_size
        pygame.font.init()
        self.font = pygame.font.SysFont('arial', self.font_size, bold=True)
        self.char_step = int(self.font_size * 0.6)
        self.width = width
        self.height = height
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
                    rendered_char = pygame.transform.rotate(rendered_char, -90)
                    screen.blit(rendered_char, (x, y))
                except Exception:
                    pass
        screen = pygame.transform.rotate(screen, -90)
        pygame.image.save(screen, 'static/img/carousel_1.png')


if __name__ == "__main__":
    app = Colored_ASCII(720, 480, 8)
    image = Image.open('static/img/img.png')
    resized_image = app.resize_image(image, app.width)
    gray_image = app.gray_image(resized_image)
    list_chars = app.pix_to_ascii(gray_image)
    list_colors = app.get_palette(resized_image)
    app.draw_image(list_chars, list_colors)