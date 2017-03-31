#!/usr/bin/env python
import freenect
import cv
import cv2
import frame_convert
import numpy as np


threshold = 173
current_depth = 320


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def get_depth():
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    return depth
    
   


def get_video():
	frame,_ = freenect.sync_get_video()
	frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
	return frame
	

cv2.namedWindow('Depth')
cv2.createTrackbar('threshold','Depth',threshold,500,change_threshold)
cv2.createTrackbar('depth','Depth',current_depth,2048,change_depth)


print('Press ESC in window to stop')


while 1:
	frame=get_video()
	depth=get_depth()
	cv2.imshow("Video",frame)
	cv2.imshow('Depth',depth)
	
	
	contours, hierarchy = cv2.findContours(depth,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	print contours
	cv2.drawContours(frame, contours, -1, (0,255,0), 2)
	cv2.imshow("Contorno",frame)
	
	if cv.WaitKey(5) & 0xFF == 27:
		break

freenect.sync_stop() #para liberar kinect
