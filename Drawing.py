import cv2
import numpy


class Draw():
    def __init__(self):
        self.width = 100
        self.height = 100

    def open_image(self, image_path, new_width=100):
        image = cv2.imread(image_path)
        width, height, h = image.shape
        ratio = height / width
        new_height = int(new_width * ratio)
        image = cv2.resize(image, (new_height, new_width))
        self.width = new_width
        self.height = new_height

        return image

    def pencil_drawing(self, image_path, width=7, blur=7):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edge_mask = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, width, blur)

        return edge_mask

    def cartoon_maker(self, img, k):

        data = numpy.float32(img).reshape((-1, 3))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = numpy.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result


app = Draw()
resized_image = app.open_image('static/img/img.png', 720)
cv2.imwrite('static/img/processed_image.png', resized_image)
edge_mask = app.pencil_drawing('static/img/processed_image.png', 7, 7)
cartoon_image = app.cartoon_maker(resized_image, 9)
cartoon = cv2.bitwise_and(cartoon_image, cartoon_image, mask=edge_mask)
cv2.imshow('image', cartoon)
cv2.waitKey(0)