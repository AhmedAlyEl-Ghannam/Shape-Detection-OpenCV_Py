import cv2
import numpy as np


def remove_black_borders(image):
    y_nonzero, x_nonzero = np.nonzero(image)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]


shapes = [0, 0, 0, 0]  # triangles, squares, rectangles, circles
img = cv2.imread("sample.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(img, 5)
_, th1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((30, 30), np.uint8)
opening = cv2.morphologyEx(th1, cv2.MORPH_OPEN, kernel)
bilateralFilter = cv2.bilateralFilter(opening, 9, 75, 75)
img = remove_black_borders(bilateralFilter)
contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.imshow('haha, pic go brrr!', img)
cv2.waitKey(0)
cv2.imwrite('2B_or_NOT_2B.jpg', img)
# print("Number of Detected Contours = ", str(len(contours)))
for i, contour in enumerate(contours):
    if i == 0:
        continue
    epsilon = 0.03 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    cv2.drawContours(img, contour, 0, (127, 127, 127), 3)
    if len(approx) == 3:
        shapes[0] = shapes[0] + 1
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        if (ar >= 0.95) and (ar <= 1.05):
            shapes[1] = shapes[1] + 1
        else:
            shapes[2] = shapes[2] + 1
    else:
        if cv2.contourArea(contour) > 1000:
            shapes[3] = shapes[3] + 1

print("Number of Triangles = ", shapes[0])
print("Number of Squares = ", shapes[1])
print("Number of Rectangles = ", shapes[2])
print("Number of Circles = ", shapes[3])
