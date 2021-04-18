import cv2
import os

CHARS = ' .,-~:;=!*#$@'
nw = 110

cap = cv2.VideoCapture('videoplayback.mp4')
# img = cv2.imread('coro.png')

# print("\x1b[2J", end='')
os.system('cls')

while cap.isOpened():
    ret, img = cap.read() #한 프레임씩
    if not ret:
        break
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape
    nh = int(h / w * nw)

    img = cv2.resize(img, (nw * 2, nh))

    text = ''
    for row in img:
        char = ''
        for pixel in row:
            index = int(pixel / 256 * len(CHARS))
            char += CHARS[index]
            # print(CHARS[index], end='')

        text+=char+'\n'

    print(text)
    # print("\x1b[2J", end='')
    # os.system('cls')