import json
import os
import random
import ctypes
from PIL import Image
from flask import Flask, render_template, request


app = Flask(__name__)
current_image_path = ''
processed_image_path = ''


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
image_size = (int(screensize[0] * 0.6), 620)
print(image_size)


def resize_image(image_path, save_path, image_size):
    image = Image.open(image_path)
    new_image = image.resize(image_size)
    new_image.save(save_path)


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def base():
    global current_image_path, processed_image_path
    params = {'current_image': current_image_path, 'processed_image': processed_image_path}
    if request.method == 'GET':
        return render_template('main.html', **params)

    elif request.method == 'POST':
        processed_image_path = 'static/img/processed_image_path.jpg'
        current_image_path = 'static/img/current_image.jpg'
        filename = request.form['file']
        pth = 'C:\\'
        for root, dirnames, filenames in os.walk(pth):
            for file in filenames:
                if file == filename:
                    path = os.path.join(root, file)
        current_image = Image.open(path)
        current_image.save(current_image_path)
        resize_image(current_image_path, processed_image_path, image_size)
        return 'gg'



if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1")