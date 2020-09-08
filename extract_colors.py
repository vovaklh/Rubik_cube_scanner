import cv2
from scan import find_cube
from color_detection import detect_color
import numpy as np
from os import listdir
from os.path import join


def extract_colors(path, size, flag):
    if len(listdir(path)) == 6:
        # create numpy array if colors
        colors = np.zeros((6, size, size))

        # loop over images
        for index, i in enumerate(listdir(path)):
            # load image
            image = cv2.imread(join(path, i))

            # extract cube
            cube = find_cube(image, flag)

            # unroll image shape
            h, w, c = cube.shape

            # create stepX and stepY
            stepX = w // size
            stepY = h // size

            # loop over cells
            for y in range(size):
                for x in range(size):
                    startX = x * stepX
                    startY = y * stepY
                    endX = (x + 1) * stepX
                    endY = (y + 1) * stepY

                    roi = cube[startY:endY, startX:endX]
                    colors[index, y, x] = detect_color(roi, w, h)
        return colors
    else:
        return None


