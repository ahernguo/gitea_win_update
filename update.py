from lib.config import UpdateConfig
from lib.updator import GiteaUpdator
from lib.version import GiteaVersion
from os.path import exists
import re
import sys

def main():
    """ Main entry """

    # check python version
    if (not sys.version_info[0] == 3):
        sys.exit("This repo only supports Python3")
    
    # check argv
    if (len(sys.argv) < 2):
        sys.exit("Must execute with a configuration file. For example `--config=mySetting.json`")

    if (not re.match(r'--config\=.+', sys.argv[1], re.IGNORECASE)):
        sys.exit("Invalid execution arguments. For example `--config=mySetting.json`")

    conf_file = re.search(r'(?<=--config=).*', sys.argv[1], re.IGNORECASE).group(0)

    if (not exists(conf_file)):
        sys.exit("Can not find the configuration \'%s\'" % conf_file)

    # load configuration and check values
    conf = UpdateConfig(conf_file)

    # initial updator
    upd = GiteaUpdator(conf)
    upd.CheckVersion()

if __name__ == '__main__':
    main()