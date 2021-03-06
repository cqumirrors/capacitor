# APIs

## Schema
1. 数据格式统一使用 JSON
2. HTTP methods:
    - `GET` to get resources without access_token
    - `POST` to create resources with access_token
    - `PUT` to update specified resources with access_token
    - `DELETE` to delete specified resources with access_token
3. 时间格式为 ISO 8601(YYYY-MM-DDTHH:MM:SSz): e.g. 2008-01-14T04:33:35Z
4. status code 作为返回值（给程序用的），并附上返回信息（给人看的）

 ```json
 {
     "status": "Bad Request",
     "message": "Problems parsing JSON"
 }
 ```

5. JSON 数组会封装在一个 JSON 对象里

 ```json
 {
     "count": 10,
     "targets": []
 }
 ```


## 获取镜像列表

```
GET    /api/mirrors
```

列表中的对象：

```
{
      "is_muted": false,
      "has_comment": false,
      "has_help": true,         // boolean ended
      "comment": "",
      "muted_at": null,
      "sync_status": null,
      "created_at": null,
      "help_url": "https://mirrors.cqu.edu.cn/wiki/index.php?title=CentOS",
      "url": "https://b.mirrors.lanunion.org/centos",
      "cname": "centos",
      "upstream_url": null,
      "full_name": "CentOS",
      "synced_at": null,
      "size": null
}
```

参数说明：

|参数          |意义           |备注               |
|-------------|---------------|-----------------|
|cname        |全局 ID        |应仅包含 [a-z] 和 -|
|full_name    |官方名称        |参见镜像官方声明   |
|url          |镜像链接        |                 |
|help_url     |镜像使用帮助链接 |现链接到相应wiki页 |
|comment      |备注           |                  |
|synced_at    |最后同步时间    |                  |
|size         |镜像大小        |                 |
|sync_status  |镜像更新状态    |具体代码含义参加下表|
|upstream_url |用于更新该镜像的上游 url|           |
|muted_at     |镜像冻结时间    |                  |
|created_at   |镜像创建时间    |                  |

`sync_status` 状态说明：

|code | status |
|-----|--------|
|100  |Syncing |
|200  |Success |
|300  |Freeze  |
|400  |Failed  |
|500  |Unknown |



## 获取镜像站公告

```
GET    /api/notices
```

返回列表中的对象：

```
{
    "is_muted": false,
    "id": 1,
    "created_at": "2015-1-1 11:11:11",
    "muted_at": null,
    "github_issue_url": null
}
```
