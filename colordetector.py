import cv2 
import numpy as np 

class detectColor():

    def __init__(self):
        
        self.SHOW_WINDOW=False # display the region of interest if true 
        self.PAUSE=1           # pause the video for selecting a color window if true
        self.clrDict=dict()    # stores all the color(name and range values) selected by user

        
        self.x1 = -1  # Used for 
        self.x2 = -1  # showing rectangle
        self.y1 = -1  # animation when 
        self.y2 = -1  # user is selecting a
        self.drawing = False # color window

        #maintains a copy of frame
        self.frameCopy=None

    '''CALCULATES THE LOWER AND UPPER OF BOUND(OF SELECT WINDOW) COLOR RANGE'''
    def calcBounds(self,img):

        #:params img : WINDOW selected by user for extracting color
        #:return array : lower and upper bound of the selected window 
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
        h,s,v = cv2.split(img)
        
        minClamp = lambda a,b : max(a,b)
        maxClamp = lambda a,b : min(a,b)
        h = h.ravel()
        a = max(h)/2
        b = min(h)/2

        if b == 0:
            minh,maxh  = -1,-1
        else:
            avg_h = a + b
            print avg_h,max(h),min(h)

            maxh = maxClamp(avg_h+10,179) 
            minh = minClamp(avg_h-10,0)

        s = s.ravel()
        maxs = maxClamp(max(s),255)
        mins = minClamp(min(s),0)

        v = v.ravel()
        maxv = maxClamp(max(v),255)
        minv = minClamp(min(v),0)

        lb = np.array([minh,mins,minv])
        ub = np.array([maxh,maxs,maxv])

        return [lb,ub]



    ''' MOUSE CALLBACK TO SELECT COLOR WINDOW '''
    def colorWindow(self,action,x,y,flags,userData):
        
        #:params action: type of event occuring 
        #:params x,y: co-ordinate of event happening
         
        if not self.PAUSE:
            if action == cv2.EVENT_LBUTTONDOWN:
                self.frameCopy = self.frame.copy()
                self.drawing = True 
                self.x1 = x
                self.y1 = y

            elif action == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    self.frame = self.frameCopy.copy()
                    cv2.rectangle(self.frame,(self.x1,self.y1),(x,y),(0,0,255),1,cv2.LINE_AA)

            elif action == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                self.x2= x
                self.y2= y
                cv2.rectangle(self.frame,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),1)
                clr = raw_input('Enter Color Name : ')
                self.clrDict[clr]=self.calcBounds(self.frame[self.y1+2:self.y2-1,self.x1+2:self.x2-1])
                print 'Colour ',clr,' Recorded. '
                self.PAUSE=1 


    '''FUNCTION THAT IDENTIFIES THE COLOR IN ROI'''
    def colourDetector(self,frame):
        
        #:params section of frame which will be used as region of interest

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HLS)
        for clr in self.clrDict.keys():
            if self.clrDict[clr][0][0] == -1:
                    self.clrDict[clr][0][0],self.clrDict[clr][1][0] = 173,179
                    mask1 = cv2.inRange(frame,self.clrDict[clr][0],self.clrDict[clr][1])
                    self.clrDict[clr][0][0],self.clrDict[clr][1][0] = 0,5
                    mask2 = cv2.inRange(frame,self.clrDict[clr][0],self.clrDict[clr][1])
                    mask = cv2.bitwise_or(mask1,mask2)
                    self.clrDict[clr][0][0] == 1
            else:
                mask  = cv2.inRange(frame,self.clrDict[clr][0],self.clrDict[clr][1])
            if((mask==255).any()):
                cv2.putText(
                self.frame,
                clr,
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, # size 
                (255,255,255),
                1, # width 
                cv2.LINE_AA # anti-alised line 
            )

    '''RUNS WEBCAMERA AND DOES THE INTERACTION WITH USER'''
    def start(self):

        cap =cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 980)
        while True:

            if self.PAUSE:
                _,self.frame = cap.read()
            
            k = cv2.waitKey(1)

            if k == ord('s'):
                if self.PAUSE == 1:
                    self.PAUSE = 0 
                else:
                    self.PAUSE = 1
            
            # PRESS 't' START IDENTIFYING COLOR
            if k == ord('t'): 
                    self.SHOW_WINDOW=True

            #PRESS 'c' TO CLOSE 
            if k == ord('c'):
                break

            if self.SHOW_WINDOW:
                self.frameCopy = self.frame.copy()
                self.frame =cv2.rectangle(self.frame,(200,200),(350,350),(0,0,255),3,cv2.LINE_AA)
                self.colourDetector(self.frameCopy[200:350,200:350])

            cv2.setMouseCallback('IC',self.colorWindow)
            cv2.imshow('IC',self.frame)
            
        cap.release()
        cv2.destroyAllWindows()
        print (self.clrDict)


obj = detectColor()
obj.start()