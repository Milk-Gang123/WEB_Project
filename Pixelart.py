from PIL import Image


def make_pixel_art(file, pixel_size):
        image = Image.open(file)
        image_width, image_height = image.size
        image = image.resize((image_width // pixel_size, image_height // pixel_size), Image.NEAREST)
        image = image.resize((image_width, image_height), Image.NEAREST)
        image.save('static/img/processed_image_path.png')


make_pixel_art('static/img/filter_page_background.png', 8)