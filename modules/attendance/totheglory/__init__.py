import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.log import LOG_ERROR,LOG_INFO
import re

class totheglory(Site, domain_suffixes=["totheglory.im"]):
    
    siteName = 'TTG'
    siteAttendanceURL = 'https://totheglory.im/signed.php'
    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            
            domain = credentials.get('domain')
            cookies = credentials.get('cookies')
            
            response = super(totheglory, totheglory).sendRequest(cookies, 'https://totheglory.im/index.php', method='GET')
            pattern = r'signed_timestamp:\s*"(\d+)",\s*signed_token:\s*"([a-f0-9]+)"'
            match = re.search(pattern, response.text)
            timestamp, token = match.groups()
            data = {"signed_timestamp": timestamp, "signed_token": token}
            response = super(totheglory, totheglory).sendRequest(cookies, totheglory.siteAttendanceURL, data=data, method='POST')
            if response.status_code == 200:
                LOG_INFO(f"{totheglory.siteName}：签到成功")
                return {totheglory.siteName:'签到成功'}
            else:
                LOG_INFO(f"{totheglory.siteName} 签到失败")
                return {totheglory.siteName:'签到失败'}

        except Exception as e:
            LOG_ERROR(e)
