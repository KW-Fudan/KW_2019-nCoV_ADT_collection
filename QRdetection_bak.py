import os, ljqpy, math
import cv2
from PIL import Image, ImageDraw
import numpy as np
from pyzbar import pyzbar

def GetCode(s):
	mid = ljqpy.RM('\\]\\(\\((.+?)  ', s)
	dname = ljqpy.RM('([0-9]{1,2}0[0-9])', mid)
	if dname == '': dname = mid
	#print(dname)
	return dname

def detecte(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#// Convert Image captured from Image Input to GrayScale	
	canny = cv2.Canny(gray, 100, 200, 3) #Apply Canny edge detection on the gray image
	contours, hierachy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#Find contours with hierarchy
	return contours, hierachy

def dist(x, y):
	return np.sqrt(((x - y)**2).sum())

def drawline(img, pt1, pt2):
	cv2.line(img, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), color=(0,0,255), thickness=2)


def conter(image):
	global hierarchy, centers, contours
	contours, hierarchy = detecte(image)
	hierarchy = hierarchy[0]
	
	centers = np.zeros([len(contours), 2])
	areas = []
	M = {}

	for i in range(len(contours)):
		rect = cv2.minAreaRect(contours[i])
		box = cv2.boxPoints(rect)
		x, y, w, h = cv2.boundingRect(box)
		centers[i][0] = x + w*0.5
		centers[i][1] = y + h*0.5
		areas.append(w * h)

	inds = sorted(list(range(len(contours))), key=lambda x:areas[x])

	cens = []
	thre = 3
	rec = set()
	for k, i in enumerate(inds):
		if areas[i] < 10: continue
		for k1 in range(k+1, len(inds)):
			i1 = inds[k1]
			if areas[i1] < areas[i] * 1.2: continue
			if areas[i1] > areas[i] * 4: break
			if dist(centers[i], centers[i1]) > thre: continue
			for k2 in range(k1+1, len(inds)):
				i2 = inds[k2]
				if areas[i2] < areas[i1] * 1.2: continue
				if areas[i2] > areas[i1] * 4: break
				if dist(centers[i1], centers[i2]) > thre: continue
				xs = {i, i1, i2}
				print(xs)
				rec |= xs
				cens.append(centers[i1])

	for i in rec:
		cv2.circle(image, (int(centers[i][0]), int(centers[i][1])), radius=3, color=(0,255,0))
	cv2.drawContours(image, [contours[i] for i in rec], -1, (0, 255, 0), 1)

	ret = []
	for i in range(len(cens)):
		for i1 in range(i+1, len(cens)):
			d1 = dist(cens[i], cens[i1])
			for i2 in range(i1+1, len(cens)):
				d2, d3 = dist(cens[i], cens[i2]), dist(cens[i1], cens[i2])
				mn, mx = min(d1, d2, d3), max(d1, d2, d3)
				mid = d1+d2+d3-mn-mx
				if mn < 10: continue
				print(abs(mn*mn + mid*mid - mx*mx) / mx*mx)
				if abs(mn*mn + mid*mid - mx*mx) / mx*mx < 1.2:
					ret.append((i,i1,i2))
				#if abs(mn-mid) < 3 and abs(mx - mid * math.sqrt(2)) < 3:
				#	ret.append((i,i1,i2))

	for i, j, k in ret:
		drawline(image, cens[i], cens[j])
		drawline(image, cens[j], cens[k])
		drawline(image, cens[k], cens[i])

	cv2.imshow('a', image)
	cv2.waitKey(0)
	return ret

	
def GetCnt(img):
	res = pyzbar.decode(img)
	draw = ImageDraw.Draw(img)
	for xx in res:
		draw.polygon(xx.polygon, outline=(255,0,0), width=5)
	img.show()
	return len(res)

detector = cv2.wechat_qrcode_WeChatQRCode("detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel")
for fn in os.listdir('imgs'):
	if not '李吉萍' in fn: continue
	ffn = os.path.join('imgs', fn)
	img = Image.open(ffn)
	code = GetCode(fn)
	img = np.array(img) 
	res, points = detector.detectAndDecode(img)
	cnt = len(res)
	print(res, points)
	#contours, hierachy = detecte(img)
	#print(conter(img))
	#cnt = GetCnt(img)
	#print(cnt, fn)