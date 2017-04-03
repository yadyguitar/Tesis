#!/usr/bin/env python
import freenect
import cv
import cv2
import frame_convert
import numpy as np

class Deteccion:
	def __init__(self):
		self.threshold = 173
		self.current_depth = 320

	def change_threshold(self,value):
		self.threshold = value

	def change_depth(self,value):
		self.current_depth = value

	def get_depth(self):
		depth, timestamp = freenect.sync_get_depth()
		depth = 255 * np.logical_and(depth >= self.current_depth - self.threshold,
                                 depth <= self.current_depth + self.threshold)
		depth = depth.astype(np.uint8)
		return depth

	def get_video(self):
		frame,_ = freenect.sync_get_video()
		frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
		return frame

print('Press ESC in window to stop')
d=Deteccion()
cv2.namedWindow('Depth')
cv2.createTrackbar('threshold','Depth',d.threshold,500,d.change_threshold)
cv2.createTrackbar('depth','Depth',d.current_depth,2048,d.change_depth)



if __name__=="__main__":
	while 1:
		frame=d.get_video()
		depth=d.get_depth()
		cv2.imshow("Video",frame)
		cv2.imshow('Depth',depth)
		contours, hierarchy = cv2.findContours(depth,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		print areas
		i=0
		for elementos in contours:
			x,y=np.round(np.median(elementos,axis=0)[0] ,decimals=0,out=None)
			punto_medio=(int(x),int(y))
			cv2.circle(frame, punto_medio ,2,(0,0,255),-1)

		
		cv2.drawContours(frame, contours, -1, (0,255,0), 2)
		cv2.imshow("Contorno",frame)
		if cv.WaitKey(5) & 0xFF == 27:
			break
	freenect.sync_stop() #para liberar kinect
