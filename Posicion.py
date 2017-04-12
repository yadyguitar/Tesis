import cv2
from Persona import Persona
import numpy as np
class Posicion:
	def __init__(self, persona):
		self.persona=persona
		self.frameRGB=None

	def setFrames(self,rgb):
		self.frameRGB=rgb

	def calculaCentroFigura(self,c):
		#calculo del centro del contorno usando momentos (:
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		#print (cX,cY)
		return (cX,cY)

	def showPointCentral(self):
		cv2.drawContours(self.frameRGB, [self.persona.contornos], 0, (0, 255, 0), 2)
		cv2.circle(self.frameRGB, self.persona.posicion, 7, (255, 255, 255), -1)
		#cv2.putText(image, "center", (cX - 20, cY - 20),
		#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		cv2.imshow("Imagen con punto central", self.frameRGB)

	def calculaPosicion(self):
		contornos=self.persona.contornos
		xy=self.calculaCentroFigura(contornos)
		self.persona.posicion=xy
		self.showPointCentral()

if __name__ == "__main__":
	print "estoy en la clase posicion"