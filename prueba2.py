import numpy as np
import cv2
print "Programa iniciado"


def clean_errors(image,operation):
	tam = image.shape
	# erode
	if(operation == 1):
		center = 0
		status = 255
		variable = 0
	#dilate
	else:
		center = 255
		status = 0
		variable = 255
	iteration = 3
	for i in range(0, tam[0]):
		for j in range(0, tam[1]):
			if(image[i][j] == center):
				if (i>0 and image[i-1][j]==status): 
					for k in range(1, iteration):			
						if(i-k > 0):
							image[i-k][j] = 2
				
				if (j>0 and image[i][j-1]==status): 
					for k in range(1, iteration):
						if(j-k > 0):
							image[i][j-k] = 2
				
				if (i+1< tam[0] and image[i+1][j]==status): 
					for k in range(1, iteration):
						if(i+k < tam[0]):
							image[i+k][j] = 2
				
				if (j+1<tam[1] and image[i][j+1]==status): 
					for k in range(1, iteration):
						if(j+k < tam[1]):
							image[i][j+k] = 2
				#image[i][j] = 2

	for i in range(0, tam[0]):
		for j in range(0, tam[1]):
			if(image[i][j] == 2):
				image[i][j] = variable	
	return image

frames = []
i = 1
acum = np.zeros((720, 1280))
frame2 = cv2.imread('frame500.jpg', 0)
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
morfo = clean_errors(dst, 1)
cv2.imwrite('morfo.jpg', morfo)

#difference = frame2 - frame1
#cv2.imwrite("difference.jpg", difference)
#width, height = cv.GetSize(difference)
#print "widht" % widht
#print "height" % height
print "Programa terminado" 
print abs(difference)
