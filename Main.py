import freenect
import cv2
import numpy as np

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
	while 1:
		frame=get_video()
		depth=get_depth()
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
