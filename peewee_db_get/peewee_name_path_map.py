#!/usr/bin/python3

import os
import time
from pathlib import Path

import logging as log
import argparse

from peewee_model_names import CoverPath, Name, FilePath

log.basicConfig(level=log.DEBUG)


needupdate = True


videopath = Path("../upside")
coverpath = Path("../covers")


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

                tmp_path = FilePath(
                    filepath=item,
                    f_name=tmp_name,
                    ctime=time.strftime(
                        "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_ctime)
                    ),
                    mtime=time.strftime(
                        "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_mtime)
                    ),
                    atime=time.strftime(
                        "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_atime)
                    ),
                    size=item.stat().st_size,
                )
                tmp_path.save()

                tmp_coverpath = CoverPath(
                    coverpath=coverpath / (str(item.stem) + ".jpg"), f_name=tmp_name
                )
                tmp_coverpath.save()

                log.debug(("add", item.stem))

        except:
            continue


# data update
def update_name_path(rootPath):
    """record_name_path"""
    global filelist, cmdlist
    for item in rootPath.iterdir():
        try:
            if item.is_dir():
                update_name_path(item)

            elif item.is_file() and item.suffix in [".mp4", ".mkv"]:

                tmp_name, name_created = Name.get_or_create(name=item.stem)
                if name_created:
                    tmp_name.save()

                    tmp_path = FilePath(
                        filepath=item,
                        f_name=tmp_name,
                        ctime=time.strftime(
                            "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_ctime)
                        ),
                        mtime=time.strftime(
                            "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_mtime)
                        ),
                        atime=time.strftime(
                            "%Y-%m-%dT%H:%M:%S", time.localtime(item.stat().st_atime)
                        ),
                        size=item.stat().st_size,
                    )
                    tmp_path.save()

                    tmp_coverpath = CoverPath(
                        coverpath=coverpath / (str(item.stem) + ".jpg"), f_name=tmp_name
                    )
                    tmp_coverpath.save()

                    log.debug(("add", item.stem))
                else:
                    pass

        except:
            continue


def gen_data():
    """gen_data"""
    global videopath, coverpath
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


def update_data():
    """update_data"""
    global videopath, coverpath
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

    update_name_path(videopath)


# if __name__ == "__main__":
#     gen_data()
