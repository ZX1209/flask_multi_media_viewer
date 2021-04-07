#!/usr/bin/env bash

cd ./peewee_db_get
python3 update_db.py
cd ..

cd ./ffmpeg_cover_get
python3 ./ffmpeg-python-cover-get.py
cd ..