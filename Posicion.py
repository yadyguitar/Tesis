import cv2
from Persona import Persona
import numpy as np
import math

class Posicion:
	def __init__(self, persona):
		self.persona=persona
		self.frameRGB=None

	def setFrames(self,rgb):
		self.frameRGB=rgb

	def calculaCentroFigura(self,c):
		#calculo del centro del contorno usando momentos (:
		M = cv2.moments(c)
		cX=self.persona.posicion[0]
		cY=self.persona.posicion[1]
		try:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		except:
			print "division entre cero"
			
		print (cX,cY)
		return (cX,cY)

	def filtroPosicion(self,xy):
		px=self.persona.posicion[0]
		py=self.persona.posicion[1]
		x=xy[0]
		y=xy[1]

		distancia=math.sqrt((px-x)**2 + (py-y)**2)
		if distancia<=5:
			return (px,py)
		return xy


	def showPointCentral(self):
		cv2.drawContours(self.frameRGB, [self.persona.contornos], 0, (0, 255, 0), 2)
		cv2.circle(self.frameRGB, self.persona.posicion, 7, (255, 255, 255), -1)
		#cv2.putText(image, "center", (cX - 20, cY - 20),
		#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		cv2.imshow("Imagen con punto central", self.frameRGB)

	def calculaPosicion(self):
		contornos=self.persona.contornos
		xy=self.calculaCentroFigura(contornos)
		#filtro para que no varie mucho la deteccion de posicion
		xy=self.filtroPosicion(xy)
		self.persona.posicion=xy
		self.showPointCentral()

if __name__ == "__main__":
	print ("estoy en la clase posicion")
