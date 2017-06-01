import threading
import numpy as np
import cv2
import time
import multiprocessing
from multiprocessing import Manager
import collections
import datetime



def proccsing_square(frame):
	tam = frame.shape
	#print tam[0]
	#square_image 
	num_pixels = 15
	i = 1
	while (i < tam[0]):
		j = 1
		while (j < tam[1]):
			#print "Esta es mi coordenadas" + str(i) + ", " + str(j)
			#print frame[i][j]
			if(frame[i][j] == 255):
				#print frame[i][j]
				#print "Esta es mi coordenadas" + str(i) + ", " + str(j)
				c1 = j
				c2 = i
				itera = 1
				status = True
				# reviso los pixeles de forma  horizontal
				
				while(itera < num_pixels):
					#print "entro en este qhile"
					if (c1 + itera < tam[1] and (c1 - itera > 0)):
						
						if(frame[i][c1 + itera] != 255 and frame[i][c1 - itera] != 255 ):
							#print "entro en esta condicion"
							status = False
					itera = itera + 1
				#print " numero de iteraciones terminadas" + str(itera)
				itera = 1
				if (status == True):
					# reviso los pixeles de forma vertical
					#print "Encontre un candidato" + str(i) + ", " + str(j)
					while(itera < num_pixels):

						if ( c2 + itera < tam[0] and (c2 - itera > 0)):
							if (frame[c2 + itera][j] != 255 and frame[c2 - itera][j] != 255):
								status = False
						itera = itera + 1
					
				# reviso que el pixel pase la prueba
				if (status == True):
					#square_image[i][j] = 2
					#print "encontre un centroide" + str(i) + ", " + str(j)
					frame = cv2.circle(frame,(j, i), 30, 255, 0)
					#cv2.imwrite("centroide.jpg", frame2)
			j = j + 1
		i = i + 1
	return frame

def frame_worker(frame, promedio, d, cont):
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
	#gray = cv2.GaussianBlur(gray, (3,3), 0)
	difference =  abs(gray - promedio) -10
	ther = 5
	max_value = 255
	print "Estoy en el hilo" + str(cont)
	print "procesando frame" + str(cont)
	th, dst = cv2.threshold(difference,ther, max_value, cv2.THRESH_BINARY);
	#th, dst = cv2.threshold(median_blue,ther, max_value, cv2.THRESH_BINARY);
	#erode_frame = clean_errors(dst, 1, 1)
	delating_frame = clean_errors(dst, 2, 2)



#frame2 = cv2.imread('frame668.jpg', 0)

out = cv2.VideoWriter('video_centro_out.avi', -1, 20, (1280,720))
#result = proccsing_square(frame2)
file_name = 'output4.avi'
cap = cv2.VideoCapture(file_name)
cont = 1
while (cap.isOpened()):
	cont = cont + 1
 	ret, frame = cap.read()
 	if (ret==True):
 		print " frame numero: " + str(cont)
 		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
 		if (cont > 300 and cont < 600):
 			circle = proccsing_square(frame)
 			out.write(circle)
 		else:
 			if (cont > 600):
 				break
 	#time.sleep(0.5)