# fileserver
说明：基于Flask框架的图片、视频、文件上传下载服务，图片请求方式仿七牛图片处理规则，图片处理基于PIL。

开发环境需求： python  3.6.4

相关引用：Flask==1.1.1, Flask-Cors==3.0.8, Pillow==6.1.0, requests==2.18.4

样例：

图片资源访问：http://localhost:8084/get/img/20191123/1502077183067_15020771825066173358.jpg?imageView2/1/w/375

视频资源访问：http://localhost:8084/get/video/376ec831vodgzp1253857838_33ebc7499031868222983182282.mp4