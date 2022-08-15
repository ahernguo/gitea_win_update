This project refers to [CMiksche/gitea-auto-update](https://github.com/CMiksche/gitea-auto-update) to update [Gitea](https://gitea.io) with service on Windows.

# Using project

1. Ensure [7-Zip](https://www.7-zip.org/) is installed and add to `%path%`
    - this project will using 7-Zip to extract / compress file

> You can use `7z --help` to check install status.

2. Make a configuration file (*.json)

```jsonc
{
    "release_url": "https://api.github.com/repos/go-gitea/gitea/releases/latest" /* the url indicate latest release of Gitea */,
    "check_mode": "site_api" /* 'cmd_call' use `.exe -v` to check local version; 'site_api' query currently gitea site api */,
    "local_version": "https://127.0.0.1:80/api/v1/version" /* the version api of your site to check. (need check_mode = site_api) */,
    "token": "abc123" /* the header token to access gitea api. (need check_mode = site_api) */,
    "exe_path": "gitea" /* the filename without extension to replace */,
    "service_name": "gitea" /* the service name to start or stop Gitea */,
    "log": "D:\\gitea_win_upd\\update.log" /* the directory to save logs */
}
```

3. Start check and update

```bat
cd /d D:\gitea_win_upd
python3 update.py --config=myConfig.json
```

> You should check `Python3` is installed. Click [HERE](https://www.python.org/downloads/) to download and install.

4. Done