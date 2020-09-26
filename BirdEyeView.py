import cv2 as cv
import numpy as np
from math import sin, tan, atan, radians, degrees

boundaries = ([87, 51, 0], [255, 135, 150])

camId = 0
width = 1280
height = 720

# fill following 5 parameters with GetParameters.py
camAngle = 61.16249506470501  # camera angle
point1 = (290, 1)  # top left
point2 = (976, 1)  # top right
point3 = (1280, 696)  # bottom right
point4 = (0, 696)  # bottom left

aspectRatio = height / width
hFov = 60
vFov = 2 * degrees(atan(aspectRatio * tan(radians(hFov / 2))))

vScale = 1
firstIteration = True

pts = np.array([point1, point2, point3, point4], dtype="float32")


def vertical_scale_factor(fg):
    b = camAngle
    c = vFov

    a = 90 - b - c / 2
    d = 180 - 90 - a
    e = (180 - c) / 2
    f = 180 - d - e
    g = 180 - e
    h = 180 - f - g

    fh = fg * sin(radians(g)) / sin(radians(h))

    return fh / fg


def order_points(points):
    rect = np.zeros((4, 2), dtype="float32")

    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]

    return rect


def four_point_transform(image, points):
    global firstIteration, vScale

    rect = order_points(points)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)

    if firstIteration:
        firstIteration = False
        vScale = vertical_scale_factor(maxHeight)

    return cv.warpPerspective(image, M, (maxWidth, maxHeight))


class BirdEyeView:
    ret = None
    frame = None
    warped = None

    def __init__(self):
        global pts, firstIteration, vScale

        cap = cv.VideoCapture(camId)
        cap.set(3, width)
        cap.set(4, height)

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            self.ret, self.frame = cap.read()

            self.warped = four_point_transform(self.frame, pts)
            self.warped = cv.resize(self.warped, None, fx=1, fy=vScale, interpolation=cv.INTER_CUBIC)
            # resize to actual vertical size

            self.warped = cv.resize(self.warped, None, fx=0.3, fy=0.3, interpolation=cv.INTER_CUBIC)
            # resize window to fit monitor

            cv.imshow('warped', self.warped)

            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    BirdEyeView = BirdEyeView()
