import schedule, threading, time, random, fnmatch
from core.config import config
from core.logs import LOG_INFO, LOG_ERROR
from core.database import Database
from modules.attendance import Site
from modules.cookiecloud import Cookies
from modules.telegram import TGBOT



def getSiteName(domain):
    try:    
        patterns = config.getSitePatterns()

        for pattern, alias in patterns.items():
            if fnmatch.fnmatch(domain, pattern):
                return alias

        return domain
    
    except Exception as e:
            LOG_ERROR(e)

class Scheduler:
    @staticmethod
    def generate_random_time():
        random_hour = random.randint(0, 20)
        random_minute = random.randint(0, 59)
        random_time = f"{str(random_hour).zfill(2)}:{str(random_minute).zfill(2)}"
        return random_time
    


    @staticmethod
    def perform_attendance():
        message = '【站点签到】\n'
        try:
            data = Database.fetch_cookies()
            exclude_suffixes = config.getExcludeSuffixes()
            exclude_keywords = config.getExcludeKeywords()
            for domain, cookies in data.items():
                if any(domain.endswith(suffix) for suffix in exclude_suffixes):
                    continue
                if any(keyword in domain for keyword in exclude_keywords):
                    LOG_INFO(f"跳过签到：{domain}")
                    continue
                site_class = Site.get_site_class(domain)
                credentials = {"domain": domain, "cookies": cookies}
                siteName = getSiteName(domain)
                if site_class.sign_in(credentials):
                    message += (f'{siteName} 签到成功\n')
                else:
                    message += (f'{siteName} 签到失败\n')
            TGBOT.Send_Message(message)
        except Exception as e:
            LOG_ERROR(e)
            
    @staticmethod
    def autoAttendance():

        random_time_one = Scheduler.generate_random_time()
        random_time_two = Scheduler.generate_random_time()
        LOG_INFO(f"每日签到开启，生成随机执行时间：{random_time_one}, {random_time_two}")
        while random_time_two == random_time_one:
            random_time_two = Scheduler.generate_random_time()

        schedule.every().day.at(random_time_one).do(Scheduler.perform_attendance)
        schedule.every().day.at(random_time_two).do(Scheduler.perform_attendance)
    
    @staticmethod
    def updateCookies():
        Database.insert_cookies(Cookies.getCookies())
        
    @staticmethod    
    def daily_reset():
        schedule.clear()
        schedule.every().day.at("00:00").do(Scheduler.daily_reset)  
        Scheduler.autoAttendance()
        schedule.every(60).minutes.do(Scheduler.updateCookies)

    @staticmethod
    def Run():
        LOG_INFO(("程序启动，初始化调度任务......"))
        schedule.every().day.at("00:00").do(Scheduler.daily_reset)
        Scheduler.autoAttendance()
        schedule.every(60).minutes.do(Scheduler.updateCookies)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    @staticmethod        
    def Start():
        scheduler_thread = threading.Thread(target=Scheduler.Run, daemon=True)
        scheduler_thread.start()