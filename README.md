# jellyfin_library_poster

jellyfin/Emby 根据媒体库里面的海报(默认最新的 9 张,没有时间就随机)生成媒体库封面并且上传更新
不会 python 随便写的

理论上支持 Emby(已得到别人验证可以)

## 使用说明

### docker 运行

```bash
docker run \
  --name jellyfin-library-poster \
  -v "./config:/app/config" \
  -v "./poster:/app/poster" \
  -v "./output:/app/output" \
  evanqu/jellyfin-library-poster:latest
```

`/app/config` 存放 config.json

`/app/poster` 存放下载得海报

`/app/output` 存放生成的媒体库封面

### docker-compose 运行

`docker-compose.yml`文件

```yaml
services:
  jellyfin-library-poster:
    image: evanqu/jellyfin-library-poster:latest
    container_name: jellyfin-library-poster
    volumes:
      - ./config:/app/config
      - ./poster:/app/poster
      - ./output:/app/output
```

```
docker-compose down && docker-compose pull && docker-compose up -d
```

### 源码运行

```

pip install -r requirements.txt
python main.py

```

## config 配置说明

`config.json` 是项目的配置文件，用于设置 Jellyfin 服务器连接信息和媒体库海报生成的规则。

### 1. Jellyfin/Emby 服务器配置

```json
"jellyfin": {
  "base_url": "http://your-jellyfin/emby-server:port",  // Jellyfin/Emby 服务器地址
  "user_name": "your-username",                    // 登录用户名
  "password": "your-password",                     // 登录密码
  "update_poster": false                            // 是否自动更新海报
}
```

- "jellyfin"的节点不要改,就算你是`emby`的也是`jellyfin`

### 2. 排除更新的媒体库

```json
"exclude_Update_library": ["Short", "Playlists", "合集"]
```

此数组列出不需要自动更新海报的媒体库名称。

### 3. 媒体库模板映射

```json
"template_mapping": [
  {
    "library_name": "Movie",             // Jellyfin 中的媒体库名称
    "library_ch_name": "电影",            // 海报的中文名称（用于海报显示）
    "library_eng_name": "MOVIE"          // 海报的英文名称（用于海报显示）
  },
  // 更多媒体库配置...
]
```

系统会根据这些映射为每个媒体库创建包含相应名称的自定义海报。

### 4. 定时任务

```json
"cron": "0 1 * * *",
```

`cron` 字段用于设置自动更新海报的定时任务时间。其格式遵循标准的 Cron 表达式规则：

- `0 1 * * *` 表示每天凌晨 1 点执行任务。
- Cron 表达式的格式为：`分钟 小时 日 月 星期`。

如果需要修改定时任务时间，请根据需求调整 Cron 表达式。例如：

- 每天中午 12 点：`0 12 * * *`
- 每周一凌晨 2 点：`0 2 * * 1`

更多 Cron 表达式的用法可以参考相关文档。

### 完成配置

```json
{
  "jellyfin": {
    "base_url": "http://192.168.2.211:8096",
    "user_name": "username",
    "password": "password",
    "update_poster": false
  },
  "cron": "0 1 * * *",
  "exclude_update_library": ["Short", "Playlists", "合集"],
  "template_mapping": [
    {
      "library_name": "Anime",
      "library_ch_name": "动漫",
      "library_eng_name": "ANIME"
    },
    {
      "library_name": "Classic TV",
      "library_ch_name": "电视剧",
      "library_eng_name": "TV"
    },
    {
      "library_name": "Movie",
      "library_ch_name": "电影",
      "library_eng_name": "MOVIE"
    },
    {
      "library_name": "Documentary",
      "library_ch_name": "纪录片",
      "library_eng_name": "DOC"
    },
    {
      "library_name": "合集",
      "library_ch_name": "合集",
      "library_eng_name": "COLLECTIONS"
    },
    {
      "library_name": "Hot Movie",
      "library_ch_name": "正在热映",
      "library_eng_name": "HOT MOVIE"
    },
    {
      "library_name": "Hot TV",
      "library_ch_name": "正在热播",
      "library_eng_name": "HOT TV"
    },
    {
      "library_name": "Short",
      "library_ch_name": "短剧",
      "library_eng_name": "SHORT"
    },
    {
      "library_name": "TEST TV",
      "library_ch_name": "测试电视",
      "library_eng_name": "TEST TV"
    }
  ]
}
```

### 注意事项

1. 请确保 `base_url`、`user_name` 和 `password` 配置正确
2. `exclude_update_library` 中列出的媒体库将不会被自动更新海报

## 效果图

![](./screenshot/2.png)

![](./screenshot/1.png)

```

```
