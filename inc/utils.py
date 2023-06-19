def data_type_is_valid(type: str, DATA_TYPES_VALID):
    if type.startswith("STRING"):
        return True
    if type in DATA_TYPES_VALID:
        return True
    return False

rename_default_excel = {"Identifier": "identifier","Symbol/Tag - DE": "label_de","Symbol/Tag - EN": "label_en",
                    "Source":"source","Address":"address","BitOffset":"bitOffset","DB_Nr":"dataBlockNumber",
                    "D_Type":"dataType","Comment":"comment","Label":"label_new","Labels EN":"label_new_en","Selected":"selected", "Comment EN":"comment_en"
                    }
