from time import time
import cv2
from scanner import ImgScanner

if __name__ == "__main__":

    vid_capture = cv2.VideoCapture("test.mp4")

    # Параметры видео (размеры, кадры и тд)
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    fps = int(vid_capture.get(5))
    frame_count = vid_capture.get(7)

    scan = ImgScanner()
    output = cv2.VideoWriter(f'result.mp4', -1, fps, frame_size)

    frame_num = 0
    start_time = time()
    while vid_capture.isOpened():
        rec, frame = vid_capture.read()
        scan.image = frame
        if rec:
            scan.draw_text_boxes(only_nums=True)
            output.write(scan.image)
            frame_num += 1
            print("{:5.2f} %".format((frame_num / frame_count) * 100))
        else:
            break
    print(f"Прошло секунд: {time() - start_time}")
    vid_capture.release()
    output.release()
    cv2.destroyAllWindows()
