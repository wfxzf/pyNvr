# pyNvr
这是一个用Python编写的NVR(网络硬盘录像机)脚本，  
利用百度网盘进行视频的云存储
可以将废旧的安卓手机变成NVR节省购买云存储的钱。

`pip install bypy`  
`pip install opencv-python`  

`bypy info`  
打开链接，登录，填写授权码。  

编辑pyNvr.py,修改配置（摄像头名称canname、串流地址url、本地存储路径pwd，单个视频时长blocktime）


`nohup python pyNvr.py &`

附，常见IP摄像头串流地址  
海康威视  
    主码流：  
    rtsp://user:password@ip:554/h264/ch1/main/av_stream  
    子码流：  
    rtsp://user:password@ip:554/mpeg4/ch1/sub/av_stream  

大华  
    rtsp://username:password@ip:port/cam/realmonitor?channel=1&subtype=0  


三星  
    高码流rtsp地址：  
    rtsp://user:password@ip:554/onvif/profile2/media.smp（720P）  
    低码率rtsp地址  
    rtsp://user:password@ip:554/onvif/profile3/media.smp  

LG  
    高码流（主码流）RTSP地址：  
    rtsp://user:password@ip:554/Master-0  
    低码流（子码流）RTSP地址：  
    rtsp://user:password@ip:554/Slave-0  

TP-Link/水星安防  
    rtsp://user:password@ip:554/stream1  
    rtsp://user:password@ip:554/stream2  

