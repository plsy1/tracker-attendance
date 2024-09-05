import yaml
import os, sys
from core.log import LOG_ERROR, LOG_INFO

DATABASE_DIR = 'data'
DATABASE_NAME = "data.db"

class ConfigManager:
    def __init__(self, config_file_path=None):
        try:
            current_dir = os.getcwd()
            config_file_path = os.path.join(current_dir, "conf/config.yaml")
            self.config = self.load_config(config_file_path)
        except Exception as e:
            LOG_ERROR(e)


    def load_config(self, config_file_path):
        with open(config_file_path, "r") as f:
            config = yaml.safe_load(f)
        return config


    def getCookieCloudConfig(self):
        try:
            result = self.config.get("cookiecloud", {})
            return result
        except Exception as e:
            LOG_ERROR(e)
            
    def getTelegramConfig(self):
        try:
            result = self.config.get("telegram", {})
            return result
        except Exception as e:
            LOG_ERROR(e)
            
    def getExcludeSuffixes(self):
        try:
            result = self.config.get('exclude_suffixes', [])
            return result
        except Exception as e:
            LOG_ERROR(e)
            
    def getExcludeKeywords(self):
        try:
            result = self.config.get('exclude_keywords', [])
            return result
        except Exception as e:
            LOG_ERROR(e)
            
    def getSitePatterns(self):
        try:
            result = self.config.get('sites', {})
            return result
        except Exception as e:
            LOG_ERROR(e)
            
config = ConfigManager()
