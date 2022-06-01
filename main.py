from time import time
from pprint import pprint
import numpy as np
import cv2
from scanner import ImgScanner


def find_vertical_titles(scanner):

    short_title_list = ["Охват", "Взаимодействия",
                        "Действия", "Показы", "Репосты",
                        "Ответы", "Позвонить", "Навигация", "Вперед",
                        "Назад", "Выходы", "Переходы", "Посещения",
                        "Подписки", "Отправить", "Нажатия"]

    image = scanner.image
    text_data = scanner.get_text_data()
    only_nums = list(filter(lambda box: box['text'].isdigit() or box['text'] in ['o', 'O'], text_data))
    only_titles = list(filter(lambda box: box['text'] in short_title_list, text_data))
    only_nums_copy = only_nums.copy()
    vertical_titles = {'titles': [], 'nums': []}

    # Нахождение вертикальных полей статистики и значнения
    for title in only_titles:
        x1, y1, w1, h1 = title['left'], title['top'], title['width'], title['height']
        for num in only_nums_copy:
            x2, y2, w2, h2 = num['left'], num['top'], num['width'], num['height']
            if abs((y1 + h1 // 2) - (y2 + h2 // 2)) < 20:
                del only_nums_copy[only_nums_copy.index(num)]
                vertical_titles['titles'].append(title)
                vertical_titles['nums'].append(num)
                # print(f"{title['text']} -> {num['text']}")

    # pprint(title_n_nums)
    return vertical_titles


if __name__ == "__main__":
    #img = cv2.imread("data/test_img.PNG")

    #scan.image = img
    scan = ImgScanner()

    """ cv2.imshow("img", scan.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

    vid_capture = cv2.VideoCapture("data/test2.mp4")
    # Параметры видео (размеры, кадры и тд)
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(vid_capture.get(5))
    frame_count = vid_capture.get(7)

    print(f"W: {frame_width}; H: {frame_height}; FPS: {fps}")

    output = cv2.VideoWriter(f'data/result.mp4', -1, fps//2, frame_size)

    frame_num = 0
    start_time = time()
    data_to_draw = []

    while vid_capture.isOpened():
        rec, frame = vid_capture.read()
        scan.image = frame

        if rec:
            data_to_draw = find_vertical_titles(scan)

            a2D = scan.image.reshape(-1, scan.image.shape[-1])
            col_range = (256, 256, 256)
            a1D = np.ravel_multi_index(a2D.T, col_range)
            bg = np.unravel_index(np.bincount(a1D).argmax(), col_range)

            #scan.draw_text_boxes(text_data=data_to_draw['titles'] + data_to_draw['nums'])
            for box in data_to_draw['nums']:
                scan.replace_text_in_box(box, bg)
            output.write(scan.image)
            frame_num += 1
            print("{:5.2f} %".format((frame_num / frame_count) * 100))
        else:
            break
    vid_capture.release()
    output.release()
    print(f"Прошло секунд: {time() - start_time}")
