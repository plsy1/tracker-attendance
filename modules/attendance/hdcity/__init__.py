import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.logs import LOG_ERROR, LOG_INFO
import re, random


class hdcity(Site, domain_suffixes=["leniter.org"]):

    siteName = "高清城市"
    siteAttendanceURL = "https://hdcity.leniter.org/sign"

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")

            response = super(hdcity, hdcity).sendRequest(
                cookies, hdcity.siteAttendanceURL, method="POST"
            )
            if response.status_code == 200:
                LOG_INFO(f"{hdcity.siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{hdcity.siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
