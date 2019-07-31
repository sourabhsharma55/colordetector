from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api, reqparse
import time
from werkzeug.serving import run_simple
#from main import server
import subprocess
import cv2
import signal
import os
import json



# import circle
# import nutdetect

app = Flask(__name__)
api = Api(app)
addCamParser = reqparse.RequestParser()
addCamParser.add_argument('screw')
addCamParser.add_argument('close')
addCamParser.add_argument('circle')
#addCamParser.add_argument('c_close')
addCamParser.add_argument('start')
#addCamParser.add_argument('s_close')
addCamParser.add_argument('fuse')
#addCamParser.add_argument('f_close')
addCamParser.add_argument('bottle')
#addCamParser.add_argument('b_close')
addCamParser.add_argument('threadlock')
#addCamParser.add_argument('t_close')
addCamParser.add_argument('live_screw')
#addCamParser.add_argument('sr_close')

a=0

class LiveFeed(Resource):

	def __init__(self):
		super().__init__()

	def kill_pid(self):
		try:
			with open('/home/nano2/res.json') as f:
				pid=json.load(f)
				s = 'kill ' + str(pid['PID'])
				os.system(s)
		except : pass

	def post(self):
		print("port working")
		global a
		args = addCamParser.parse_args()
		print(args)
		print("args_parser")
		if args['screw']:
			print('screw')
			self.kill_pid()
			a=subprocess.Popen(["python3", "new_screw.py"])  #screw
			print(a.pid)
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)

		elif args['start']:
			print("start")
			self.kill_pid()
			a=subprocess.Popen(["python3", "main.py"])  # thread
			print(a.pid)
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)
			
		elif args['threadlock']:
			print("threadlock")
			self.kill_pid()
			a=subprocess.Popen(["python3", "new_threadlock.py"])  # thread
			print(a.pid)
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)
			

		elif args['fuse']:
			print("fuse")
			self.kill_pid()
			a=subprocess.Popen(["python3", "new_fuse.py"])
			print(a.pid)
			with open('/home/nano2/res.json','w') as f:	  # fuse
				json.dump({"PID":a.pid},f)
				
		elif args['bottle']:
			print("bottle")
			self.kill_pid()
			a=subprocess.Popen(["python3", "jsonBottleCap.py"])
			print(a.pid)                                          # bottle
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)
				
		elif args['live_screw']:
			print("screw_live_feed")
			self.kill_pid()
			a=subprocess.Popen(["python3", "jsonScrewLiveFeed.py"])
			print(a.pid)                                          # live_feed
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)
				
		elif args['circle']:
			print("circle")
			self.kill_pid()
			a=subprocess.Popen(["python3", "circle.py"])
			print(a.pid)                                          # circle
			with open('/home/nano2/res.json','w') as f:	
				json.dump({"PID":a.pid},f)
			

#=----------------close=---------------------------------------------------------
		elif args['close']:
			with open('/home/nano2/res.json') as f:
				pid=json.load(f)
			print("CLOSE",pid['PID'])
			s = 'kill ' + str(pid['PID'])
			os.system(s)


def run_server():

	run_simple('10.0.0.1', 5010, app, use_reloader=True, processes=1000)	

if __name__ == '__main__':

	try:
		api.add_resource(LiveFeed, '/cam')
		app.debug = True 
		os.system("sudo systemctl restart nvargus-daemon")
		time.sleep(3)
		run_server()

	except: 
		s = "sudo fuser -k 5010/tcp && sudo fuser -k 5555/tcp"
		os.system("sudo systemctl restart nvargus-daemon")    # cleaning the resources of gstreamer.
		time.sleep(3)
		os.system(s)
		time.sleep(5)
		run_server()
