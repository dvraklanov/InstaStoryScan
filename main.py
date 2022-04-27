from time import time
from pprint import pprint
import cv2
from scanner import ImgScanner

if __name__ == "__main__":

    check_list = ["Охват", "Взаимодействие",
                  "Действия", "Показы", "Репосты",
                  "Ответы", "Позвонить", "Навигация", "Вперед",
                  "Назад", "Выходы", "Переходы", "Посещения",
                  "Подписки", "Отправить"]

    scan = ImgScanner()
    img = cv2.imread("data/test_img2.PNG")

    scan.image = img
    is_num = lambda x: x.isdigit() or x in ['o', 'O']
    in_check = lambda x: x in check_list
    only_nums = scan.get_text_data(filter=is_num)
    only_titles = scan.get_text_data(filter=in_check)
    scan.draw_text_boxes(text_data=only_titles+only_nums)

    for title in only_titles:
        x1, y1, w1, h1 = title['left'], title['top'], title['width'], title['height']
        for num in only_nums:
            x2, y2, w2, h2 = num['left'], num['top'], num['width'], num['height']
            if abs((y1 + h1 // 2) - (y2 + h2 // 2)) < 20:
                print(f"{title['text']} -> {num['text']}")

    cv2.imshow("img", scan.image)
    cv2.imshow("timg", scan.transformed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    """vid_capture = cv2.VideoCapture("data/test.mp4")
    # Параметры видео (размеры, кадры и тд)
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(vid_capture.get(5))
    frame_count = vid_capture.get(7)

    scan = ImgScanner()
    output = cv2.VideoWriter(f'data/result.mp4', -1, fps, frame_size)

    frame_num = 0
    start_time = time()

    while vid_capture.isOpened():
        rec, frame = vid_capture.read()
        scan.image = frame
        if rec:
            is_num = lambda x: x.isdigit() or x in ['o', 'O']
            in_check = lambda x: x in check_list
            only_nums = scan.get_text_data(filter=is_num)
            only_titles = scan.get_text_data(filter=in_check)
            scan.draw_text_boxes(filter=lambda x: in_check(x) or is_num(x))

            for title in only_titles:
                x1, y1, w1, h1 = title['left'], title['top'], title['width'], title['height']
                for num in only_nums:
                    x2, y2, w2, h2 = num['left'], num['top'], num['width'], num['height']
                    if abs((y1 + h1 // 2) - (y2 + h2 // 2)) < 20:
                        print(f"{title['text']} -> {num['text']}")
            output.write(scan.image)
            frame_num += 1
            print("{:5.2f} %".format((frame_num / frame_count) * 100))
        else:
            break

    vid_capture.release()
    output.release()
    cv2.destroyAllWindows()
    print(f"Прошло секунд: {time() - start_time}")"""