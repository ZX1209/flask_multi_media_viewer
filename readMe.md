## todo
- [x] 构建数据库
    - [x] name path map
    - [x] name coverpath map
    - [x] ffmpeg gen 
    - [x] file time record
- [x] 视频服务器
    - [x] RangeHTTPServer in ./
- [x] 数据生成
  - [x] 封面数据生成,相对截图
- [ ] 构建页面
- [x] 路径问题
  - [x] 工作目录,相对路径
- [x] 标签系统构建
  - [x] 数据结构
  - [x] 数据存储,更新,维护

## 文件组织结构
* ffmpeg_cover_get
  * ffmpeg-python-cover-get.py , 遍历视频文件,生成到对应文件夹
* peewee_db_get
  * init_db.py ,初始化 重构数据库
  * peewee_model_names.py , peewee 数据 模型
  * peewee_name_path_map.py , 数据对应生成
  * peewee_api_names.py , 对外 api
* flaskApp
* covers , 实际封面存储文件夹
* upside , 外部文件链接 
  

## tag 建立
import ,export
