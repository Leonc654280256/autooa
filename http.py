import time
from typing import Tuple
import requests
import sys
import io
import ast
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  #改变标准输出的默认编码
all_record_times = []


def get_data():
    #登录时需要POST的数据
    data = {'username': '21306', 'password': '21306', 'logintype': 'employee'}

    #设置请求头
    headers = {
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

    #登录时表单提交到的地址（用开发者工具可以看到）
    login_url = 'http://119.57.137.242:49526/iclock/accounts/login/'

    #构造Session
    session = requests.Session()

    #在session中发送登录请求，此后这个session里就存储了cookie
    #可以用print(session.cookies.get_dict())查看
    try:
        resp = session.post(login_url, data)
    except:
        print("get seesion  error")
        return False
    else:
        print("get session successs")


    check_time = time.strftime("%Y-%m-%d", time.localtime())
    try:
       # record_url = "http://119.57.137.242:49526/iclock/staff/transactions/?starttime=%s&endtime=%s" % (check_time, check_time)
        record_url = "http://119.57.137.242:49526/iclock/staff/transactions/?starttime=2021-11-11&endtime=2021-11-11"
        record_res = session.post(record_url).content.decode('utf-8')
    except:
        print("get %s data error"  %(check_time))
        return False
    else:
        print("get %s data success: %s "  %(check_time, record_res))

    try:
        res = ast.literal_eval(record_res)

        for i in res:
            if len(i) > 2: 
                all_record_times.append(i[2])

        all_record_times.sort()
    except:
        print("parese failed")
        return False
    else: 
        print("parese success")
        print(all_record_times)
        return True
        

def send_email(buf):
    my_sender='654280256@qq.com'    # 发件人邮箱账号
  
    my_pass = 'gxvchfjtkpfnbgac'              # 发件人邮箱密码
  
    my_user='654280256@qq.com'      # 收件人邮箱账号，我这边发送给自己
  
  
    try:
  
         msg=MIMEText(buf,'plain','utf-8')
  
         msg['From']=formataddr(["leonc",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
  
         msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
  
         msg['Subject']="考勤数据提醒"                # 邮件的主题，也可以说是标题
  
  
  
         server=smtplib.SMTP("smtp.qq.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
  
         server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
  
         server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
  
         server.quit()  # 关闭连接
  
    except:  
      print("发送失败")
      return False
    else:
      print("发送成功")
      return True
   
     
  

  
  
  


def try_send_data():

    max_try_times = 0
    while max_try_times < 5:
        res = get_data()
        if res == False:
            print("get data failed")
            max_try_times = max_try_times + 1
            continue
        else:
            print("send data info to leonc")
            if send_email(" ".join(all_record_times)) != True :
                max_try_times = max_try_times + 1
                continue
            else:
               break
    

def main(argv=None):
   
    while True:
        try_send_data()
        time.sleep(31)
        minutes = time.strftime("%H:%M", time.localtime()) 
        if minutes == "09:28":
            try_send_data()
        elif minutes == "09:32":
            try_send_data()
        elif minutes == "18:30":
            try_send_data()
        elif minutes == "19:30":
            try_send_data()

if __name__ == "__main__":
    sys.exit(main())

        
  
