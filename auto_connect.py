""" 
    自动连接校园网
"""

import requests
from time import sleep
import tkinter as tk
import tkinter.font as tkFont

# region 配置请求参数
# 尝试连接次数
num_connect = 3 
configParameters = {
    'url': 'http://10.7.0.103:30004/byod/byodrs/login/defaultLogin', # 这个不是校园网页面的 url, 是发生请求的
    'headers': {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'userip=10.121.5.31',
        'Host': '10.7.0.103:30004',
        'Origin': 'http://10.7.0.103:30004',
        'Pragma': 'no-cache',
        'Referer': 'http://10.7.0.103:30004/byod/view/byod/template/templatePc.html?customId=-1&usermac=08bf-b8c1-285a&userip=10.121.5.31&userurl=https://www.bilibili.com/&original=https://www.bilibili.com/&ssid=E&nasRedirectUrl=http://10.7.0.103:30004/byod/index.html?usermac=08bf-b8c1-285a&userip=10.121.5.31&userurl=https://www.bilibili.com/&original=https://www.bilibili.com/&ssid=E',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'data': {
        'code': '',
        'codeTime': '',
        'dynamicPwdAuth': False,
        'guestManagerId': 0,
        'licenseCode': '',
        'serviceSuffixId': '-1',
        'shopIdE': None,
        'userGroupId': 0,
        'userName': '230021101224',  # 学号
        'userPassword': 'MDQwNDUy',  # 密码
        'validateCode': '',
        'validationType': 0,
        'wlannasid': None
    }
}
# endregion

# region # 验证表单数据填写
class ConfigParametersError(Exception):
    pass

def validate_config(config):
    # 检查url是否存在且非空
    if not config.get('url'):
        raise ConfigParametersError("URL is required")

    # 检查headers字段是否包含必要的键
    headers = config.get('headers', {})
    required_headers = ['Accept', 'Content-Type', 'User-Agent']
    for header in required_headers:
        if header not in headers or not headers[header]:
            raise ConfigParametersError(f"Header '{header}' is required and cannot be empty")

    # 检查data字段中的必填项
    data = config.get('data', {})
    required_data_fields = ['userName', 'userPassword', 'userGroupId']
    for field in required_data_fields:
        if field not in data or not data[field]:
            raise ConfigParametersError(f"'{field}' in data is required and cannot be empty")

    # 可选项可以设置默认值
    optional_fields = ['code', 'codeTime', 'licenseCode', 'validateCode', 'shopIdE', 'wlannasid']
    for field in optional_fields:
        if field in data and not data[field]:
            print(f"Optional field '{field}' is empty, but this is allowed.")

    print("All required fields are filled correctly.")
# endregion

# region 登录尝试弹窗
def show_message(title, message):
    """ 显示弹窗消息 """
    root = tk.Tk()
    root.title(title)
    root.geometry("300x100")
    root.resizable(False, False)

    font = tkFont.Font(family="Microsoft YaHei", size=12)
    label = tk.Label(root, text=message, padx=10, pady=10, font=font)
    label.pack(expand=True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 100
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.after(5000, root.destroy)
    root.mainloop()
# endregion    

# region 尝试登陆发送请求
def make_request():
    """发送登录请求并返回响应"""
    try:
        response = requests.post(configParameters.url, headers=configParameters.headers, json=configParameters.data)
        response.raise_for_status()  # 检查 HTTP 错误
        return response
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return None
# endregion

# region 尝试登录并显示结果
def login():
    for attempt in range(3):
        print(f"尝试第 {attempt + 1} 次登录...")
        response = make_request()

        if response:
            result = response.json()
            if result.get('code') == 0:
                show_message('School Website', '   登录成功 ！')
                return
            else:
                show_message(f'登录失败 (尝试 {attempt + 1})', f'登录失败: {result.get("msg")}')
        else:
            show_message(f'请求失败 (尝试 {attempt + 1})', '请求失败')

        sleep(2) # 定义重试时间, 不要太快会被限制访问
# endregion

if __name__ == "main":
    login()