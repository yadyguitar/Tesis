import freenect
import cv2
import numpy as np
from time import time
from Persona import Persona
from Deteccion import Deteccion
from Posicion import Posicion

def get_depth():
	depth, timestamp = freenect.sync_get_depth()
	#np.clip(depth, 0, 2**10 - 1, depth)
	#depth >>= 2
	depth = depth.astype(np.uint8)
	return depth

def get_video():
	frame,_ = freenect.sync_get_video()
	frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
	return frame

def guardaInfoPersona(posicion):
	file=open('infoPersona.txt','w')
	np.savetxt(file,posicion)
	file.close


if __name__=="__main__":
	#Instanciar clases (:
	persona=Persona()
	deteccion=Deteccion(persona,1)
	posicion=Posicion(persona)
	tiempoinicial=time()
	cont=0
	seg=1
	while 1:
		'''print "depth"
		print (cont/30,time()-tiempoinicial)
		print "rgb"
		print (cont/30,time()-tiempoinicial)'''
		frame=get_video()
		depth=get_depth()

		cont+=1

		if (time()-tiempoinicial>(seg+1)):
			print str(cont) + "frames por segundo"

		if(int(time()-tiempoinicial)>(seg)):
			seg=int(time()-tiempoinicial)
			cont=0
	
			

		cv2.imshow("Profundidad",depth)#para pruebas
		#se va modificando la class persona y se puede ir accediendo a sus propiedades actuales
		deteccion.setFrames(frame,depth)
		
		#deteccion.deteccionManual()
		deteccion.deteccionAutomatica() #si detecto algo, sigue con lo demas, de lo contrario, blender utilizara la ultima informacion que tenia de el file Persona
		if persona.contornos != None:
			posicion.setFrames(frame,depth)
			posicion.calculaPosicion()
			#print persona.posicion 
			#guarda informacion de la clase persona
			guardaInfoPersona(persona.posicion)
		if cv2.waitKey(1) & 0xFF == 27:
			break
	
	freenect.sync_stop() #para liberar kinect
