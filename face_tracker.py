import RPi.GPIO as GPIO
import cv2
from time import sleep
import numpy as np

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)

GPIO.setup(4, GPIO.OUT)

pwm_1 = GPIO.PWM(12 , 50)

pwn_2 = GPIO.PWM(4, 50)

pwm_1.start(6)
pwm_2.start(7)

def SetAngle(angle, pin, pwm):
	duty = angle / 18 + 2
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(0.05)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
right_cascade = cv2.CascadeClassifier('lbpcascade_profileface.xml')

cap = cv2.VideoCapture(0)

angle_1 = 72
angle_2 = 90

stepSize = 1

threshold = 5

try:

	while(1):

		x, y, w, h = 0, 0, 0, 0
		ret, img = cap.read()

		height, width = img.shape

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (X, Y, W, H) in faces:
			if W*H > w*h:
				x, y, w, h = X, Y, W, H


		if not faces:

			faces = right_cascade.detectMultiScale(gray, 1.3, 5)
			for (X, Y, W, H) in faces:
			if W*H > w*h:
				x, y, w, h = X, Y, W, H


			if face!=():

				flipped = np.fliplr(img)
				gray_2 = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
				faces = right_cascade.detectMultiScale(gray, 1.3, 5)
				for (X, Y, W, H) in faces:
					if W*H > w*h:		
						x, y, w, h = width - X, Y, W, H

		if faces!=():
			continue

		if y + threshold < height//2:

			if angle_1 >= threshold:
				angle_1-=1
				SetAngle(angle_1, 12, pwm_1)

		if y > height//2 + threshold:

			if angle_1 <= 180 - threshold:
				angle_1+=1
				SetAngle(angle_1, 12, pwm_1)

		if x + threshold < width//2:

			if angle_2 >= threshold:
				angle_2-=1
				SetAngle(angle_2, 4, pwm_2)

		if x > width//2 + threshold:

			if angle_2 <= 180 - threshold:
				angle_2+=1
				SetAngle(angle_2, 4, pwm_2)

except KeyboardInterrupt:

	pwm_1.stop()
	pwm_2.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()




