# jcson - enhanced json for configuration

[![Build Status](https://travis-ci.org/zakalibit/jcson.svg?branch=master)](https://travis-ci.org/zakalibit/jcson)

## Introdcution
The jcson python module is an enhanced json parser, that supports:

* path expression sustitutions, a way of referring to other parts of the json/dictionary tree
* include directive
* new line and inline comments


## Instaling

Install and update using pip:

```
pip install -U jcson
```


## A simple example

Sample config file simple.jcson:

```
{
    "foo" : {
        "bar": "some value"
    },

    "bar_value": "${foo.bar}",

    "concatenated": "${foo.bar} used later"
}
```


Pyhton code that reads it:

```pyhton

import json
import jcson

c = jcson.read('simple.jcson')

print (json.dumps(c, indent=4))
```

Output:

```
{
    "foo" : {
        "bar": "some value"
    },

    "bar_value": "some value",

    "concatenated": "some value used later"
}
```
