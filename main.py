import cv2
import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
cap = cv2.VideoCapture(0)
ret, val = cap.read()
jpeg_quality = 95
while True:
    ret, val = cap.read()
    if ret:

        ret_code, jpg_buffer = cv2.imencode(
            ".jpg", val, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
        socket.send(jpg_buffer.tostring())
        print "sent"

