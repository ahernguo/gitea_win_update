This project refers to [CMiksche/gitea-auto-update](https://github.com/CMiksche/gitea-auto-update) to update [Gitea](https://gitea.io) with service on Windows.

# Using project

1. Ensure [7-Zip](https://www.7-zip.org/) is installed and add to `%path%`
    - this project will using 7-Zip to extract / compress file

        > You can use `7z --help` to check install status.

2. Ensure [Python3](https://www.python.org/downloads/) and `requests` are installed
    - 2.x are not supported

        > You can use `pip install requests` to add module after install python3

2. Make a configuration file (*.json)

    > see demo files in [demo_config](\demo_config)

    ```jsonc
    {
        "exe_path": "D:\\gitea\\gitea.exe",
        "service_name": "gitea",
        "log": "D:\\gitea\\update.log",
        "release_url": "https://api.github.com/repos/go-gitea/gitea/releases/latest",
        "check_mode": "site_api",
        "local_version": "https://127.0.0.1:3000/api/v1/version",
        "token": "abc123",
        "overwrite_mode": "backup",
        "backup_dir": "D:\\gitea\\backup"
    }
    ```

    - `exe_path` target .exe file to check and update
    - `service_name` the service name to start/stop
    - `log` (**OPTION**) the file to logging. Keep empty to disable logging.
    - `release_url` the GitHub API url that indicate latest release of Gitea
    - `check_mode` 
        - `cmd_call` use '**gitea.exe -v**' to check local version
        - `site_api` query local site API to check version
    - `local_version` local Gitea API url to check. (must exists when '**check_mode = site_api**')
    - `token` header token to acceess Gitea API. (must exists when '**check_mode = site_api**')
    - `overwrite_mode` how to update .exe
        - `overwrite` replace .exe directly
        - `backup` backup to .7z before update
    - `backup_dir` the directory to store backup 7z file. (must exists when '**overwrite_mode = backup**')

3. Start check and update

    ```bat
    cd /d D:\gitea_win_upd
    python update.py --config=myConfig.json
    ```

    > You can use Windows Scheduler to run it periodically.

4. Done