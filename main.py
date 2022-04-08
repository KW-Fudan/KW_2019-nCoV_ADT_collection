import shutil
import re, time, ljqpy, os
from datetime import datetime
from PIL import ImageGrab

from config import sttime

import uiautomation as uia
main = uia.WindowControl(ClassName='FileManagerWnd')
mm = main.GetChildren()[1].GetChildren()[-1]
msg = mm.GetChildren()[0].GetChildren()[-1].GetChildren()[0]

if os.path.exists('imgs'): shutil.rmtree('imgs')
os.mkdir('imgs')

datdir = os.path.join(os.environ['USERPROFILE'], 'Documents/WeChat Files')
x1 = [x for x in os.listdir(datdir) if x not in ['All Users', 'Applet']][0]
datdir = os.path.join(datdir, x1, 'FileStorage/Image', datetime.today().strftime('%Y-%m'))

def GetAllName(x, name=False):
    r = x.Name if name else ''
    rr = []
    for z in x.GetChildren():
        rr.append(GetAllName(z, name=True))
    if len(rr) > 0:
        rr = ' '.join(rr)
        r = r + f'({rr})'
    return r

def GetPic(st):
    rr = st.GetChildren()[0].GetChildren()[1].GetChildren()[1]
    if rr.IsOffscreen: return
    rect = rr.BoundingRectangle
    pic = ImageGrab.grab([rect.left, rect.top, rect.right, rect.bottom]) 
    return pic

allpics = []
alltext = set()
for i in range(100):
    for st in reversed(msg.GetChildren()):
        typ = st.Name
        st = st.GetChildren()[0].GetChildren()[1]
        text = re.sub('[\r\n]', ' ', GetAllName(st, name=True))
        if typ == '[图片]': text = typ + text
        if text in alltext: continue
        dt = ljqpy.RM(' ([0-9]{1,2}:[0-9]{2})\\)', text)
        if len(dt) == 4: dt = '0' + dt
        if dt < sttime: break
        if text.startswith('[图片]'):
            allpics.append(text)
        alltext.add(text)
        print(text[:100])
    if dt < sttime: break
    msg.WheelUp(wheelTimes=4, waitTime=0.5)

picdats = [fn for fn in ljqpy.ListDirFiles(datdir, filter=lambda x:x.endswith('.dat'))]
picdats.sort(key=lambda x:-os.path.getmtime(x))
for fn in picdats:
    mtime = os.path.getmtime(fn)
    dd = datetime.fromtimestamp(mtime)
    if dd.strftime('%m-%d') < datetime.today().strftime('%m-%d'): continue
    dd = dd.strftime('%H:%M')
    found = None
    for x in allpics:
        if dd[0] == '0': dd = dd[1:]
        if dd in x:
            with open(fn, 'rb') as fin: dat = fin.read()
            xkey = dat[0] ^ 0xFF
            ndat = bytes([x^xkey for x in dat])
            xx = x.replace(':', '-')
            with open(f'imgs/{xx}.png', 'wb') as fout: fout.write(ndat)
            print('found', x)
            found = x
            break
    if found: allpics.remove(found)


