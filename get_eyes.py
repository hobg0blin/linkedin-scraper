import cv2
import sys

paths = sys.argv[1:]

print('haar cascades: ', cv2.data.haarcascades)
for img in paths:
    print('path: ', paths)
    print('img: ', img)
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    print("Found {} Faces in {}.".format(len(faces), img))

    i = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        outname = "{}_eyes{}_.jpg".format(img, str(i).zfill(4))
        i += 1
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey +eh), (0, 0, 0), -1)

        cv2.imwrite(outname, roi_color)
#        status = cv2.imwrite('faces_detected.jpg', image)
#        print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
