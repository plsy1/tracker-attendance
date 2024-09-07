import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.logs import LOG_ERROR, LOG_INFO
import re, random


class haidan(Site, domain_suffixes=["www.haidan.video"]):

    siteName = "海胆"
    siteAttendanceURL = "https://www.haidan.video/signin.php"

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")

            response = super(haidan, haidan).sendRequest(
                cookies, haidan.siteAttendanceURL, method="POST"
            )
            if response.status_code == 200:
                LOG_INFO(f"{haidan.siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{haidan.siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
