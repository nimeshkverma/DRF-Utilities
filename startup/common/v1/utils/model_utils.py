def check_pk_existence(model, pk_value):
    is_valid_company = False
    if model.active_objects.filter(pk=pk_value):
        is_valid_company = True
    return is_valid_company
