source /etc/profile
. ~/.bash_profile
#!/bin/bash

count=`ps -ef |grep python|grep fileserver.py|grep -v grep|wc -l`
if [ $count != 0 ];then
    echo $(date): "fileserver is running..."
else
    echo $(date): "Start fileserver success..."
    cd /home/wlsc/program/fileserver/src/ && nohup python fileserver.py > /dev/null 2>&1 &
fi