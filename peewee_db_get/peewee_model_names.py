#!/usr/bin/env python3

import peewee
import datetime

db = peewee.SqliteDatabase(
    "/home/gl/Projects/flask_multi_media_viewer/peewee_db_get/names.db"
)


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

    class Meta:
        database = db
        db_table = "filepaths"  # file name to path,no repeat


class CoverPath(peewee.Model):
    f_name = peewee.ForeignKeyField(Name, backref="coverpath")

    coverpath = peewee.CharField()

    class Meta:
        database = db
        db_table = "coverpaths"  # file name to path,no repeat


def init_db():

    Name.drop_table()
    Name.create_table()

    FilePath.drop_table()
    FilePath.create_table()

    CoverPath.drop_table()
    CoverPath.create_table()

    Tag.drop_table()
    Tag.create_table()

    tagname = Tag.names.get_through_model()
    tagname.create_table()
