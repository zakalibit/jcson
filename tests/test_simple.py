from __future__ import print_function

import os
import jcson

CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_simple_subst():
    m = jcson.read(os.path.join(CURDIR, 'simple.jcson'))
    assert m['services']['proxy']['port'] == 80
    assert m['services']['webapp']['port'] == 8080
    assert m['services']['webapp']['env']['debug'] == 1