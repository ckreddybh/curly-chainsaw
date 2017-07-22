#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os

delimiter = '_'
_id = ''


def write_file(p, data):
    filename = p+'.json'
    try:
        with open(filename) as json_data:
            d = json.load(json_data)
    except IOError:
        d = []
    with open(filename, 'w') as outfile:
        # print d
        d.append(data)
        json.dump(d, outfile)


def is_list_value_premitve(list_obj):

    for value in list_obj:
        if isinstance(value, dict):
            return False
        elif isinstance(value, list) or isinstance(value, set):
            return False
    return True


def make_key(parent_key, delimiter, key):
    if key.endswith('s'):
        key = key[:-1]
    if parent_key:
        return "{parent_key}{delimiter}{key}".format(
            parent_key=parent_key,
            delimiter=delimiter,
            key=key)
    else:
        return key


def flatten_file(json_obj, file_name, parent_index):
    data = {}
    for key, value in json_obj.items():
        if isinstance(value, dict):
            pass
        elif isinstance(value, list) or isinstance(value, set):
            if is_list_value_premitve(value):
                data[key] = value
        else:
            data[key] = value
    
    data["id"] = _id
    if parent_index:
        # import pdb;pdb.set_trace()
        data["__index"] = str(parent_index)
    write_file(file_name, data)


def flatten(d):
    global _id
    for x in d:
        key = x[:-1]
    cmd = 'rm -rf '+key+'_*'
    cmd2 = 'rm -rf '+key+'.*'
    os.system(cmd)
    os.system(cmd2)

    obj = d[x][0]
    _id = obj["id"]
    flatten_json(obj, key)


def _process(json_obj, index, parent_key):
    # import pdb;pdb.set_trace()
    if isinstance(json_obj, dict):
        json_obj["__index"] = str(index)
        data = {}
        for key, value in json_obj.items():
            if isinstance(value, dict):
                flatten_json(value, make_key(parent_key, delimiter, key), parent_index=index)
            elif isinstance(value, list) or isinstance(value, set):
                if is_list_value_premitve(value):
                    data[key] = value
            else:
                data[key] = value
        data["id"] = _id
        return data
    else:
        return None


def flatten_json(json_obj, key, parent_index=None):
    if isinstance(json_obj, dict):
        if isinstance(parent_index, int):
            parent_index = str(parent_index)
        flatten_file(json_obj, key, parent_index)
        for json_obj_key in json_obj:
            if key:
                flatten_json(json_obj[json_obj_key], make_key(key, delimiter, json_obj_key), parent_index)
    elif isinstance(json_obj, list) or isinstance(json_obj, set):
        list_obj = []
        for index, item in enumerate(json_obj):
            temp = _process(item, index, key)
            if temp:
                list_obj.append(temp)
        if list_obj:
            with open(key+'.json', 'w') as outfile:
                json.dump(list_obj, outfile)
            
if __name__ == '__main__':

    with open(sys.argv[1]) as json_data:
        d = json.load(json_data)
    # print(d)
    flatten(d)