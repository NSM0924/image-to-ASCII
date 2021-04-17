import cv2

CHARS = ' .,-~:;=!*#$@'
nw = 50

img = cv2.imread('coro.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = img.shape
nh = int(h / w * nw)

img = cv2.resize(img, (nw * 2, nh))

text=''
for row in img:
    for pixel in row:
        index = int(pixel / 256 * len(CHARS))
        text += CHARS[index]
        # print(CHARS[index],end='')

    print(text)
    text=''