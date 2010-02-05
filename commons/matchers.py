#!/usr/bin/env python

"""
 Provides a few simple custom hamcrest matchers.
 The 'matcher' function also supports the creation of matchers
 from a supplied function (e.g. based on a lambda function).
"""

from commons import flip 
from functional import partial, flip
#from functools import partial
from hamcrest import *
from hamcrest.core.core import *
from hamcrest.core.core.isnone import none, not_none
from hamcrest.core.base_matcher import *
from operator import gt
 
class DefunMatcher(BaseMatcher):
 
    def __init__(self, matcher, description=None):
        self.matcher = matcher
        self.description = description
 
    def matches(self, *args, **kwargs):
        return self.matcher(*args, **kwargs)
 
    def describe_to(self, description):
        description.append_text(self.description or repr(self))
 
def matcher(fun, desc=None):
    return DefunMatcher(fun, desc)
 
def kwmatch(**kwargs):
    """ creates a 'with' matcher for in value in 'kwargs' which is not already a BaseMatcher
    """
    args = kwargs
    for k in args.iterkeys():
        v = args[k]
        if not isinstance(v, BaseMatcher):
            args[k] = is_(v)    
    def match(**kw):
        for k,v in kw.items():
            if not args[k].matches(v):
                return False
        return True
    return matcher(match)

def local(fn, desc=None):
    m = matcher(fn, desc=desc)
    def match(**kwargs):
        return m.matches(**kwargs)
    return matcher(match)

def hasattribute(name):
    return matcher(lambda x: hasattr(x, name),
        "'%s' attribute to be present" % (name))
 
def is_true():
    return is_(equal_to(True))
 
def is_false():
    return is_not(is_true())

def nomatch(desc=None):
    return matcher(lambda _: False, desc)
 
def greater_than(n):
    return matcher(partial(flip(gt), n))

def match_subsequent_items(seq):
    """Creates an object that matches and removes the head item
    from 'seq' on each call. Be sure to pass a copy of 'seq' to this
    function if you're planning to keep a reference yourself!"""
    def reduce_match(input):
        if len(seq) == 0: return False
        return equal_to(seq.pop(0)).matches(input)
    return matcher(reduce_match,
        "expected the next item in the list %s, but was not")
 
any = instance_of

def checktype(t):
    return partial(flip(assert_that), instance_of(t))
