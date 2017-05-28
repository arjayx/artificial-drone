import numpy as np
import cv2

def clean_errors(image,operation, iteration):
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


print "Inicializando programa"
file_name = 'video3.mov'
cap = cv2.VideoCapture(file_name,0)
frames = []
i = 1
acum = np.zeros((720, 1280))
frames_average = 500
out = cv2.VideoWriter('output12.avi', -1, 20, (1280,720))
ret = True
while(cap.isOpened() and i <=frames_average and ret == True):
	ret,frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if (ret==True):
		acum = acum + gray
		i = i + 1
	else:
		break
error_prom = -20
i = frames_average
promedio = (acum + error_prom)/ frames_average
cap2 = cv2.VideoCapture(file_name,0)
error = 0
print "Procesando output video"
cont = 0
while (cap2.isOpened()):
	ret,frame = cap2.read()
	
	if (ret==True):
		frame = frame - error
		cont = cont + 1
		print cont
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		
		difference =  abs(gray - promedio)
		ther = 15
		max_value = 255
		
		th, dst = cv2.threshold(difference,ther, max_value, cv2.THRESH_BINARY);
		#erode_frame = clean_errors(dst, 1, 2)
		#delating_frame = clean_errors(dst, 2, 2)
		out.write(dst)
	else:
		break
print "Programa terminado"
cap.release()
cap2.release()
cv2.destroyAllWindows()