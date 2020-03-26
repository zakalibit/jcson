# -*- coding: utf-8 -*-

__version__ = '0.1.4'
__all__ = ['read']

__author__ = 'Alex Revetchi <alex.revetchi@gmail.com>'

import os
import io
import re
import sys
import copy
import json
from jcson import jpath
from jcson import jfixer
from collections import  defaultdict, OrderedDict

if sys.version_info[0] >= 3:
    __str_types__ = (str, bytes)
else:
    __str_types__ = (str, unicode)


class CircularReferenceError(Exception):
    pass


def strip_comments(content_in):
    content_out = ''
    for l in content_in.splitlines(True):
        ## skip empty lines & strip comments
        l = l.lstrip()
        if not l or l.startswith('#'):
            content_out +='\n'  ## make error reporting match original file line numbering
        else:
            p = l.find('#')
            if p > -1: l = l[:p] + '\n'
            content_out += l
    return content_out


re_include = re.compile(r'(#*\s*include\s+\"([\/\w\.]+\w+)\")')


def validate_jcontent(fcontent):
    """
        Validates json content ignoring include directives
    """
    includes = re_include.finditer(fcontent)
    
    last_end = 0
    content = ''
    for inc in includes:
        content += fcontent[last_end:inc.start()]
        last_end = inc.end()
    if last_end:
        fcontent = content + fcontent[last_end:]
    json.loads(fcontent)


def file_content(filename):
    with io.open(filename, 'rt', encoding='utf8') as f:
        content = f.read()
        content = strip_comments(content)
        validate_jcontent(content)
        return content
        
    
def process_includes(filename):
    path = os.path.dirname(os.path.abspath(filename))

    fcontent = file_content(filename)
    includes = [i for i in re_include.finditer(fcontent)]

    while len(includes):
        last_end = 0
        content = ''
        for inc in includes:
            icontent = file_content(os.path.join(path, inc.group(2)))
            content += fcontent[last_end:inc.start()] + icontent.strip().strip('{}')
            last_end = inc.end()

        content += fcontent[last_end:]
        content = jfixer.fix_missing_trailing_commas(content)

        includes = [i for i in re_include.finditer(content)]
        fcontent = content
        
    return fcontent


def load_content(filename):
    return process_includes(filename)


# ${var.name} substitution with in the file or env
re_var = re.compile(r'\${(?P<mvar>[\w\._-]+)}')

def parse_substitutions(path, node):
    if not isinstance(node, __str_types__): return

    res = re_var.findall(node)
    spath = '.'.join(path)
    for m in res:
        if m == spath:
            raise CircularReferenceError('Circular reference detected for: {}'.format(m))
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
            for depth, s in  parse_substitutions(path, node):
                substitutions[depth].append(s)

        if not len(substitutions): break

        for _, subs in substitutions.items():
            for s in subs:
                v = resolve_substitution_value(config, s['var'], s['path'])
                expand_node_substitution(config, s['var'], s['path'], v)

    return config
