#!/usr/bin/env python3

import peewee
import datetime
import json
from pathlib import Path
import os

file_path = Path(__file__).absolute()
file_dir_path = file_path.parent
original_working_path = Path("./").absolute()


db_path = file_dir_path / "names.db"
db_path.resolve()


db = peewee.SqliteDatabase(str(db_path))

tagDataFilePath = file_dir_path / "./tagdata.json"


class Name(peewee.Model):

    name = peewee.CharField()
    ctime = peewee.DateField(default=datetime.date.today)

    class Meta:
        database = db
        db_table = "names"  # file name to path,no repeat


class Tag(peewee.Model):
    tagname = peewee.CharField()
    names = peewee.ManyToManyField(Name, backref="tags")

    class Meta:
        database = db
        db_table = "tags"  # file name to path,no repeat


class FilePath(peewee.Model):
    f_name = peewee.ForeignKeyField(Name, backref="filepath")

    filepath = peewee.CharField()
    ctime = peewee.DateField()  # formats="%Y-%m-%dT%H:%M:%S"
    mtime = peewee.DateField()
    atime = peewee.DateField()
    size = peewee.IntegerField()

    class Meta:
        database = db
        db_table = "filepaths"  # file name to path,no repeat


class CoverPath(peewee.Model):
    f_name = peewee.ForeignKeyField(Name, backref="coverpath")

    coverpath = peewee.CharField()

    class Meta:
        database = db
        db_table = "coverpaths"  # file name to path,no repeat


def export_tag_data(filepath):
    tagsData = dict()
    for tag in Tag.select():
        tagsData[tag.tagname] = list(map(lambda n: n["name"], tag.names.dicts()))
    with open(filepath, "w") as fp:
        json.dump(tagsData, fp, skipkeys=True)


def import_tag_data(filepath):
    importData = None
    with open(filepath, "r") as fp:
        importData = json.load(fp)

    for tagname in importData:
        tmp_tag = Tag(tagname=tagname)
        tmp_tag.save()

        for name in importData[tagname]:
            try:
                tmp_n, _ = Name.get_or_create(name=name)
                tmp_tag.names.add(tmp_n)
            finally:
                pass

    print(importData)


tagname = Tag.names.get_through_model()


def init_db():
    export_tag_data(tagDataFilePath)

    Name.drop_table()
    Name.create_table()

    FilePath.drop_table()
    FilePath.create_table()

    CoverPath.drop_table()
    CoverPath.create_table()

    Tag.drop_table()
    Tag.create_table()

    tagname.drop_table()
    tagname.create_table()
