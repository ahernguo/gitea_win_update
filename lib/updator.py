import logging, os, re, requests, sys, tempfile, time
from .config import CheckMode, OverwriteMode, UpdateConfig
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
        
        # setting 'requests' log to warning. for less log
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # initial message
        self.Log.info("GiteaUpdator initialized")

    def CheckLocalVersion(self) -> GiteaVersion:
        """ check the version of local site """
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

        return localVer

    def CheckGithubVersion(self) -> tuple[GiteaVersion, str]:
        """ check the github release page and return version and its download url """

        rsp = requests.get(self.Config.releaseUrl)
        data = rsp.json()
        ver = GiteaVersion(data["tag_name"])
        tar_name = f"gitea-{ver.Major}.{ver.Minor}.{ver.Build}-windows-4.0-amd64.exe.xz"
        url = list(filter(lambda x:x["name"]==tar_name, data["assets"]))[0]["browser_download_url"]
        return (ver, url)

    def StartUpdate(self) -> None:
        """ start to update. download → stop service → start service """
    
        # write log
        self.Log.info(f"Starting to update gitea. Config file : '{self.Config.configPath}'")

        # check local version
        localVer = self.CheckLocalVersion()
        githubVer, download_url = self.CheckGithubVersion()
        self.Log.info(f"    Local version : {str(localVer)}, GitHub Version : {str(githubVer)}")

        # compare version
        if (localVer >= githubVer):
            self.Log.info("Unnecessary to update. exit program")
            return
    
        # for a shorter suspension of gitea service. download first
        # make a tempfile for download
        temp_file = tempfile.NamedTemporaryFile(suffix=".xz").name

        # download file to temp file
        self.Log.info(f"    Download new file '{download_url}' to '{temp_file}' ...")
        with open(temp_file, "wb") as fs:
            rsp = requests.get(download_url)
            fs.write(rsp.content)

        # stop the service. 1062 error is "Service not started"
        self.Log.info("  Stopping service ...")
        os.popen(f"sc stop {self.Config.serviceName}").read()
        
        # wait service stopped.
        qryChk : re.Match[str] | None = None
        tmo = time.time() + 10 # now add 10s 
        while (not qryChk and time.time() < tmo):
            qryOut = os.popen(f"sc query {self.Config.serviceName}").read()
            qryChk = re.search(r"(stopped|1062)", qryOut, re.IGNORECASE)
            time.sleep(0.25)

        if (not qryChk or time.time() > tmo):
            raise Exception(f"Stopping service '{self.Config.serviceName}' failed")

        # backup if overwrite mode specified
        if (self.Config.overwriteMode == OverwriteMode.BACKUP):
            # ensure directory first. copy next.
            if (not os.path.exists(self.Config.backupDir)):
                os.makedirs(self.Config.backupDir)
            # make the backup path
            backup_path = os.path.join(
                self.Config.backupDir,
                f"gitea_backup_{time.strftime('%Y%m%d_%H%M%S')}.7z"
            )
            # using 7z to backup
            self.Log.info(f"    Backup to '{backup_path}' ...")
            os.popen(f"7z a -t7z \"{backup_path}\" -m0=lzma2 -mx=9 -aoa \"{self.Config.exePath}\"").read()
            
        # delete file (avoid 7z error)
        if (os.path.exists(self.Config.exePath)):
            self.Log.info("    Deleting old file ...")
            os.remove(self.Config.exePath)

        # extract file and put to exePath
        self.Log.info("    Extracting new file ...")
        os.popen(f"7z e \"{temp_file}\" -so > \"{self.Config.exePath}\"").read()

        # start service
        self.Log.info("    Starting service ...")
        startOut = os.popen(f"sc start {self.Config.serviceName}").read()
        startChk = re.search(r"(start_pending|running)", startOut, re.IGNORECASE)
        if (not startChk):
            raise Exception(f"Starting service '{self.Config.serviceName}' failed")

        # clean temp file
        self.Log.info(f"    Cleaning temp file '{temp_file}' ...")
        os.remove(temp_file)

        # done
        self.Log.info(f"Done.")

