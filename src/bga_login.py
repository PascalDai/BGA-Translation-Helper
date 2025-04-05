import requests
from typing import Dict, Optional
import json
import re
import uuid
import time
import random
from datetime import datetime

class BGALogin:
    def __init__(self, username: str = None, password: str = None):
        self.base_url = "https://zh-cn.boardgamearena.com"
        self.session = requests.Session()
        self._setup_headers()
        self.request_token = None
        self._setup_cookies()
        self.retry_delay = 60  # 重试等待时间（秒）
        self.max_retries = 3   # 最大重试次数
        self.username = username
        self.password = password
    
    def _setup_headers(self):
        """设置基本的请求头"""
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': self.base_url,
            'referer': f'{self.base_url}/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Google Chrome";v="122", "Not(A:Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'connection': 'keep-alive'
        }
    
    def _setup_cookies(self):
        """设置初始 cookies"""
        # 生成一个随机的 PHPSESSID
        php_sessid = ''.join([str(uuid.uuid4()).replace('-', '')[:26]])
        
        # 设置初始 cookies
        self.session.cookies.set('__stripe_mid', str(uuid.uuid4()))
        self.session.cookies.set('_gid', 'GA1.2.2063708604.1743730001')
        self.session.cookies.set('_ga', 'GA1.1.1764613420.1706763765')
        self.session.cookies.set('PHPSESSID', php_sessid)
        self.session.cookies.set('social_disable_autoconnect', '1')
        
        # 设置初始的 registrationState
        registration_state = {
            "username": None,
            "emailAddress": None,
            "password": None,
            "numSteps": 2,
            "loginSource": "email",
            "emailIsInvalid": False
        }
        self.session.cookies.set('registrationState', json.dumps(registration_state))
    
    def _update_request_token(self, token: str):
        """更新请求令牌"""
        self.request_token = token
        self.headers['x-request-token'] = token
        print(f"已更新 request_token: {token}")
    
    def _handle_rate_limit(self, response_data: Dict) -> int:
        """
        处理速率限制，返回需要等待的秒数
        
        Args:
            response_data: 响应数据
            
        Returns:
            int: 需要等待的秒数
        """
        if 'wait_until' in response_data:
            wait_until = int(response_data['wait_until'])
            now = int(time.time())
            wait_seconds = max(0, wait_until - now)
            return wait_seconds
        return self.retry_delay
    
    def get_request_token(self) -> Optional[str]:
        """
        从 BGA 登录页面获取 request_token
        
        Returns:
            Optional[str]: 获取到的 request_token，如果获取失败则返回 None
        """
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    wait_time = self.retry_delay * (attempt + 1)
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                
                print("正在访问 BGA 登录页面...")
                # 添加随机延迟
                time.sleep(1.5 + random.random())
                
                # 先访问登录页面
                login_url = f"{self.base_url}/welcome"
                response = self.session.get(
                    login_url,
                    headers=self.headers,
                    allow_redirects=True
                )
                
                if response.status_code != 200:
                    print(f"访问登录页面失败，状态码: {response.status_code}")
                    print(f"响应内容: {response.text[:200]}")
                    continue
                
                # 保存响应内容到文件以便调试
                with open('login_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("已保存登录页面内容到 login_page.html")
                
                # 尝试多种正则表达式模式来匹配 request_token
                patterns = [
                    r'requestToken:\s*["\']([^"\']+)["\']',
                    r'requestToken:\s*([^"\'\s,}]+)',
                    r'bgaConfig\s*=\s*{[^}]*requestToken:\s*["\']([^"\']+)["\']',
                    r'request_token:\s*["\']([^"\']+)["\']',
                    r'request_token:\s*([^"\'\s,}]+)',
                    r'bgaConfig\s*=\s*{[^}]*request_token:\s*["\']([^"\']+)["\']'
                ]
                
                for pattern in patterns:
                    token_match = re.search(pattern, response.text, re.IGNORECASE)
                    if token_match:
                        token = token_match.group(1)
                        self._update_request_token(token)
                        return token
                
                print("未找到 request_token")
                print("响应内容片段:", response.text[:500])
            except Exception as e:
                print(f"获取 request_token 失败: {str(e)}")
                if attempt < self.max_retries - 1:
                    continue
        
        return None
    
    def check_username(self, username: str) -> Dict:
        """
        检查用户名是否可用
        
        Args:
            username: 要检查的用户名
            
        Returns:
            Dict: 包含检查结果的响应
        """
        # 由于我们是登录而不是注册，所以直接返回成功
        print(f"跳过用户名检查: {username}")
        return {"success": True}
    
    def login_with_password(self, username: str, password: str, remember_me: bool = False) -> Dict:
        """
        使用用户名和密码登录
        
        Args:
            username: 用户名
            password: 密码
            remember_me: 是否记住登录状态
            
        Returns:
            Dict: 登录响应结果
        """
        if not self.request_token:
            raise ValueError("Request token is required for login")
        
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    wait_time = self.retry_delay * (attempt + 1)
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                
                # 添加随机延迟
                time.sleep(1 + random.random())
                    
                url = f"{self.base_url}/account/auth/loginUserWithPassword.html"
                data = {
                    'username': username,
                    'password': password,
                    'remember_me': 'true' if remember_me else 'false',
                    'request_token': self.request_token
                }
                
                # 更新 registrationState
                registration_state = {
                    "username": username,
                    "emailAddress": None,
                    "password": password,
                    "numSteps": 2,
                    "loginSource": "email",
                    "emailIsInvalid": False
                }
                self.session.cookies.set('registrationState', json.dumps(registration_state))
                
                print(f"正在尝试登录: {username}")
                response = self.session.post(
                    url,
                    data=data,
                    headers=self.headers,
                    allow_redirects=True
                )
                
                if response.status_code != 200:
                    print(f"登录请求失败，状态码: {response.status_code}")
                    print(f"响应内容: {response.text[:200]}")
                    continue
                
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    print("无法解析响应 JSON")
                    print(f"响应内容: {response.text[:200]}")
                    continue
                
                if result.get('status') == 1:
                    print("登录成功")
                    return result
                elif result.get('status') == 0:
                    error = result.get('error', '未知错误')
                    print(f"登录失败: {error}")
                    
                    # 检查是否需要等待
                    if 'wait_until' in result:
                        wait_seconds = self._handle_rate_limit(result)
                        if wait_seconds > 0 and attempt < self.max_retries - 1:
                            print(f"需要等待 {wait_seconds} 秒")
                            time.sleep(wait_seconds)
                            continue
                    
                    return result
                else:
                    print(f"未知响应状态: {result}")
                    continue
                    
            except Exception as e:
                print(f"登录过程中发生错误: {str(e)}")
                if attempt < self.max_retries - 1:
                    continue
                return {"status": 0, "error": str(e)}
        
        return {"status": 0, "error": "超过最大重试次数"}
        
    def login(self) -> bool:
        """
        执行登录流程
        
        Returns:
            bool: 登录是否成功
        """
        try:
            # 获取 request_token
            if not self.get_request_token():
                print("获取 request_token 失败")
                return False
            
            # 执行登录
            login_result = self.login_with_password(self.username, self.password)
            
            # 检查登录结果
            if login_result.get('status') == 1:
                print("登录成功")
                return True
            else:
                error_msg = login_result.get('error', '未知错误')
                print(f"登录失败: {error_msg}")
                return False
                
        except Exception as e:
            print(f"登录过程中发生错误: {str(e)}")
            return False 