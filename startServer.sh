#!/usr/bin/env bash
python3 -m RangeHTTPServer &
cd ./flaskApp
python3  __init__.py