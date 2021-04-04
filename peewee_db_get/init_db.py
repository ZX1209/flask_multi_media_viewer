from peewee_model_names import init_db, import_tag_data, tagDataFilePath

from peewee_name_path_map import gen_data


if __name__ == "__main__":
    init_db()
    gen_data()
    import_tag_data(tagDataFilePath)
