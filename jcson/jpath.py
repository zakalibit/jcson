# -*- coding: utf-8 -*-

def traverse(dictionary, path=[]):
    if isinstance(dictionary, dict):
        iterator = dictionary.items()
    else:
        iterator = enumerate(dictionary)
    for k, v in iterator:
        yield path + [k], v
        if isinstance(v, (dict, list)):
            for k, v in traverse(v, path+[k]):
                yield k, v


## dictionary value lookup, using key, or a path through the object graph
def find(dictionary, key):
    key_path = key.split('.')
    key_name = key_path[-1]
    key_path = key_path[:-1]

    ## grab a value on the topmost level if exists
    value = None
    if key_name in dictionary:
        value = dictionary[key_name]

    ## scan dict tree for best match
    current_node = dictionary
    for p in key_path:
        if p in current_node:
            ## check if key value exists at current level
            if key_name in current_node[p]:
                value = current_node[p][key_name]
            if isinstance(current_node[p], dict):
                current_node = current_node[p]
            else: break
        else: break

    return value
