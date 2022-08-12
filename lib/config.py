
import json
import sys

class UpdateConfig:

    def __init__(self, conf_file:str) -> None:
        """ Load config and initial it """

        with open(conf_file) as fs:
            js = json.load(fs)
        
        self.__release : str = js["release_url"]
        self.__tar_ver : str = js["local_version"]
        self.__root : str = js["exe_dir"]
        self.__exe_name : str = js["exe_name"]
        self.__svc_name : str = js["service_name"]
        self.__log_name : str = js["log"]
        
        if (not self.__release):
            raise Exception("'release_url' can not be null or empty")
        if (not self.__tar_ver):
            raise Exception("'local_version' can not be null or empty")
        if (not self.__root):
            raise Exception("'exe_dir' can not be null or empty")
        if (not self.__exe_name):
            raise Exception("'exe_name' can not be null or empty")
        if (not self.__svc_name):
            raise Exception("'service_name' can not be null or empty")
        if (not self.__log_name):
            print("Disable logging.")
        
    @property
    def releaseUrl(self) -> str:
        """ the url indicate latest release of Gitea """
        return self.__release
    
    @property
    def siteVersion(self) -> str:
        """ the version api of your site to check """
        return self.__tar_ver
    
    @property
    def root(self) -> str:
        """ the Gitea root directory """
        return self.__root

    @property
    def exeName(self) -> str:
        """ the filename without extension to replace """
        return self.__exe_name
    
    @property
    def serviceName(self) -> str:
        """ the service name to start or stop Gitea """
        return self.__svc_name
    
    @property
    def isLogEnabled(self) -> bool:
        """ log enable/disable """
        return self.__log_name != ""

    @property
    def logFile(self) -> str:
        """ the directory to save logs """
        return self.__log_name