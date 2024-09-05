from typing import  Dict
from core.logs import LOG_ERROR,LOG_INFO
from core.config import config
import requests, fnmatch # type: ignore
class DefaultSite:
    
    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get('domain')
            cookies = credentials.get('cookies')
            
            siteName = DefaultSite.getSiteName(domain)
            siteAttendanceURL = f'https://{domain}/attendance.php'
            response = DefaultSite.sendRequest(cookies, siteAttendanceURL, method='GET')
            if response.status_code == 200:
                LOG_INFO(f"{siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
            
    @staticmethod
    def sendRequest(cookies, url, host=None, headers=None, data=None, method='GET'):
        """
        发送 HTTP 请求，并根据响应状态码返回布尔值。

        :param cookies: 要发送的 cookies
        :param url: 请求的 URL
        :param host: 请求的主机（可选）
        :param headers: 请求的头部（可选）
        :param data: 请求的正文（仅适用于 POST 请求）
        :param method: 请求的方法（'GET' 或 'POST'）
        :return: 请求是否成功（状态码为 200）
        """
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=10)
            else:
                raise ValueError("Unsupported HTTP method provided. Use 'GET' or 'POST'.")
            return response

        except Exception as e:
            LOG_ERROR(e)


    @staticmethod
    def getSiteName(domain):
        try:    
            patterns = config.getSitePatterns()

            for pattern, alias in patterns.items():
                if fnmatch.fnmatch(domain, pattern):
                    return alias

            return domain
        
        except Exception as e:
                LOG_ERROR(e)