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
import numpy as np

if True: #config
    #config
    ##choose netdisk ( 1 for baidu netdisk ; 2 for ali netdisk ;else for don`t upload)
    netdisk = 1
    ##camera's name
    cameraName='cam01'
    ##local file path
    pwd='D://videos//'
    ##video stream url(see readme)
    url='rtsp://admin:admin@domain:port/stream1'
    #url='rtsp://127.0.0.1:8554/s001'
    ##single video length(minute  1-1000)
    blocktime = 1
    ##up load to baidu netdisk? True or False.
    bUploadToNetdisk = True
    ##remove after upload? True or False.
    bRemoveAfterUpload = False
    ##motion detect(True or False)
    bMotionDetect = False
    ##stop to capture when no motion after this time(second, 10-20 for advice)
    recordAfterAction = 10
    ##record time bebore action (second)
    recordBeforeAction = 3
    ##sensitivity(percentage,0 - 1)
    sensitivity = 0.3
    ##delete local file after this time(day,0 for don`t delete`)
    saveDays = 0


if True: #judge and pretreatment netdisk 
    if netdisk == 1:
        from bypy import ByPy
    elif netdisk == 2:
        from aligo import Aligo
        ali = Aligo()
        if os.path.exists('config.conf'):
            with open("config.conf", "r") as f:
                floder_id = f.readline()
                f.close()
        else:
            creat_res = ali.create_folder(name='IPcameras', parent_file_id='root')
            creat_res = ali.create_folder(name='IPcameras', parent_file_id=creat_res.file_id)
            floder_id = creat_res.file_id
            with open("config.conf", "a") as f:
                f.write(creat_res.file_id)
                f.close()
    else:
        print('will not upload to netdisk')

def bysync(file,path,i,bRemoveAfterUpload ):
    if i >= 3:
        print(file+"upload error,check the internet, netdisk account and path.")
        return
    time.sleep(10)
    print(file+"  uploading.......")
    bp = ByPy()
    code = bp.upload(file,'/'+path+'/')
    if code == 0:
        if bRemoveAfterUpload == True:
            os.remove(file)
        print(file+" successfuly uploaded!")
    else:
        i=i+1
        print(file+"retry :"+str(i))
        bysync(file,path,i,bRemoveAfterUpload)


def alisync(file,path,i,bRemoveAfterUpload):
    if i >= 3:
        print(file+"upload error,check the internet, netdisk account and path.")
        return
    time.sleep(10)
    ali = Aligo()
    code = ''
    global floder_id
    try:
        code = ali.upload_files(file_paths=[file],parent_file_id=floder_id)
    except Exception as e:
        print(e)
        i=i+1
        print(file+"retry :"+str(i))
        alisync(file,path,i,bRemoveAfterUpload)
    if code != '':
        if bRemoveAfterUpload == True:
            os.remove(file)
        print(file+" successfuly uploaded!")
    else:
        i=i+1
        print(file+"retry :"+str(i))
        alisync(file,path,i,bRemoveAfterUpload)

