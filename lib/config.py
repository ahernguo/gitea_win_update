import json
from enum import Enum

class CheckMode(str, Enum):
    """ The way to check local version """
    FILE = "cmd_call"
    API = "site_api"

class OverwriteMode(str, Enum):
    """ The way to replace .exe """
    Overwrite = "overwrite"
    BACKUP = "backup"

class UpdateConfig:

    def __init__(self, conf_file : str) -> None:
        """ Load config and initial it """

        self.__conf_file = conf_file

        with open(conf_file) as fs:
            self.__js = json.load(fs)
        
        if (not self.__js["release_url"]):
            raise Exception("'release_url' can not be null or empty")
        if (not self.__js["check_mode"]):
            raise Exception("'check_mode' can not be null or empty")
        if (not self.__js["overwrite_mode"]):
            raise Exception("'overwrite_mode' can not be null or empty")
        if (not self.__js["exe_path"]):
            raise Exception("'exe_path' can not be null or empty")
        if (not self.__js["service_name"]):
            raise Exception("'service_name' can not be null or empty")

        if (self.checkMode == CheckMode.API):
            if (not self.__js["local_version"]):
                raise Exception("'local_version' can not be null or empty")
            if ( not self.__js["token"]):
                raise Exception("'token' can not be null or empty")
        
        if (self.overwriteMode == OverwriteMode.BACKUP):
            if (not self.__js["backup_dir"]):
                raise Exception("'backup_dir' can not be null or empty")
        
    @property
    def configPath(self) -> str:
        return self.__conf_file

    @property
    def releaseUrl(self) -> str:
        """ the url indicate latest release of Gitea """
        return self.__js["release_url"]
    
    @property
    def siteVersion(self) -> str:
        """ the version api of your site to check """
        return self.__js["local_version"]
    
    @property
    def exePath(self) -> str:
        """ the filename without extension to replace """
        return self.__js["exe_path"]
    
    @property
    def serviceName(self) -> str:
        """ the service name to start or stop Gitea """
        return self.__js["service_name"]
    
    @property
    def isLogEnabled(self) -> bool:
        """ log enable/disable """
        return self.__js["log"] != ""

    @property
    def logFile(self) -> str:
        """ the directory to save logs """
        return self.__js["log"]

    @property
    def token(self) -> str:
        """ the token to access """
        return self.__js["token"]

    @property
    def checkMode(self) -> CheckMode:
        """ the mode to check local gitea version """
        return self.__js["check_mode"]

    @property
    def overwriteMode(self) -> OverwriteMode:
        """ the mode to overwrite .exe """
        return self.__js["overwrite_mode"]

    @property
    def backupDir(self) -> str:
        """ the directory to backup .exe """
        return self.__js["backup_dir"]