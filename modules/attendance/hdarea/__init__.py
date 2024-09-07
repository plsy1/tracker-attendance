import requests  # type: ignore
from typing import Dict
from modules.attendance import Site
from core.logs import LOG_ERROR, LOG_INFO
import re, random


class hdarea(Site, domain_suffixes=["hdarea.club"]):

    siteName = "好大"
    siteAttendanceURL = "https://hdarea.club/sign_in.php"

    @staticmethod
    def sign_in(credentials: Dict[str, str]):
        try:
            domain = credentials.get("domain")
            cookies = credentials.get("cookies")

            data = {"action": "sign_in"}

            response = super(hdarea, hdarea).sendRequest(
                cookies, hdarea.siteAttendanceURL, data=data, method="POST"
            )
            if response.status_code == 200:
                LOG_INFO(f"{hdarea.siteName}：签到成功")
                return True
            else:
                LOG_INFO(f"{hdarea.siteName} 签到失败")
                return False
        except Exception as e:
            LOG_ERROR(e)
