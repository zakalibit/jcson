# -*- coding: utf-8 -*-

__version__ = '0.1.1'
__all__ = ['read']

__author__ = 'Alex Revetchi <alex.revetchi@gmail.com>'

import os
import io
import re
import sys
import copy
import json
from jcson import jpath
from collections import  defaultdict, OrderedDict

if sys.version_info[0] >= 3:
    __str_types__ = (str, bytes)
else:
    __str_types__ = (str, unicode)

def strip_comments(content_in):
    content_out = ''
    for l in content_in.splitlines(True):
        ## skip empty lines & strip comments
        l = l.strip()
        if not l or l.startswith('#'):
            content_out +='\n'  ## make error reporting match original file line numbering
        else:
            p = l.find('#')
            if p > -1: l = l[:p] + '\n'
            content_out += l
    return content_out


def file_content(filename):
    with io.open(filename, 'rt', encoding='utf8') as f:
        content = f.read()
        return strip_comments(content)


re_include = re.compile(r'(#*\s*include\s+\"([\/\w\.]+\w+)\")')

def process_includes(filename):
    content = file_content(filename)
    incfiles = re_include.findall(content)

    while incfiles:
        for include, ifile in incfiles:
            icontent = file_content(ifile)
            content = content.replace(include, icontent)
        incfiles = re_include.findall(content)
    return content


def load_content(filename):
    return process_includes(filename)


# ${var.name} substitution with in the file or env
re_var = re.compile(r'\${(?P<mvar>[\w\._-]+)}')

def parse_substitutions(path, node):
    if not isinstance(node, __str_types__): return

    res = re_var.findall(node)
    for m in res:
        depth = len(m.split('.'))
        yield depth, {'path': path, 'var': m}


def resolve_substitution_value(config, subst, path):
    v = jpath.find(config, subst)

    if v is None:
        if subst in os.environ:
            v = os.environ[subst]
        elif subst.upper() in os.environ:
            v = os.environ[subst.upper()]

    if v is None:
        raise Exception('{} cound not be resolved.'.format(subst))
    return v


def expand_node_substitution(config, subst, path, value):
    p = path[0]

    if len(path) > 1:
        expand_node_substitution(config[p], subst, path[1:], value)
    else:
        var = '${'+subst+'}'
        if config[p] == var:
            config[p] = copy.deepcopy(value)
        else:
            config[p] = config[p].replace(var, str(value))


def read(filename):
    content = load_content(filename)
    config = json.loads(content, object_pairs_hook=OrderedDict)

    while re_var.findall(json.dumps(config)):
        substitutions = defaultdict(list)

        ## collect all stubstitutions sorted by depth
        for path, node in jpath.traverse(config):
            for depth, subst in  parse_substitutions(path, node):
                substitutions[depth].append(subst)

        if not len(substitutions): break

        for _, subs in substitutions.items():
            for s in subs:
                v = resolve_substitution_value(config, s['var'], s['path'])
                expand_node_substitution(config, s['var'], s['path'], v)

    return config
