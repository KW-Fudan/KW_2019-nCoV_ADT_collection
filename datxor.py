datfile = 'C:/Users/Ljq/Documents/WeChat Files/lsdefine/FileStorage/Image/2022-04/2e80fbc35923c0042420ad1c9468c32e.dat'

with open(datfile, 'rb') as fin:
    dat = fin.read()

print(hex(dat[0]))
print(hex(dat[1]))

xkey = dat[0] ^ 0xFF
xkey2 = dat[1] ^ 0xD8

print(hex(xkey), hex(xkey2))

ndat = bytes([x^xkey for x in dat])
with open('temp.png', 'wb') as fout:
    fout.write(ndat)