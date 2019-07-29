import numpy as np 
import cv2 
import json
from SYNVISION import colordetector

#-----------------------------------------------------------------------------------------------------------------------------------------------
def gstreamer_pipeline (capture_width=600, capture_height=450,display_width=600, display_height=450, framerate=60, flip_method=0) :   
	return ('nvarguscamerasrc ! ' 
	'video/x-raw(memory:NVMM), '
	'width=(int)%d, height=(int)%d, '
	'format=(string)NV12, framerate=(fraction)%d/1 ! '
	'nvvidconv flip-method=%d ! '
	'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
	'videoconvert ! '
	'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))
#------------------------------------------------------------------------------------------------------------------------------------------------
port = "5553"
if len(sys.argv) > 1: 
port =  sys.argv[1]
int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
jpeg_quality = 95

# camera------------------------------------------------------------------------
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

# screw_class--------------------------------------------------------------------
class Tester():

	def __init__(self):
		self.detectorObject = colordetector.detectColor()
		#_,self.frame = cap.read()
		with open('/home/nano2/new_qc/qc_modules/config.json') as f:
		    configuration = json.load(f)
		self.screwConfig = configuration['missingScrews']
		colours = self.screwConfig['colourDict']

	for name in colours:
	    lb = np.array(colours[name][0])
	    ub = np.array(colours[name][1])
	    self.detectorObject.clrDict[name] = [lb,ub]

	self.detectorObject.checkBoxes = self.screwConfig['boundingBox']

	def run(self,val):  # 'val' is the frames from the gstreamer_camera

		frame  = self.detectorObject.detect(val,
		self.screwConfig['returnFoundColour'],
		self.screwConfig['requiredPixelRatio'],
		self.screwConfig['reverseFlag'])
		return frame
'''
obj = Tester()
cv2.imshow('Detection',obj.run())
cv2.waitKey(0000)
'''

obj = Tester()
while True:
	try:
		ret, val = cap.read()
	if ret:
		ret_code, jpg_buffer = cv2.imencode(
		".jpg", obj.run(val), [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
		socket.send(jpg_buffer.tostring())
		print "Frames sent"
		key = cv2.waitKey(1):
		if key == ord("c"):
			exit(0)

	except KeyboardInterrupt:
		socket.close()
		print "server is closed!"
		break

exit(0)