#!/usr/bin/python3

import argparse

from pathlib import Path
import subprocess

import logging as log
from pathlib import Path
import os

file_path = Path(__file__).absolute()
file_dir_path = file_path.parent
original_working_path = Path("./").absolute()


log.basicConfig(level=log.INFO)


videopath = file_dir_path / Path("../upside")
coverpath = file_dir_path / Path("../covers")


filelist = []
cmdlist = []

need_regenerate = False


def get_video_seconds(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


# data gen
def gen_video_cover(rootPath):
    """gen_video_cover"""
    global filelist, cmdlist
    for item in rootPath.iterdir():
        try:
            if item.is_dir():
                gen_video_cover(item)

            elif item.is_file() and item.suffix in [".mp4", ".mkv", ".avi"]:
                pic_file_path = coverpath / (str(item.stem) + ".jpg")
                if (
                    not need_regenerate and pic_file_path.exists()
                ):  # todo: update all setting
                    pass
                else:
                    filelist.append(str(item))
                    cmdlist.append(
                        [
                            "ffmpeg",
                            "-ss",
                            str(get_video_seconds(item) * 0.6),
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
                            str(coverpath / (str(item.stem) + ".jpg")),
                            "-nostdin",
                        ]
                    )
        except:
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--videopath")
    parser.add_argument("--coverpath")
    args = parser.parse_args()

    if args.videopath:
        videopath = Path(args.videopath)

    if args.coverpath:
        coverpath = Path(args.coverpath)

    # gen data
    gen_video_cover(videopath)

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


# for (dirpath, dirnames, filenames) in os.walk(videopath):
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
#                 coverpath / item.name,
#             ]
#         )
