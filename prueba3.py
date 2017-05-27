import numpy as np
import cv2

print "Inicializando programa"
cap = cv2.VideoCapture('output2.avi',0)
frames = []
i = 1
acum = np.zeros((720, 1280))
frames_average = 1000
out = cv2.VideoWriter('output3.avi', -1, 20, (1280,720))
ret = True
while(cap.isOpened() and i <=frames_average and ret == True):
	ret,frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if (ret==True):
		acum = acum + gray
		i = i + 1
	else:
		break

i = frames_average
promedio = acum / frames_average
cap2 = cv2.VideoCapture('video3.mov',0)
print "Procesando output video"
while (cap2.isOpened()):
	ret,frame = cap2.read()
	
	if (ret==True):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		
		difference =  abs(gray - promedio)
		ther = 10
		max_value = 255
		th, dst = cv2.threshold(difference,ther, max_value, cv2.THRESH_BINARY);
		out.write(dst)
	else:
		break
print "Programa terminado"

cap.release()
cap2.release()
cv2.destroyAllWindows()
