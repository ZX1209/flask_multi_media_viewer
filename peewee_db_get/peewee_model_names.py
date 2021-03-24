#!/usr/bin/env python3

import peewee
import datetime

db = peewee.SqliteDatabase("names.db")


class Name(peewee.Model):

    name = peewee.CharField()
    ctime = peewee.DateField(default=datetime.date.today)

    class Meta:
        database = db
        db_table = "names"  # file name to path,no repeat


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


if __name__ == "__main__":
    init_db()
