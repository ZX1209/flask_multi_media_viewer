#!/usr/bin/env bash
python3 -m RangeHTTPServer &
cd ./fastapi
uvicorn main:app --reload --port 10001