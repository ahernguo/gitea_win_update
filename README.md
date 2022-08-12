This project refers to [CMiksche/gitea-auto-update](https://github.com/CMiksche/gitea-auto-update) to update [Gitea](https://gitea.io) with service on Windows.

# Using project

1. Make a configuration file (*.json)

```jsonc
{
    "release_url": "https://api.github.com/repos/go-gitea/gitea/releases/latest" /* the url indicate latest release of Gitea */,
    "local_version": "https://127.0.0.1:80/api/v1/version" /* the version api of your site to check */,
    "exe_dir": "D:\\Gitea" /* the Gitea root directory */,
    "exe_name": "gitea" /* the filename without extension to replace */,
    "service_name": "gitea" /* the service name to start or stop Gitea */,
    "log": "D:\\gitea_win_upd\\update.log" /* the directory to save logs */
}
```

2. Start check and update

```bat
cd /d D:\gitea_win_upd
python3 update.py --config=myConfig.json
```

> You should check `Python3` is installed. Click [HERE](https://www.python.org/downloads/) to download and install.

3. Done