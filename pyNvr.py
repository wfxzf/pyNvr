# Copyright (C) 2022  wfxzf

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os
import cv2
import time
import threading
from bypy import ByPy


#config
##camera's name
camname='cam01'
##local file path
pwd='G://videos//'
##video stream url
url='rtsp://username:password@ip:port/videopath'
##single video length（minute  1-1000）
blocktime=1


def bysync(file,path):
    time.sleep(10)
    bp = ByPy()
    code = bp.upload(file,'/'+path+'/')
    if code == 0:
        os.remove(file)
    


cap = cv2.VideoCapture(url)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
pwd = pwd + camname+'//'



while True:
    cu_pwd = pwd+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()))+'.avi'
    out = cv2.VideoWriter(cu_pwd, fourcc,fps, size)
    ret,frame = cap.read()
    start_time=int(time.time())
    brk = 0
    while ret:
        if int(time.time()-start_time >= blocktime*60 ):
            sync = threading.Thread(target=bysync, args=(cu_pwd,camname))
            sync.start()
            break
        ret,frame = cap.read()
        #cv2.imshow("frame",frame)
        out.write(frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #brk = 1
            #break
    #if brk == 1:
        #break
cv2.destroyAllWindows()
cap.release()
out.release()
