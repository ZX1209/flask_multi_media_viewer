#!/usr/bin/python3

import os
from pathlib import Path
import subprocess
import json
import time
import logging as log

log.basicConfig(level=log.INFO)

needupdate = True

filePath = Path(__file__)
# file_dir_path = filepath.parent

original_working_path = Path("./").absolute()

# working directory set
runPath = Path("/home/gl/Projects/Python/flask-http-file-server/flaskApp")
os.chdir(runPath)

upPath = Path("./static/upside/")

picOutBase = Path("./static/covers")

filelistPath = picOutBase / "filelist.json"
# cmdlistPath = picOutBase / "cmdlist.json"

filelist = []
cmdlist = []


# data gen
def gen_video_cover(rootPath):
    """gen_video_cover
    """
    global filelist, cmdlist
    for item in rootPath.iterdir():
        try:
            if item.is_dir():
                gen_video_cover(item)

            elif item.is_file() and item.suffix in [".mp4",".mkv"]:
                pic_file_path = picOutBase / (str(item.stem) + ".jpg")
                if pic_file_path.exists():  # todo: update all setting
                    pass
                else:
                    filelist.append(str(item))
                    cmdlist.append(
                        [
                            "ffmpeg",
                            "-ss",
                            "00:00:10.000",
                            "-y",
                            "-i",
                            str(item),
                            "-r",
                            "1",
                            "-vframes",
                            "1",
                            "-an",
                            "-vcodec",
                            "mjpeg",
                            str(picOutBase / (str(item.stem) + ".jpg")),
                        ]
                    )
        except:
            continue


# gen data
gen_video_cover(upPath)


processCount = 0

procs = []
for cmd in cmdlist:
    print(f"process {cmd}")
    procs.append(subprocess.Popen(cmd))

    ## for memory
    processCount += 1
    if processCount > 5:
        for p in procs:
            p.wait()

        # procs = []
        processCount = 0

for p in procs:
    p.wait()

log.info(filelist)


# for (dirpath, dirnames, filenames) in os.walk(upPath):
#     if item.suffix == ".mp4":
#         subprocess.call(
#             [
#                 "ffmpeg",
#                 "-y",
#                 "-i",
#                 item,
#                 "-ss",
#                 "00:00:05.000",
#                 "-vframes",
#                 "1",
#                 picOutBase / item.name,
#             ]
#         )
