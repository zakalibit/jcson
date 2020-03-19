from __future__ import print_function

import jcson

def test_simple_subst():
    m = jcson.read('simple.jcson')
    assert m['services']['proxy']['port'] == 80
    assert m['services']['webapp']['port'] == 8080