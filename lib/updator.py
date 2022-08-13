import logging, requests
from lib.config import UpdateConfig
from .version import GiteaVersion

class GiteaUpdator:

    def __init__(self, conf : UpdateConfig) -> None:
        """ Initial updator and variables """
        
        self.Config = conf

        if (self.Config.isLogEnabled):
            # formatter of log content
            formatter = logging.Formatter(
                fmt='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M:%S'
            )
            # create a file handler which config specific
            logHdl = logging.FileHandler(self.Config.logFile, encoding="UTF-8")
            logHdl.setFormatter(formatter)
            # get root logger (without name)
            self.Log = logging.getLogger()
            self.Log.setLevel(logging.DEBUG)
            self.Log.addHandler(logHdl)
            self.Log.info("GiteaUpdator initializing with '%s'" % self.Config.configPath)
        
        print("Updator initialized")

    def CheckVersion(self) -> bool:
        """ check the version of local site which to update """

        # get local site version
        rsp = requests.post(self.Config.siteVersion)
        data = rsp.json()
        print(data)
        #localVer = GiteaVersion(data["version"])
        #print(localVer)
