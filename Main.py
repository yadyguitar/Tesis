import freenect
import cv2
import cv
import numpy as np

from Persona import Persona
from Deteccion import Deteccion


def get_depth():
	depth, timestamp = freenect.sync_get_depth()
	np.clip(depth, 0, 2**10 - 1, depth)
	depth >>= 2
	depth = depth.astype(np.uint8)
	return depth

def get_video():
	frame,_ = freenect.sync_get_video()
	frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
	return frame


if __name__=="__main__":
	print "hola"
	persona=Persona()
	deteccion=Deteccion(persona)
	while 1:
		frame=get_video()
		depth=get_depth()

		deteccion.setFrames(frame,depth)
		deteccion.deteccionManual()

		if cv.WaitKey(5) & 0xFF == 27:
			break
	
	freenect.sync_stop() #para liberar kinect
