from __future__ import print_function

import os
import jcson

CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_simple_subst():
    m = jcson.read(os.path.join(CURDIR, 'simple.jcson'))
    assert m['services']['proxy']['port'] == 80
    assert m['services']['webapp']['port'] == 8080
    assert m['services']['webapp']['env']['debug'] == 1


config = """
{
    include "simple_include.jcson"

    "services": {
        "proxy": {
            "port": "${profile.ports.proxy}"
        },

        "webapp": {
            "port": "${profile.ports.webapp}",
            "env": "${profile.env}"
        }
    }
}
"""

def test_reads():
    m = jcson.reads(config, include_path = CURDIR)
    assert m['services']['proxy']['port'] == 80
    assert m['services']['webapp']['port'] == 8080
    assert m['services']['webapp']['env']['debug'] == 1



config_env = """
{
    "user": "${USER}"
}
"""

def test_env_susbst():
    user = os.environ['USER']
    m = jcson.reads(config_env, include_path = CURDIR)
    assert m['user'] == user
