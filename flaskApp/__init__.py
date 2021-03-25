import sys

sys.path.insert(0, "../peewee_db_get/")

from flask import (
    Flask,
    current_app,
    g,
    session,
    request,
    render_template,
    jsonify,
    send_file,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

# from pathUtility import basePath, curPath
from pathlib import Path

from get_local_addr import get_lan_ip
from peewee_api_names import NameApi_1


api = NameApi_1()

host = "localhost"
port = 6379

# # redis 取出的结果默认是字节，我们可以设定 decode_responses=True 改成字符串。
# redis = StrictRedis(host=host, port=port, decode_responses=True)


img_base_url = "/static/covers2"


def isVideoFile(self):
    return self.suffix == ".mp4"


Path.isVideoFile = isVideoFile


curPath = Path("./")
basePath = Path("../")

import logging as log

log.basicConfig(level=log.INFO)
log.debug("this is a demo massage")

app = Flask(__name__)
# app.config["USE_X_SENDFILE"] = True


def sortedFileList(dirPath):
    """"just sort the dir or file order"""

    sortedList = []

    for path in dirPath.glob("*"):
        if path.is_dir():
            sortedList.insert(0, path)
        else:
            sortedList.append(path)

    if str(dirPath) != ".":
        sortedList.insert(0, dirPath / "../")

    log.debug(sortedList)

    return sortedList


@app.route("/")
def homepage():
    return redirect(url_for("all_video_view"))


@app.route("/all_video_view")
def all_video_view():
    end = 500
    videoItems = api.get_items()

    return render_template(
        "name_view.html", videoItems=videoItems, img_base_url="/static/covers"
    )


# 以页面形式展示
@app.route("/page_view/")
@app.route("/page_view/<int:page>")
def page_view(page=1):
    page_len = 12

    start = page_len * (page - 1)
    end = page_len * (page) - 1

    log.debug((start, end))

    videoItems = api.get_items(start, end)

    return render_template(
        "pages_view.html",
        videoItems=videoItems,
        img_base_url="/static/covers",
        cur_page=page,
    )


@app.route("/resources/", defaults={"var": ""})
@app.route("/resources/<path:var>")
def getRes(var):
    intoPath = curPath / var
    if intoPath.exists():
        if intoPath.is_file():
            if intoPath.suffix == ".mp4":
                filename = intoPath.resolve()
                return send_file(filename, attachment_filename=filename, conditional=True)

            return send_file(intoPath.resolve())
        else:
            return "not a file"

    return "no suce file"


# tag: tags
@app.route("/api/v1/add_tag")
def add_tag(name=None, tag=None):
    if name is None:
        name = request.args["name"]
    if tag is None:
        tag = request.args["tag"]

    redis.sadd("tags", tag)
    redis.rpush(tag + "_names", name)

    return 1


@app.route("/api/v1/name_tags")
def name_tags(name=None):
    if name is None:
        name = request.args["name"]

    tmp_tags = redis.smembers(name + "_tags")

    return jsonify(tmp_tags)


@app.route("/api/v1/tag_names")
def tag_names(tag=None):
    if tag is None:
        tag = request.args["tag"]

    tmp_names = redis.lrange(tag + "_names", 0, -1)

    return jsonify(tmp_names)


if __name__ == "__main__":
    print(get_lan_ip())
    app.run(debug=True, host="0.0.0.0", port=5001)
