import cv2 as cv
from math import tan, atan, sin, degrees, radians

width = 1280
height = 720
camId = 0

line1 = []
line2 = []


def drawLine(x, y):
    if len(line1) != 2:
        line1.append([x, y])
        # print("written in line 1")
    elif len(line2) != 2:
        line2.append([x, y])
        # print("written in line 2")


def calculateParameters():
    global line1, line2

    a1 = degrees(atan((line1[0][0] - line1[1][0]) / (line1[1][1] - line1[0][1]))) * -1
    a2 = degrees(atan((line2[1][0] - line2[0][0]) / (line2[1][1] - line2[0][1]))) * -1

    total = a1 + a2
    camAngle = -1419.86460839654 + (52.50471923974 * total) + (-0.587483589940888 * total * total) + (
            0.00207285233289911 * total * total * total)

    b1 = total * -1
    b2 = 0.921273435612413 + (2.90963449098438 * b1) + (0.0583885791885022 * b1 * b1) + (
            0.0002664526023097 * b1 * b1 * b1)

    c1 = height * sin(radians(b2)) / sin(radians(90 - b2))

    pt1 = (c1, 0)
    pt2 = (width - c1, 0)
    pt3 = (width, height)
    pt4 = (0, height)

    print("camAngle = " + str(camAngle))

    print("point1 = " + str(pt1))
    print("point2 = " + str(pt2))
    print("point3 = " + str(pt3))
    print("point4 = " + str(pt4))

    line1 = []
    line2 = []


def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # print('Down x = %d, y = %d' % (x, y))
        drawLine(x, y)
    elif event == cv.EVENT_LBUTTONUP:
        # print('Up x = %d, y = %d' % (x, y))
        drawLine(x, y)


class GetParameters:
    ret = None
    frame = None

    def __init__(self):
        cap = cv.VideoCapture(camId)
        cap.set(3, width)
        cap.set(4, height)

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            self.ret, self.frame = cap.read()

            if len(line1) == 2:
                cv.line(img=self.frame, pt1=(line1[0][0], line1[0][1]), pt2=(line1[1][0], line1[1][1]),
                        color=(0, 255, 0), thickness=3, lineType=8, shift=0)
            if len(line2) == 2:
                cv.line(img=self.frame, pt1=(line2[0][0], line2[0][1]), pt2=(line2[1][0], line2[1][1]),
                        color=(0, 0, 255), thickness=3, lineType=8, shift=0)
                calculateParameters()
                break

            cv.imshow('frame', self.frame)

            cv.setMouseCallback('frame', onMouse)

            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    GetParameters = GetParameters()
