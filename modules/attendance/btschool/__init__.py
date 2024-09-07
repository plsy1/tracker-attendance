import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.logs import LOG_ERROR, LOG_INFO
import re, random


class btschool(Site, domain_suffixes=["btschool.club"]):

    siteName = "学校"
    siteAttendanceURL = "https://pt.btschool.club/index.php?action=addbonus"

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")

            response = super(btschool, btschool).sendRequest(
                cookies, btschool.siteAttendanceURL, method="GET"
            )
            if response.status_code == 200:
                LOG_INFO(f"{btschool.siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{btschool.siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
