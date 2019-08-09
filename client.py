import numpy as np
import sys

import cv2
import zmq

port = "5553"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)


socket.connect("tcp://192.168.0.41:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, b"")
c = 0
import time
t_base = time.time()
# Process 5 updates
total_value = 0
while True:
    c += 1
    # print("working")
    image = socket.recv()
    # print(image)
    image = cv2.imdecode(np.fromstring(image, dtype='uint8'), -1)
    cv2.imshow("f", image)
    '''if c % 100 == 0:
        c = 0
        t2 = time.time()
        print "sdfds",t_base, t2
        print f"fps = {100/(t2 - t_base)}"
        t_base = t2'''
    cv2.waitKey(1)



