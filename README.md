# jcson - enhanced json for configuration

[![Build Status](https://travis-ci.org/zakalibit/jcson.svg?branch=master)](https://travis-ci.org/zakalibit/jcson)

## Introdcution
The jcson python module is an enhanced json parser, that supports:

* path expression subtitutions, with fallback to environment variables.
* include directive
* new line and inline comments


## Path expression sustitutions

Substitutions are a way of referring to other parts of the configuration tree.
The syntax is ${pathe.xpression} where the path.expression is used to write out a path through the object graph, like
${foo.bar} that refers to { "foo": { "bar" : 42 }
If a substitution is not present within a configuration tree, search will attempt to fallback to environment variables.


## Include directive

An include directive consists of the unquoted string include followed by quoted filename.

```
include "include.jcson"
```


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
