import requests
from datetime import datetime

# 定义全局请求的url
URL_PREFIX = 'http://127.0.0.1:98'

# 测试使用的用户名
TEST_USERNAME = 'edp'
# 测试使用的密码
TEST_PASSWORD = 'admin'


def user_login():
    """用户登录"""
    url = f'{URL_PREFIX}/api/login'

    user_name, user_password = info_encrypt(TEST_USERNAME, TEST_PASSWORD)
    headers = {
        'request-time': generate_reqeust_time()
    }
    query_params = {
        'username': user_name,
        'password': user_password,
        'validateCode': '1234'
    }

    default_code = "1234"


    session = requests.Session()

    # Set the 'JCCODE' attribute in the session's cookies
    session.cookies.set(name='JCCODE', value=default_code)

    response = session.post(url, headers=headers, params=query_params)
    print(response.json())
    return response.json()['token']


def info_encrypt(user_name: str, user_password: str):
    """用户登录信息国密加密"""
    url = f'{URL_PREFIX}/api/system/encrypt'
    data = {
        'username': TEST_USERNAME,
        'password': TEST_PASSWORD,
    }
    user_name_content = {
        'content': user_name
    }

    headers = {
        'request-time': generate_reqeust_time()
    }
    response = requests.post(url, headers=headers, params=user_name_content)
    encrypt_user_name = response.json()['item']['ciphertext']

    user_password_content = {
        'content': user_password
    }
    response = requests.post(url, headers=headers, params=user_password_content)
    encrypt_user_password = response.json()['item']['ciphertext']
    return encrypt_user_name, encrypt_user_password


def generate_reqeust_time() -> str:
    """创建请求时间"""
    # Get the current date and time
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_captcha_image():
    """获取验证码"""
    url = f'{URL_PREFIX}/api/getCaptchaImg'
    headers = {
        'request-time': generate_reqeust_time()
    }
    response = requests.get(url, headers=headers)

    # print(response.__getattribute__('cookies')['JCCODE'])
    print(response.cookies)

    session = requests.Session()
    session_response = session.get(url, headers=headers)
    print(session_response.cookies)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Assuming the attribute 'JCCODE' is present in the response content
        if 'JCCODE' in response.text:
            # Extract the value of 'JCCODE' (you may need to use a more specific approach)
            jc_code_start = response.text.find('JCCODE') + len('JCCODE')
            jc_code_end = response.text.find('"', jc_code_start)
            jc_code = response.text[jc_code_start:jc_code_end]

            print('JCCODE:', jc_code)
        else:
            print('JCCODE not found in the response content.')
    else:
        print('Failed to retrieve data. Status code:', response.status_code)
        print('Error Response:', response.text)

    # return response.json()['item']['captcha']
def main():
    print(user_login())

if __name__ == '__main__':
    main()
