# !/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os, shutil
import smtplib
from email.mime.text import MIMEText
import datetime

pause = 100 #间隔多少秒检测一次
tem_threshold = 75 #阈值温度
mailto_list=['zcy0016@163.com']  #你自己接收的邮箱，可以设置多个
mail_host="smtp.163.com"
mail_user="GPU_Monitor" #发送警报的邮箱
mail_pass="GPUMonitor123" #不是登录密码，是STMP密码
mail_postfix="163.com"

def send_email(to_list,sub,content):
    me="GPU Auto Monitor"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception:
        print("send error!!!")
        return False

def get_gpu_tem():
    shell_str = "tem_line=`nvidia-smi | grep %` && tem1=`echo $tem_line | cut -d C -f 1` " \
                "&& tem2=`echo $tem1 | cut -d % -f 2` && echo $tem2"
    result = os.popen(shell_str)
    result_str = result.read()
    tem_str = result_str.split("\n")[0]
    result.close()
    return float(tem_str)

while(True):
    try:
        tem_num = get_gpu_tem()
        if tem_num>tem_threshold:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            warning_str = nowTime+"  Current temperature is " + str(tem_num) + "!!!"
            print(warning_str)
            send_email(mailto_list, "GPU Warning!!!", warning_str)
            print("send over")

    finally:
        time.sleep(pause)