def detect(list,sensitivity):

    f = list[len(list)-8]
    l = list[len(list)-1]

    
    b,g,r = cv2.split(f)
    lb,lg,lr = cv2.split(l)

    # cv2.namedWindow('r',0)
    # cv2.resizeWindow('r',384,216)
    # cv2.imshow('r',f)
    # cv2.waitKey(10)

    mask = np.zeros((f.shape[0],f.shape[1]),dtype=np.uint8)
    histSize = 256
    histRange = (0, histSize) 
    #method = cv2.HISTCMP_CHISQR
    #method = cv2.HISTCMP_CORREL
    method = cv2.HISTCMP_BHATTACHARYYA
    difflist = []
    detectBlockNum = 4
    XbolckSize = f.shape[0]//detectBlockNum
    YbolckSize = f.shape[1]//detectBlockNum
    for i in range(0,f.shape[0]-XbolckSize,XbolckSize):
        for j in range(0,f.shape[1]-YbolckSize,YbolckSize):
            #print(np.sum(f[i:i+32,j:j+32])/(32*32))
            b_hist = cv2.calcHist([b[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)
            g_hist = cv2.calcHist([g[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)
            r_hist = cv2.calcHist([r[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)

            lb_hist = cv2.calcHist([lb[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)
            lg_hist = cv2.calcHist([lg[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)
            lr_hist = cv2.calcHist([lr[i:i+XbolckSize,j:j+YbolckSize]], [0], None, [histSize], histRange)
           
            diff = max(cv2.compareHist(b_hist, lb_hist, method),cv2.compareHist(g_hist, lg_hist, method),cv2.compareHist(r_hist, lr_hist, method))
            mask[i:i+XbolckSize,j:j+YbolckSize] = int(255 * diff)
                
            if diff > 0.2:
                print (str(i)+" "+str(j))
            difflist.append(diff)
    # cv2.namedWindow('mask',0)
    # cv2.resizeWindow('mask',384,216)
    # cv2.imshow('mask',mask)
    # cv2.waitKey(10)
    print(max(difflist))
    if max(difflist) >= sensitivity or sum(i > sensitivity*0.8 for i in difflist) > 2 or sum(i > sensitivity*0.7 for i in difflist) > 5: 
        return True
    return False


    # diff = cv2.absdiff(f,l)
    # f.astype("float")
    # diff.astype("float")
    # f = f + 0.000000000001
    # diffrate = np.divide(diff,f)
    # diffall = diffrate[:,:,0]+diffrate[:,:,1]+diffrate[:,:,2]
    # for i in range(1,diffall.shape[0]-32,32):
    #     for j in range(1,diffall.shape[1]-32,32):
    #         print(np.sum(diffall[i:i+32,j:j+32])/(32*32))
    #         if np.sum(diffall[i:i+32,j:j+32])/(32*32) >= sensitivity*3:                
    #             return True
    # return False


def motiondetect(url,cameraName,pwd,blocktime,bUploadToNetdisk,bRemoveAfterUpload,netdisk,sensitivity,recordAfterAction,bMotionDetect):
    
    try:
        print("****")
        cap = cv2.VideoCapture(url)
    except Exception as e:
        print("can not capture video stream, please check your url or internet.")
        print(e)
        exit()
    else:
        print("successfully capture !")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps >= 30:
            fps = 30
        elif fps <=0:
            fps = 5
        print("fps:"+str(fps))
        size = (int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))), int(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        print("video size:"+str(size))
        pwd = pwd + cameraName+'//'
        if os.path.exists(pwd) == False:
            try:
                os.mkdir(pwd)
            except Exception as e:
                print(e)
                print("place check or crate folder manually")
                exit()

    bCapture = not bMotionDetect
    bStop = False

    while True:
        cu_pwd = pwd+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()))+'.avi'
        out = cv2.VideoWriter(cu_pwd, fourcc,fps, size)
        try:
            ret,frame = cap.read()
        except Exception as e:
            print("can not capture video stream, please check your url or internet.")
            print(e)
            print("we will try again........")
            time.sleep(1)
            continue

        start_time=int(time.time())
        flist = [frame]
        action_time=int(time.time())
        detecttime = 0
        while ret:
            if (bCapture and (int(time.time())-start_time >= blocktime*60)) or bStop:
                if bUploadToNetdisk == True and netdisk == 1:
                    sync = threading.Thread(target=bysync, args=(cu_pwd,cameraName,0,bRemoveAfterUpload))
                    sync.start()
                if bUploadToNetdisk == True and netdisk == 2:
                    sync = threading.Thread(target=alisync, args=(cu_pwd,cameraName,0,bRemoveAfterUpload))
                    sync.start()
                out.release()
                bStop = False
                break
            #time.sleep(1/fps)
            try:
                ret,frame = cap.read()
            except Exception as e:
                print("connect error,please check,we wouldnot stop :"+e)
                continue
            if bMotionDetect:
                flist.append(frame)
                if (len(flist) < fps*recordBeforeAction):
                    continue
                while(len(flist) >= fps*recordBeforeAction):
                    del flist[0]
                detecttime = detecttime + 1
                if (detecttime >= int(fps)):
                    detecttime = 0
                    if detect(flist,sensitivity) :
                        if not bCapture:
                            start_time = int(time.time())
                            for f in flist:
                                out.write(f)
                        action_time =int(time.time())
                        bCapture = True
                        # cv2.namedWindow('s',0)
                        # cv2.resizeWindow('s',300,300)
                        # cv2.imshow('s',frame)
                        # cv2.waitKey(1) 
                        print("motion")
                    #print("no motion")
                if bCapture and int(time.time())-int(action_time) >= recordAfterAction:
                    #cv2.destroyAllWindows()
                    bStop = True
                    bCapture = False
            
            if bCapture:
                print("write")
                out.write(frame)

    cv2.destroyAllWindows()
    cap.release()
    out.release()

if __name__ == '__main__':
    
    while(1):
        try:
            motiondetect(url,cameraName,pwd,blocktime,bUploadToNetdisk,bRemoveAfterUpload,netdisk,sensitivity,recordAfterAction,bMotionDetect)
        except Exception as e:
            print(e)
            continue

