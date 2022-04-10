from PIL import Image


class ImageFilter:
    def __init__(self):
        self.pixel_size = 10
        self.fields = ['Размер пикселя']

    def field_1(self, new_pixel_size):
        if new_pixel_size in range(0, 100):
            self.pixel_size = new_pixel_size

    def make_image(self, file):
        image = Image.open(file)
        image_width, image_height = image.size
        image = image.resize((image_width // self.pixel_size, image_height // self.pixel_size), Image.NEAREST)
        image = image.resize((image_width, image_height), Image.NEAREST)
        image.save('static/img/processed_image.png')
