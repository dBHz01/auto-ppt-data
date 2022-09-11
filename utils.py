def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

def remove_all(array, a):
    while a in array:
        array.remove(a)
    return array

def down(lst):
    out = []
    for obj in lst:
        if isinstance(obj, list):
            out += obj
    if len(out) == 0:
        return lst
    else:
        return out