import cv2
import numpy as np
import matplotlib.pyplot as plt 

img = cv2.imread('plus3.jpg')
# img = cv2.imread('cross3.jpg')

img = cv2.medianBlur(img,5)
img = cv2.bilateralFilter(img,9,75,75)
img = cv2.medianBlur(img,5)

plt.imshow(img)
plt.show()

#------------------------image 1--------------------------------------
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255,0)
_,contours,hierarchy = cv2.findContours(thresh,2,1)

cnt = contours[1]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

print("number of defects img_1 : ",defects.shape[0])

l1 = []
for i in range(defects.shape[0]):
	s,e,f,d = defects[i,0]
	if d>200 :
		p = d//256
		l1.append(p)
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		cv2.line(img,start,end,[0,255,0],3)
		cv2.circle(img,far,2,[0,0,255],7)


plt.imshow(img)
plt.show()

#-----------------image 2---------------------------------------------
img = cv2.imread('cross.png')

img = cv2.medianBlur(img,5)
img = cv2.blur(img,(2,2))
img = cv2.medianBlur(img,5)

plt.imshow(img)
plt.show()

img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255,0)
_,contours,hierarchy = cv2.findContours(thresh,2,1)
cnt = contours[1]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

print("number of defects img_1 : ",defects.shape[0])
print(defects[0])

l2 = []
for i in range(defects.shape[0]):
	s,e,f,d = defects[i,0]
	if d>200 :
		p = d//256
		l2.append(p)
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		cv2.line(img,start,end,[0,255,0],3)
		cv2.circle(img,far,2,[0,0,255],7)


plt.imshow(img)
plt.show()

s = sum(l1)
for i in range(len(l1)):
	l1[i] = l1[i]/s

s = sum(l2)
for i in range(len(l2)):
	l2[i] = l2[i]/s


print("l1 : ",sorted(l1,reverse = True))
print("l2 : ",sorted(l2,reverse=True))

if l1==l2:
	print("MATCHED")