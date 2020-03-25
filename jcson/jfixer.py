# -*- coding: utf-8 -*-
import re

invalid_trailing_commas_re = re.compile(r',\s*[\],\}]')

def fix_invalid_trailing_commas(content):
    index = 0
    result = ""
    for m in invalid_trailing_commas_re.finditer(content):
        if index:
            result += content[index: m.start()]
        else:
            result = content[: m.start()]
        index = m.start() + 1

    if index:
        result += content[index:]
        result = fix_invalid_trailing_commas(result)

    return result or content 


missing_trailing_commas_re = re.compile(r'[\]\}\"\w]\s*\"\w+\"')

def fix_missing_trailing_commas(content):
    index = 0
    result = ""
    for m in missing_trailing_commas_re.finditer(content):
        if index:
            result += content[index:m.start()+1] + ','
        else:
            result += content[:m.start()+1] + ','
        index = m.start() + 1

    if index:
        result += content[index:]

    return result or content