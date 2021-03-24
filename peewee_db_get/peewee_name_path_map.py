#!/usr/bin/python3

import os
from pathlib import Path

import logging as log
import argparse

from peewee_model_names import CoverPath, Name, FilePath

log.basicConfig(level=log.INFO)


needupdate = True

videopath = Path("../upside/")
coverpath = Path("../flaskApp/covers")


filelist = []
cmdlist = []

# threads
tds = []


# data gen
def record_name_path(rootPath):
    """record_name_path"""
    global filelist, cmdlist
    for item in rootPath.iterdir():
        try:
            if item.is_dir():
                record_name_path(item)

            elif item.is_file() and item.suffix in [".mp4", ".mkv"]:
                tmp_name = Name(name=item.stem)
                tmp_name.save()

                tmp_path = FilePath(filepath=item, f_name=tmp_name)
                tmp_path.save()

                tmp_coverpath = CoverPath(
                    coverpath=coverpath / (str(item.stem) + ".jpg"), f_name=tmp_name
                )
                tmp_coverpath.save()

                log.info(("add", item.stem))

        except:
            continue


if __name__ == "__main__":
    # video path args
    # cover path
    parser = argparse.ArgumentParser()
    parser.add_argument("--videopath")
    parser.add_argument("--coverpath")
    args = parser.parse_args()

    # can use gen?
    if args.videopath:
        videopath = Path(args.videopath)

    if args.coverpath:
        coverpath = Path(args.coverpath)
    # gen data

    record_name_path(videopath)
