#!/usr/bin/env python3

#first test on ball tracking from this site: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

'''
#paste this in Sonic Pi and run it
live_loop :testWebCam do
  use_real_time
  pad, status = (sync "/osc:127.0.0.1:**/pad") #sync gets an array of values, take the first one
  print pad
  print status
  if (pad == 3 and status == 1)
    sample :drum_heavy_kick
  end
  
  if (pad == 2 and status == 1)
    sample :drum_snare_hard
  end
  
  if (pad == 1 and status == 1)
    sample :drum_cymbal_open
  end
  
end
'''

osc_ip = '127.0.0.1'
osc_port = 4559 #Sonic Pi
osc_client = udp_client.SimpleUDPClient(osc_ip,osc_port)
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define boundaries of trigger zones, frame is 600x448 pixels
trg_zone_1 = ((0,300),(200,448))
trg_zone_2 = ((200,300),(400,448))
trg_zone_3 = ((400,300),(600,448))

trg_zone_1_line_thickness = 3
trg_zone_2_line_thickness = 3
trg_zone_3_line_thickness = 3

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (66, 84, 208)
greenUpper = (79, 197, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
 
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
 
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()
 
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts.appendleft(center)

	# check if center is in one of the trigger boxes
	if center:
		center_x = center[0]
		center_y = center[1]

		if trg_zone_1[0][0] <= center[0] <= trg_zone_1[1][0] and trg_zone_1[0][1] <= center[1] <= trg_zone_1[1][1]:
			if trg_zone_3_line_thickness == 3:
				osc_client.send_message('pad', [1, 1])
			trg_zone_3_line_thickness = -1
		else:
			if trg_zone_3_line_thickness == -1:
				osc_client.send_message('pad', [1, 0])
			trg_zone_3_line_thickness = 3

		if trg_zone_2[0][0] <= center[0] <= trg_zone_2[1][0] and trg_zone_2[0][1] <= center[1] <= trg_zone_2[1][1]:
			if trg_zone_2_line_thickness == 3:
				osc_client.send_message('pad', [2, 1])
			trg_zone_2_line_thickness = -1
		else:
			if trg_zone_2_line_thickness == -1:
				osc_client.send_message('pad', [2, 0])
			trg_zone_2_line_thickness = 3

		if trg_zone_3[0][0] <= center[0] <= trg_zone_3[1][0] and trg_zone_3[0][1] <= center[1] <= trg_zone_3[1][1]:
			if trg_zone_1_line_thickness == 3:
				osc_client.send_message('pad', [3, 1])
			trg_zone_1_line_thickness = -1
		else:
			if trg_zone_1_line_thickness == -1:
				osc_client.send_message('pad', [3, 0])
			trg_zone_1_line_thickness = 3

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# flip the frame
	frame = cv2.flip(frame,1)

	# draw some boxes, these are the visual representation of the trigger zones
	colour_green = (195, 255, 76)
	colour_blue = (76, 195, 255)
	colour_pink = (255, 76, 195)
	frame = cv2.rectangle(frame,trg_zone_1[0], trg_zone_1[1],colour_green,trg_zone_1_line_thickness)
	frame = cv2.rectangle(frame,trg_zone_2[0], trg_zone_2[1],colour_blue,trg_zone_2_line_thickness)
	frame = cv2.rectangle(frame,trg_zone_3[0], trg_zone_3[1],colour_pink,trg_zone_3_line_thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the camera
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()