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

if True: #config
    #config
    ##choose netdisk ( 1 for baidunetdisk ; 2 for alinetdisk )
    netdisk = 1
    ##camera's name
    camname='cam01'
    ##local file path
    pwd='G://videos//'
    ##video stream url(see readme)
    url='rtsp://user:password@ip:port/videopath'
    ##single video length（minute  1-1000）
    blocktime=1
    ##up load to baidu netdisk? True or False.
    uptoby = True
    ##remove after upload? True or False.
    re_af_up = True

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
            #global floder_id
            floder_id = creat_res.file_id
            with open("config.conf", "a") as f:
                f.write(creat_res.file_id)
                f.close()
    else:
        print('netdisk config error ,only for 1 or 2')

def bysync(file,path,i,re_af_up ):
    if i >= 3:
        print(file+"upload error,check the internet, netdisk account and path.")
        return
    time.sleep(10)
    print(file+"  uploading.......")
    bp = ByPy()
    code = bp.upload(file,'/'+path+'/')
    if code == 0:
        if re_af_up == True:
            os.remove(file)
        print(file+" successfuly uploaded!")
    else:
        i=i+1
        print(file+"retry :"+str(i))
        bysync(file,path,i,re_af_up)

def alisync(file,path,i,re_af_up):
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
        alisync(file,path,i,re_af_up)
    if code != '':
        if re_af_up == True:
            os.remove(file)
        print(file+" successfuly uploaded!")
    else:
        i=i+1
        print(file+"retry :"+str(i))
        alisync(file,path,i,re_af_up)


def capture(url,camname,pwd,blocktime,uptoby,re_af_up,netdisk):
    try:
        cap = cv2.VideoCapture(url)
    except:
        print("can not capture video stream, please check your url or internet.")
    else:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps >= 30:
            fps = 30
        elif fps <=0:
            fps = 1
        print("fps:"+str(fps))
        size = (int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))), int(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        print("video size:"+str(size))
        pwd = pwd + camname+'//'
        if os.path.exists(pwd) == False:
            try:
                os.mkdir(pwd)
            except:
                print("文件夹可能创建错误，请手动创建文件夹")

    while True:
        cu_pwd = pwd+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()))+'.avi'
        out = cv2.VideoWriter(cu_pwd, fourcc,fps, size)
        ret,frame = cap.read()
        start_time=int(time.time())
        #brk = 0
        while ret:
            if int(time.time()-start_time >= blocktime*30):
                if uptoby == True and netdisk == 1:
                    sync = threading.Thread(target=bysync, args=(cu_pwd,camname,0,re_af_up))
                    sync.start()
                if uptoby == True and netdisk == 2:
                    sync = threading.Thread(target=alisync, args=(cu_pwd,camname,0,re_af_up))
                    sync.start()
                out.release()
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

if __name__ == '__main__':
    capture(url,camname,pwd,blocktime,uptoby,re_af_up,netdisk)
