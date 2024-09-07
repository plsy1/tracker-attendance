import importlib,time
from pathlib import Path
from modules.cookiecloud import Cookies
from core.database import Database
from core.scheduler import Scheduler



def auto_import_subclasses(package_name):
    '''
    自动载入子模块
    '''
    package = importlib.import_module(package_name)
    package_path = Path(package.__path__[0])
    for folder in package_path.iterdir():
        if folder.is_dir():
            init_file = folder / '__init__.py'
            if init_file.exists():
                module_path = f"{package_name}.{folder.name}"
                importlib.import_module(module_path)


def init():
    Database.init()
    Database.insert_cookies(Cookies.getCookies())
    auto_import_subclasses("modules.attendance")
    Scheduler.Start()
    
if __name__ == "__main__":
    init()
    Scheduler.perform_attendance()
    while True:
        time.sleep(1)