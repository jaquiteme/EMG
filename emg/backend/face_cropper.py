import cv2
import numpy as np
import sys
import os


class FaceCropper(object):

    def __init__(self, CASCADE_PATH):
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    def generate(self, image, name, f_name):
        nparr = np.fromstring(image.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        # img = cv2.imread(image)
        print(img)
        if (img is None):
            print("Can't open image file")
            return 0

        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img, 1.1, 3, minSize=(32, 32))
        if (faces is None):
            print('Failed to detect face')
            return 0

        # if (show_result):
        #     for (x, y, w, h) in faces:
        #         cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        #     cv2.imshow('img', img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        facecnt = len(faces)
        print("Detected faces: %d" % facecnt)
        i = 0
        height, width = img.shape[:2]

        for (x, y, w, h) in faces:
            r = max(w, h) / 2
            centerx = x + w / 2
            centery = y + h / 2
            nx = int(centerx - r)
            ny = int(centery - r)
            nr = int(r * 2)

            faceimg = img[ny:ny+nr, nx:nx+nr]
            lastimg = cv2.resize(faceimg, (150, 150))
            i += 1
            _path = "/home/jordy/EMG/emg/dataset/{}.{}.png".format(name, f_name)
            cv2.imwrite(_path, lastimg)

            return _path


# if __name__ == '__main__':
#     CASCADE_PATH = "haarcascade_frontalface_default.xml"
#     detecter = FaceCropper(CASCADE_PATH)
#     detecter.generate("/home/jordy/EMG/emg/backend/pp.jpg", "bella", "bellow")