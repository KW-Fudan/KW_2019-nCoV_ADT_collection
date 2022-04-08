import os, sys, time, ljqpy, re

xs = os.listdir('imgs')

def GetCode(s):
    mid = ljqpy.RM('\\]\\(\\((.+?)  ', s)
    dname = ljqpy.RM('([0-9]{1,2}0[0-9])', mid)
    if dname == '': dname = mid
    #print(dname)
    return dname

def tryint(x):
    try: return int(x)
    except: return 99999

codes = [GetCode(x) for x in xs]
codes.sort(key=lambda x:tryint(x))
    
print('\n检测到')
print(','.join(codes))

alllist = [f'{i}0{j}' for i in range(1, 16) for j in range(1, 5)]
lack = []
for x in alllist:
    if x not in codes:
        lack.append(x)

print('\n缺少')
print(','.join(lack))

print('\n未识别')
print(','.join([x for x in codes if tryint(x) >= 9999]))