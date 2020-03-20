jcson - enhanced json for configuration
========================================

Introdcution
------------
The jcson python module is an enhanced json parser, that supports:

* path expression sustitutions, a way of referring to other parts of the json/dictionary tree
* include directive
* new line and inline comments


Path expressions
----------------

Path expressions are used to represent a path through the object graph ${foo.bar}, that are syntactically identical to a value concatenation, except that they may not contain substitutions. This means that you can't nest substitutions inside other substitutions, and you can't have substitutions in keys.

    {
        "foo" : {
            "bar": "some value"
        },

        "bar_value": "${foo.bar}",

        "concatenated": "${foo.bar} used later"
    }

Note that path expression is in quotes, as it needs to be a valid json string, when parsed will produce the following:

    {
        "foo" : {
            "bar": "some value"
        },

        "bar_value": "some value",

        "concatenated": "some value used later"
    }

Path expressions that point to complex types like array, dictionary, when parsed will expand expression key in to a respective complex type:

    {
        "foo" : {
            "bar": "some value"
        },

        "foo2": "${foo}"
    }

will produce:

    {
        "foo" : {
            "bar": "some value"
        },

        "foo2": {
            "bar": "some value"
        }
    }
