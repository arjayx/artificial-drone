import threading
import numpy as np
import cv2
import time
import multiprocessing
from multiprocessing import Manager
import collections
import datetime


out = cv2.VideoWriter('output_video_median3.avi', -1, 20, (1280,720))


def proccsing_square(frame):
	tam = frame.shape
	#print tam[0]
	#square_image 
	num_pixels = 40
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
					cv2.circle(frame,(j, i), 30, 255, 0)
					#cv2.imwrite("centroide.jpg", frame2)
			j = j + 1
		i = i + 1
	return frame


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


def frame_worker(frame, promedio, d, cont):
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
	gray = cv2.GaussianBlur(gray, (7,7), 0)
	difference =  abs(gray - promedio) - 12 
	ther = 2
	max_value = 255
	print "Estoy en el hilo" + str(cont)
	print "procesando frame" + str(cont)
	th, dst = cv2.threshold(difference,ther, max_value, cv2.THRESH_BINARY);
	#th, dst = cv2.threshold(median_blue,ther, max_value, cv2.THRESH_BINARY);
	#erode_frame = clean_errors(dst, 1, 1)
	#delating_frame = clean_errors(dst, 2, 4)
	#erode_frame = clean_errors(delating_frame, 1, 2)
	circles_frame = proccsing_square(dst)
	#l.append(delating_frame)
	d[cont] = dst
	print "termine de procesar frame" + str(cont)

	#print erode_frame
	#delating_frame = clean_errors(dst, 2, 2)





if __name__ == '__main__':
	print "Inicializando programa"
	file_name = 'video1.mov'
	cap = cv2.VideoCapture(file_name,0)
	frames = []
	i = 1
	acum = np.zeros((720, 1280))
	frames_average = 800
	#out = cv2.VideoWriter('output13.avi', -1, 20, (1280,720))
	ret = True
	while(cap.isOpened() and i <=frames_average and ret == True):
		ret,frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		if (ret==True):
			acum = acum + gray
			i = i + 1
		else:
			break
	error_prom = 0
	i = frames_average
	promediop = (acum + error_prom)/ frames_average
	cap2 = cv2.VideoCapture(file_name,0)
	error = 0
	print "Procesando output video"
	cont = 1
	hilos = 5
	num_frames = 0
	frames = []
	threads = []
	while (cap2.isOpened()):

		ret, frame = cap2.read()

		if (ret==True):
			num_frames = num_frames + 1
			print num_frames
			#print cont
			frames.append(frame) 
			cont = cont + 1
			#out.write(dst)
		else:
			break
		if (cont > hilos):
			#print "inicializando threads"
			cont2 = 0
			result = []

			with Manager() as manager:
				d = manager.dict()
				for frame in frames:
					#print 'add thread'
					#recv_end, send_end = multiprocessing.Pipe(False)
					t = multiprocessing.Process(target=frame_worker, args=(frame, promediop, d, cont2))
					threads.append(t)
					#result.append(recv_end)
					cont2 = cont2 + 1
				
				for thread in threads:
					#print "Empiezo thread"
					thread.start()
					#print "Entro a esperar"
					#thread.join()

				for thread in threads:
					#print "Empiezo thread"
					#print "Entro a esperar"
					thread.join()
				#print queue
				 
				print "Imagenes procesadas"
				od = collections.OrderedDict(sorted(d.items()))
				for key in od:
					fp = od[key]
					out.write(fp)
				#print result[l]
				#out.write(result[l])
			cont = 0
			frames = []
			threads = []

	
	print "Programa terminado"
	cap.release()
	cap2.release()
	cv2.destroyAllWindows()