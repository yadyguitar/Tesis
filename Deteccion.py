#!/usr/bin/env python
import freenect
import cv2
import numpy as np
from Persona import Persona


class Deteccion:
	def __init__(self, persona):
		self.frameRGB=None
		self.frameDepth=None		
		self.threshold = 92
		self.persona=persona
		cv2.namedWindow('Thres')
		#Creo dos trackbar, uno con el minimo, y otro con el maximo (Sublime no permite acentos ):)
		cv2.createTrackbar('Threshold','Thres',self.threshold,500,self.change_threshold)

	def change_threshold(self,value):
		self.threshold = value

	def setFrames(self,rgb,depth):
		self.frameRGB=rgb
		self.frameDepth=depth

	def showFrameContorno(self,nombre,frame): #Imagen rgb con el contorno ya dibujado
		contours=persona.contornos
		cv2.drawContours(frame, contours, -1, (0,255,0), 2)
		cv2.imshow(nombre,frame)

	def binarizarFrame(self,frame):
		ret, threshold = cv2.threshold(frame,self.threshold,255,cv2.THRESH_BINARY_INV) #Refinamiento
		return threshold

	def buscaContornos(self,frame):
		contours, hierarchy = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Refinamiento: investigar mas de esto
		#contours, hierarchy = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		return contours

	def showRotatedRectangle(self,frame,cnt):
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(frame,[box],0,(0,0,255),2)
		cv2.imshow('Rectangulo',frame)

	def setContornoPersona(self,contours):
		try:
			indexContorno=self.getIndexContornoAreaMayor(contours)#indice donde se encuentra la persona
			self.persona.contornos=contours[indexContorno]
		except:
			print ("no hay contornos")
		
	def getIndexContornoAreaMayor(self,contornos): #Obtengo el area de contornos, la mas grande se supone sera la persona
		areas=[]
		for cont in contornos:
			areas.append(cv2.contourArea(cont))
		maximo=max(areas)
		return areas.index(maximo)

	def deteccionManual(self):#primera propuesta de deteccion
		#Filtrado y tratamiento imagen
		depth=cv2.GaussianBlur(self.frameDepth, (5, 5), 0)
		depth=cv2.medianBlur(depth,5)
		#depth = cv2.blur(depth,(5,5))

		thres=self.binarizarFrame(depth)
		#*********************************************************************************#
		#cv2.imshow('Thres',thres) #muestra la ventana donde ajustare manualmente el thres

		contours=self.buscaContornos(thres.copy())
		self.setContornoPersona(contours)
		cv2.drawContours(self.frameRGB,[self.persona.contornos],0, (0,255,0), 2)
		#*********************************************************************************#
		#cv2.imshow('Imagen RGB',self.frameRGB)
		cv2.imshow('Imagen Depth',self.frameDepth)
		
		#self.showRotatedRectangle(self.frameRGB,self.persona.contornos)

if __name__=="__main__":
	print('Press ESC in window to stop')
