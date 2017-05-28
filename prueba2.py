import numpy as np
import cv2
print "Programa iniciado"


def clean_errors(image):
	tam = image.shape
	status = 0
	for i in range(0, tam[0]):
		for j in range(0, tam[1]):
			if(image[i][j] == 255):
				if (i>0 and image[i-1][j]==status): 
					image[i-1][j] = 2
				
				if (j>0 and image[i][j-1]==status): 
					image[i][j-1] = 2
				
				if (i+1< tam[0] and image[i+1][j]==status): 
					image[i+1][j] = 2
				
				if (j+1<tam[1] and image[i][j+1]==status): 
					image[i][j+1] = 2
	
	return image

def morfology(frame, variable):
	tam = frame.shape

	for i in range(0, tam[0]):
		for j in range(0, tam[1]):
			if(frame[i][j] == 2):
				frame[i][j] = variable
	return frame


frames = []
i = 1
acum = np.zeros((720, 1280))
frame2 = cv2.imread('frame200.jpg', 0)
while(i <= 100):
	frame = cv2.imread('frame' + str(i) + '.jpg', 0)
	frames.append(frame)
	acum = frame + acum
	i = i + 1


promedio = acum / 100
difference =  abs(frame2 - promedio)

cv2.imwrite('salida3.jpg', difference)
ther = 30
max_value = 255
th, dst = cv2.threshold(difference,ther, max_value, cv2.THRESH_BINARY);
cv2.imwrite('salida4.jpg', dst)
new_frame = clean_errors(dst)
morfo = morfology(new_frame, 255)
cv2.imwrite('morfo.jpg', morfo)

#difference = frame2 - frame1
#cv2.imwrite("difference.jpg", difference)
#width, height = cv.GetSize(difference)
#print "widht" % widht
#print "height" % height
print "Programa terminado" 
print abs(difference)
