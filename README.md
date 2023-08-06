# pyNvr
这是一个用Python编写的NVR(网络硬盘录像机)脚本，  
利用阿里网盘或者百度网盘进行视频的云存储
可以将废旧的安卓手机变成NVR节省购买云存储的钱。  

## 安卓手机
在安卓手机上，使用termux无法安装opencv，可以通过tmoe部署proot容器中的ubuntu  
安装tmoe:  
`bash -c "$(curl -Lv gitee.com/mo2/linux/raw/master/debian.sh)"`  
过程很简单，不多赘述了，图形界面没必要装。  
  
  
**更建议使用Aidlux，安卓手机上Aidlux很方便，可以直接使用python，已经装好了opencv，比Termux更方便快捷。安装bypy并登录就可以直接使用了。**  

安装python  
如果使用百度网盘：  
`pip install bypy`  
`bypy info`  
复制链接粘贴到浏览器打开，登录，填写授权码。  
如果使用阿里云盘：  
`pip install aligo`

安装opencv：  
`pip install opencv-python`Aidlux不需要。  
创建保存视频的文件夹,例如：  
`mkdir /home/videos`  
`mkdir /home/videos/cam01`  
一定要创建好路径，并且跟配置的路径一致，最后一层文件夹的名称为摄像头名称（camname）,参数pwd写到倒数第二层文件夹，以//结尾即可。
编辑pyNvr.py,修改配置（选择netdisk（netdisk = 1为百度，2为阿里），摄像头名称camname、串流地址url、本地存储路径pwd，单个视频时长blocktime,开启储存到百度网盘upyoby，上传完成后删除本地文件re_af_up）

运行：  
`cd pyNvr`  
运行：  
`python pyNvr.py`  
如果使用阿里网盘，第一次使用需要登录（百度已经登陆过）  
如果二维码显示错乱，需要新建一个终端，手动找到/tmp中的图片复制到手机可以直接访问的文件夹中，扫描，如：  
`cp /tmp/tmp56sdcc.png /sdcard/DCIM/QRcode.png`  
打开文件管理，找到DCIM文件夹下的这张图，扫描即可。  
 测试没有问题后，`ctrl + C`终止程序。  
后台运行程序:  
`nohup python pyNvr.py &`  

## 程序极其简陋，稳定和安全毫无保障，仅仅用于不含任何隐私信息、图省钱省事还想多一层云备份的情况
## 仅建议用于linux不完整的安卓手机，云服务器、实体机、树莓派建议使用知名开源或商业软件，如Bluecherry,Motion等。

附，国内常见IP摄像头串流地址:  
>海康威视  
>    主码流：  
>    rtsp://user:password@ip:554/h264/ch1/main/av_stream  
>    子码流：  
>    rtsp://user:password@ip:554/mpeg4/ch1/sub/av_stream  
>
>大华  
>    rtsp://username:password@ip:port/cam/realmonitor?channel=1&subtype=0  
>
>TP-Link/水星安防  
>    rtsp://user:password@ip:554/stream1  
>    rtsp://user:password@ip:554/stream2  
>三星  
>    高码流rtsp地址：  
>    rtsp://user:password@ip:554/onvif/profile2/media.smp（720P）  
>    低码率rtsp地址  
>    rtsp://user:password@ip:554/onvif/profile3/media.smp  
>
>LG  
>    高码流（主码流）RTSP地址：  
>    rtsp://user:password@ip:554/Master-0  
>    低码流（子码流）RTSP地址：  
>    rtsp://user:password@ip:554/Slave-0  



