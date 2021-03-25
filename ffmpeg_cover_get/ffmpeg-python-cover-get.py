#!/usr/bin/python3

import argparse

from pathlib import Path
import subprocess

import logging as log

log.basicConfig(level=log.INFO)


videopath = Path("../upside")
coverpath = Path("../covers")


filelist = []
cmdlist = []


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
                            str(coverpath / (str(item.stem) + ".jpg")),
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
        procs.append(subprocess.Popen(cmd, stdout=subprocess.PIPE))

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
