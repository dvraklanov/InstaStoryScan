from pprint import pprint
from typing import Dict, List, Union, Callable
import numpy as np
import cv2
import pytesseract


class ImgScanner(object):
    TextData = List[Dict[str, Union[int, str]]]
    cfg = r'--oem 3 --psm 3  -l rus+eng'

    def __init__(self):

        self.image = None
        self.transformed_image = None
        # Колонки получаемые из таблицы с данными о кадре
        self._data_col = ['text', 'left', 'top', 'width', 'height', 'conf']

        # Стандартные параметры рамки
        self._border_margin = 5
        self._border_color = (0, 0, 255)  # красный
        self._border_thick = 2

    # Получить информацию о тексте на кадре
    def get_text_data(self, filter: Callable = lambda x: True) -> TextData:

        # бинаризация
        self.transformed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if self is not None:
            boxes = pytesseract.image_to_data(self.transformed_image, config=self.cfg, output_type=pytesseract.Output.DICT)
            text_data = [{key: boxes[key][i] for key in self._data_col}
                         for i, txt in enumerate(boxes['text']) if not txt.isspace() and txt and filter(txt)]

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

            for word in text_data:
                x, y, w, h = word['left'], word['top'], word['width'], word['height']
                cv2.rectangle(self.image, (x - margin, y - margin), (x + w + margin, y + h + margin), color, thick)
