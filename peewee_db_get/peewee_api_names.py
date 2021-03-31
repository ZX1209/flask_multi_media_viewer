from peewee_model_names import Name, FilePath, CoverPath, Tag


def peewee_model_to_dict_string(class_variable):
    """"""
    return {
        key: str(value)
        for key, value in class_variable.__dict__["__data__"].items()
        if not key.startswith("__") and not callable(key)
    }


class NameApi_1:
    def __init__(self):
        """__init__"""
        self.nameCount = Name.select().count()

    def count_names(self):
        self.nameCount = Name.select().count()
        return self.nameCount

    def set_name_tag(self, name_id, tag_name):
        tmp_tag, _ = Tag.get_or_create(tagname="tag")
        tmp_tag.save()

        tmp_tag.names.add(Name.get(Name.id == name_id))

        return 1

    def name2tags(self, name_id):
        tmp_name = Name.get(Name.id == name_id)
        return list(tmp_name.tags.dicts())

    def tag2names(self, tag_id):
        tmp_tag = Tag.get(Tag.id == tag_id)
        return list(tmp_tag.names.dicts())

    def get_items(self, start=1, end=None):
        # dont do so much check now
        # end set
        if end is None:
            end = self.nameCount
        elif end > self.nameCount:
            end = self.nameCount

        return list(
            Name.select(Name, FilePath, CoverPath)
            .join_from(Name, FilePath)
            .join_from(Name, CoverPath)
            .where((Name.id >= start) & (Name.id <= end))
            .order_by(FilePath.ctime.desc())
            .dicts()
        )

    def get_all_name(self):
        return [peewee_model_to_dict_string(i) for i in Name.select(Name.name)]

    def get_cover_path_by_name(self, name):
        tmp_name = Name.select().where(Name.name == name).get()

        tmp_cover = tmp_name.cover.get()

        return [peewee_model_to_dict_string(tmp_cover)]

    def get_file_path_by_name(self, name):
        tmp_name = Name.select().where(Name.name == name).get()

        tmp_file = tmp_name.filepath.get()

        return [peewee_model_to_dict_string(tmp_cover)]

    def inspect_test(self, one, two, three):
        pass


if __name__ == "__main__":
    test = NameApi_1()
