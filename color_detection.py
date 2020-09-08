import cv2
import numpy as np

colors = {
    1: ([25, 52, 72], [102, 255, 200]),  # green
    2: ([94, 80, 2], [126, 255, 255]),  # blue
    3: ([21, 110, 117], [45, 255, 255]),  # yellow
    4: ([0, 110, 125], [17, 255, 255]),  # orange
    5: ([161, 155, 84], [179, 255, 255]),  # red
    6: ([0, 0, 168], [172, 111, 255])  # white
}

list_of_colors = list(colors.keys())


def detect_color(image, w, h):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    maximum = np.zeros(shape=[len(colors.keys())])
    for index, i in enumerate(colors.values()):
        low, high = i
        low, high = np.array(low), np.array(high)

        mask = cv2.inRange(hsv_image, low, high)

        percentFilled = cv2.countNonZero(mask) / float(w * h)
        maximum[index] = percentFilled

    color = np.argmax(maximum)
    return list_of_colors[color]
