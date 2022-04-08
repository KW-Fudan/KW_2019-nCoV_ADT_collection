import os, ljqpy, math, shutil
import cv2
from PIL import Image, ImageDraw
import numpy as np

from config import alllist

def GetCode(s):
	mid = ljqpy.RM('\\]\\(\\((.+?)  ', s)
	return mid
	dname = ljqpy.RM('([0-9]{1,2}0[0-9])', mid)
	if dname == '': dname = mid
	#print(dname)
	return dname
	
if os.path.exists('ret'): shutil.rmtree('ret')
os.mkdir('ret')

from tqdm import tqdm
ret = {}
detector = cv2.wechat_qrcode_WeChatQRCode("detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel")
for fn in tqdm(os.listdir('imgs')):
	#if not '李吉萍' in fn: continue
	ffn = os.path.join('imgs', fn)
	img = Image.open(ffn)
	code = GetCode(fn)
	img = np.array(img) 
	res, points = detector.detectAndDecode(img)
	cnt = len(res)
	points = np.array(points, dtype='int32')
	for zz in points:
		cv2.polylines(img, points, True, color=(255,0,0), thickness=20)
	#print(cnt, code, res)
	ret.setdefault(code, []).append([cnt, res])
	newfn = f'ret/{code}_{cnt}.png'
	iimg = Image.fromarray(img)
	iimg.save(newfn)
	#cv2.imshow('a', img)
	#cv2.waitKey(0)

def tryint(x):
    try: return int(x)
    except: return 99999

codes = ret.keys()
alllist = list(codes)
lack = []
for x in alllist:
    if x not in codes:
        lack.append(x)
        ret.setdefault(x, []).append([-1, []])

ret = sorted(ret.items(), key=lambda x:tryint(x[0]))
csvs = [['微信群备注（户主）', '识别出上传数', '抗原ID']]
total = bad = 0
for x in ret:
	print(x)
	yy = max(x[1])
	if yy[0] == 0: bad += 1
	total += len(yy[1])
	csvs.append([x[0], yy[0] if yy[0] >= 0 else '未发现', ' '.join(yy[1])])

csvs.append(['', '', ''])
csvs.append([f'总检测数：{total}', '', ''])
csvs.append([f'无法识别的图片：{bad}', '', ''])
#csvs.append([f'未上传户数：{len(lack)}', '', ''])

print('\n总检测数：', total)
print('无法识别的图片：', bad)
#print('未上传户数：', len(lack))

ljqpy.SaveCSV(csvs, 'result.csv')
import pandas as pd
csv = pd.read_csv('result.csv', delimiter='\t')
csv.to_excel('result.xlsx', index=False)
