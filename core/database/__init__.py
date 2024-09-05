import sqlite3
from contextlib import contextmanager
from core.logs import LOG_INFO, LOG_ERROR
import os
from core.config import DATABASE_DIR, DATABASE_NAME
from typing import Dict, Tuple, Optional

class Database:

    @staticmethod
    @contextmanager
    def connect():
        """上下文管理器，确保连接自动关闭"""
        conn = sqlite3.connect(os.path.join(DATABASE_DIR, DATABASE_NAME))
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def init():
        """初始化数据库，创建表"""
        if not os.path.exists(DATABASE_DIR):
            os.makedirs(DATABASE_DIR)
        with Database.connect() as cursor:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS cookies (
                domain TEXT PRIMARY KEY,
                cookie_string TEXT
            )
            """
            )



    @staticmethod
    def insert_cookies(data: Dict[str, Dict[str, str]]):
        """插入或更新 cookies"""
        with Database.connect() as cursor:
            for domain, cookies in data.items():
                # 将 cookies 字典转换为字符串
                cookie_string = ';'.join([f"{name}={value}" for name, value in cookies.items()])
                cursor.execute('''
                INSERT OR REPLACE INTO cookies (domain, cookie_string)
                VALUES (?, ?)
                ''', (domain, cookie_string))

    @staticmethod
    def fetch_cookies() -> Dict[str, Dict[str, str]]:
        """查询所有 cookies"""
        with Database.connect() as cursor:
            cursor.execute('SELECT domain, cookie_string FROM cookies')
            rows = cursor.fetchall()
            result = {}
            for domain, cookie_string in rows:
                # 将 cookie_string 转换回字典
                cookies = {}
                for pair in cookie_string.split(';'):
                    if '=' in pair:
                        name, value = pair.split('=', 1)
                        cookies[name] = value
                result[domain] = cookies
            return result
        
