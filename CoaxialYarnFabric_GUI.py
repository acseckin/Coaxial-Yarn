# -*- coding: utf-8 -*-
"""
@author: A.Ç.SEÇKİN
seckin.ac@gmail.com
"""

import serial
from pynput import keyboard
import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import csv  


filename="deneme_001.csv"

status=0
def on_press(key):
    global status
    if key==keyboard.Key.esc:
        print("çıkış")
        status=-1
        return False
    pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1800,400)
win.setWindowTitle('pyqtgraph example: Plotting')
pg.setConfigOptions(antialias=True)

plots=[]
ocurves=[]
ccurves=[]
for i in range(16):
    plots.append(win.addPlot(title='Channel-'+str(i)))
    #plots[-1].setInteractive(True)
    ccurves.append(plots[-1].plot(pen=(0,255,0), name="ch_"+str(i)))
    ocurves.append(plots[-1].plot(pen=(255,0,0), name="offset_"+str(i)))
    if i%8==7:
        win.nextRow()

ser=serial.Serial('COM8',115200, timeout=5)
ser.flushInput()
ser.close()
ser.open()
sweeplen=200
indata=np.zeros((16,sweeplen))
offset=np.zeros((16,sweeplen))
offsetc=200
status=0
linecount=1

def update():
    global status,offset, offsetc, ser, ocurves, ccurves, indata,linecount
    inline = str(ser.readline().strip())
    inline=inline.replace("'","")
    info=inline.split(",")
    if len(info)!=(sweeplen+1):
        status=0
        print("okuma hatası")
    else:
        portid=info[0][1:-1]
        if portid.isnumeric():
            if status==0:
                status=1
            portid=int(portid)
            indata[portid]=np.array(info[1:]).astype(int)
            if offsetc==0:
                ccurves[portid].setData(indata[portid])
                ocurves[portid].setData(offset[portid]/200.0)
                if portid==15:
                    with open(filename,'a',newline='') as f:
                        b=indata.flatten()
                        writer = csv.writer(f,delimiter=';')
                        writer.writerow(b)
                        print("kayıt:",linecount)
                        linecount=linecount+1
            else:
                ccurves[portid].setData(np.zeros((16,sweeplen))[0])
                ocurves[portid].setData(np.zeros((16,sweeplen))[0])
            
                
        if ((offsetc!=0) and (status>0)):
            print("Offset verisi toplanıyor:",offsetc)
            offset=offset+indata
            offsetc=offsetc-1
            if (offsetc==0):
                print("offset verisi kayıt ediliyor.")
                with open(filename,'a',newline='') as f:
                    cnames=np.arange(1,3201)
                    b=offset/200.0
                    b=b.flatten()
                    writer = csv.writer(f,delimiter=';')
                    writer.writerow(cnames)
                    writer.writerow(b)
                    print("Offset verisi kayıt tamamlandı.",linecount)
                    linecount=linecount+1
                print("Deneye başlanabilir....")
    
    app.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0.05)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()   
        

            
            