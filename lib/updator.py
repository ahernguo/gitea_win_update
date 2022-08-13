import logging, os, requests, sys
from .config import CheckMode, UpdateConfig
from .version import GiteaVersion

class GiteaUpdator:

    def __init__(self, conf_file : str) -> None:
        """ Initial updator and variables """
        
        # load config
        self.Config = UpdateConfig(conf_file)

        # get root logger (without name)
        self.Log = logging.getLogger()
        self.Log.setLevel(logging.DEBUG)
        
        # create stdout stream handler that showing info like `print`
        stmHdl = logging.StreamHandler(sys.stdout)
        self.Log.addHandler(stmHdl)

        # if user choose to log to file. create file handler
        if (self.Config.isLogEnabled):
            # formatter of log content
            formatter = logging.Formatter(
                fmt="%(asctime)s %(levelname)-8s %(message)s",
                datefmt="%m-%d %H:%M:%S"
            )
            # create a file handler which config specific
            logHdl = logging.FileHandler(self.Config.logFile, encoding="UTF-8")
            logHdl.setFormatter(formatter)
            self.Log.addHandler(logHdl)
        
        # initial message
        self.Log.info("GiteaUpdator initialized")

    def CheckVersion(self) -> bool:
        """ check the version of local site and github. return (True)need update (False)unnecessary """

        # get local site version
        localVer : GiteaVersion
        if (self.Config.checkMode == CheckMode.API):
            # using header token to access. see gitea api guide for more info
            head = { "Authorization": f"token {self.Config.token}" }
            rsp = requests.get(
                self.Config.siteVersion,
                headers=head
            )
            # response like : { "version" : "1.16.8" }
            data = rsp.json()
            localVer = GiteaVersion(data["version"])
        else:
            # -v will report : Gitea version 1.17.0 built with GNU Make 4.1, go1.18.4 ...
            ver_str = os.popen("%s -v" % self.Config.exePath).read()
            localVer = GiteaVersion(ver_str.split(" ")[2])
        
        # get remote site version
        rsp = requests.get(self.Config.releaseUrl)
        data = rsp.json()
        remoteVer = GiteaVersion(data["tag_name"])

        # print info and check
        logStr = f"local version : {str(localVer)}, latest version : {str(remoteVer)}"
        self.Log.info(logStr)
        return localVer < remoteVer


