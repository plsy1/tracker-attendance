from PyCookieCloud import PyCookieCloud
from core.log import LOG_INFO,LOG_ERROR
from core.config import config
from typing import Dict

config = config.getCookieCloudConfig()
host = config.get('host')
uuid = config.get('uuid')
password = config.get('password')

class Cookies:
    '''
    返回domain:cookies形式的字典
    '''
    def getCookies() -> Dict[str, Dict[str, str]]:
        try:
            result = {}
            
            cookieCloud = PyCookieCloud(host, uuid, password)
            decrypted_data = cookieCloud.get_decrypted_data()
            
            for domain, cookies in decrypted_data.items():
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                result[domain] = cookie_dict

            return result
        
        except Exception as e:
            LOG_ERROR("getCookies", e)

