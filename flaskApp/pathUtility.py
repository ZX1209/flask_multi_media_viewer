#!/usr/bin/env python3

from pathlib import Path
import logging as log
import os


log.basicConfig(level=log.DEBUG)
log.debug("this is a demo massage")

basePath = Path("../")
os.chdir(basePath)

curPath = Path("./")
os.chdir((curPath.resolve() / "flaskApp"))
