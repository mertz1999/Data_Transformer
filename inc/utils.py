def data_type_is_valid(type: str, DATA_TYPES_VALID):
    if type.startswith("STRING"):
        return True
    if type in DATA_TYPES_VALID:
        return True
    return False