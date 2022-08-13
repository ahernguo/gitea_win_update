import json

class UpdateConfig:

    def __init__(self, conf_file : str) -> None:
        """ Load config and initial it """

        self.__conf_file = conf_file

        with open(conf_file) as fs:
            self.__js = json.load(fs)
        
        if (not self.__js["release_url"]):
            raise Exception("'release_url' can not be null or empty")
        if (not self.__js["local_version"]):
            raise Exception("'local_version' can not be null or empty")
        if (not self.__js["exe_name"]):
            raise Exception("'exe_name' can not be null or empty")
        if (not self.__js["service_name"]):
            raise Exception("'service_name' can not be null or empty")
        if (not self.__js["log"]):
            print("Disable logging.")
        
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
    def root(self) -> str:
        """ the Gitea root directory """
        return self.__js["exe_dir"]

    @property
    def exeName(self) -> str:
        """ the filename without extension to replace """
        return self.__js["exe_name"]
    
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