from pprint import pprint
from random import randint
from typing import Dict, List, Union, Callable
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import pytesseract


class ImgScanner(object):
    TextBox = Dict[str, Union[int, str]]
    TextData = List[TextBox]
    cfg = r'--oem 3 --psm 3 -l rus+eng'
    kernel = np.ones((2, 2), np.uint8)

    def __init__(self):

        self.image = None

        # Колонки получаемые из таблицы с данными о кадре
        self._data_col = ['text', 'left', 'top', 'width', 'height', 'conf']

        # Стандартные параметры рамки
        self._border_margin = 5
        self._border_color = (0, 0, 255)  # красный
        self._border_thick = 2

    # Получить информацию о тексте на кадре
    def get_text_data(self) -> TextData:

        # бинаризация
        transformed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        transformed_image = cv2.threshold(transformed_image, 200, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # удаление шумов
        # self.transformed_image = cv2.dilate(self.transformed_image, self.kernel, iterations=1)
        # self.transformed_image = cv2.erode(self.transformed_image, self.kernel, iterations=1)
        # self.transformed_image = cv2.morphologyEx(self.transformed_image, cv2.MORPH_CLOSE, self.kernel)
        # self.transformed_image = cv2.GaussianBlur(self.transformed_image, (5, 5), 0)
        # self.transformed_image = cv2.bilateralFilter(self.transformed_image, 15, 75, 75)
        # self.transformed_image = cv2.dilate(self.transformed_image, self.kernel, iterations=1)

        if self.image is not None:
            boxes = pytesseract.image_to_data(transformed_image, config=self.cfg,
                                              output_type=pytesseract.Output.DICT)
            text_data = [{key: boxes[key][i] for key in self._data_col}
                         for i, txt in enumerate(boxes['text']) if not txt.isspace() and txt]

            return text_data

    # Обвести все слова(числа) на кадре
    def draw_text_boxes(self, text_data: TextData, margin=None, color=None, thick=None):

        if self.image is not None:

            if margin is None:
                margin = self._border_margin
            if color is None:
                color = self._border_color
            if thick is None:
                thick = self._border_thick

            for box in text_data:
                x, y, w, h = box['left'], box['top'], box['width'], box['height']
                cv2.rectangle(self.image, (x - margin, y - margin), (x + w + margin, y + h + margin), color, thick)

    def replace_text_in_box(self, box: TextBox, bg):

        x, y, w, h = box['left'], box['top'], box['width'], box['height']
        self.image[y: y + h, x: x + w] = bg
        cv2.putText(self.image, '1500', (x-30, y+h), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.7, color=(0, 0, 0))

