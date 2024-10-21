import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.logs import LOG_ERROR, LOG_INFO
import re, random


class lemonhd(Site, domain_suffixes=["lemonhd.club"]):

    siteName = "柠檬"
    siteAttendanceURL = "https://lemonhd.club/attendance.php"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")

            response = super(lemonhd, lemonhd).sendRequest(
                cookies, lemonhd.siteAttendanceURL, headers=lemonhd.headers,method="GET"
            )
            if response.status_code == 200:
                LOG_INFO(f"{lemonhd.siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{lemonhd.siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
