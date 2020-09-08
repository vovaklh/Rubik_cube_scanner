import cv2
import imutils
from imutils.perspective import four_point_transform


def find_cube(image, debug):
    # show image
    if debug:
        cv2.imshow("Image", image)
        cv2.waitKey(0)

    # convert to gray scale, apply blurring and edge
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

    # show edged
    if debug:
        cv2.imshow("Edged", thresh)
        cv2.waitKey(0)

    # find contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # coords of box
    box = []

    # approximate
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, peri * 0.02, True)

        if len(approx) == 4:
            box = approx
            break

    # draw contours
    copy = image.copy()
    cv2.drawContours(copy, [box], -1, (0, 255, 0), 2)
    if debug:
        cv2.imshow("Contours", copy)
        cv2.waitKey(0)

    # extract cube
    roi = four_point_transform(image, box.reshape((4, 2)))
    if debug:
        cv2.imshow("Cube", roi)
        cv2.waitKey(0)

    return roi
