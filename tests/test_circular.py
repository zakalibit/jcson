from __future__ import print_function

import os
import jcson
import pytest

CURDIR = os.path.abspath(os.path.dirname(__file__))

def test_circular():
    with pytest.raises(jcson.CircularReferenceError):
        jcson.read(os.path.join(CURDIR, 'circular.jcson'))