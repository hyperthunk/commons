#!/usr/bin/env python

import sys
from itertools import repeat, izip, chain
from functools import wraps
from functional import flip
from operator import concat

if 'java' in sys.platform:
    # some things are not really a benefit when running on the jvm....
    # whilst the c-implementation of functional is very fast, the java bytecode isn't,
    # so we import the stdlib module instead which is fairly good nonetheless
    from functools import partial
    
    # jython is only up to python2.5 and zip_longest was added in 2.6
    # - this code was taken straight from the python stdlib documentation:
    # http://docs.python.org/library/itertools.html#itertools.izip_longest
    def izip_longest(*args, **kwds):
        """
        izip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
        
        Make an iterator that aggregates elements from each of the iterables.
        If the iterables are of uneven length, missing values are filled-in with fillvalue.
        Iteration continues until the longest iterable is exhausted.
        
        If one of the iterables is potentially infinite, then the izip_longest() function
        should be wrapped with something that limits the number of calls (for example
        itertools.islice() or itertools.takewhile()). If not specified, fillvalue defaults to None.
        """
        fillvalue = kwds.get('fillvalue')
        def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
            yield counter()         # yields the fillvalue, or raises IndexError
        fillers = repeat(fillvalue)
        iters = [chain(it, sentinel(), fillers) for it in args]
        try:
            for tup in izip(*iters):
                yield tup
        except IndexError:
            pass
else:
    from itertools import izip_longest
    from functional import partial

# just adding a new name (alias) for itertools.chain
# takes out None(s) from an iterable
compact = chain

def recursive_getattr(key, obj):
    """
    get attributes recursively, translating the dot '.' syntax into lookups 
    into the nested levels of objects within the graph of which `obj' is the entry point.
    """
    return reduce(lambda acc, attr: getattr(acc, attr), key.split('.'), obj)

def memoize(fn):
    """
    cache the results of calls to a referentially transparent function
    to avoid the overhead of excessive (for example, recursive) calls
    """
    cache = {}
    @wraps(fn)
    def wrap(*args, **kw):
        inputs = (args, tuple(kw.items()))
        if cache.has_key(inputs):
            return cache[inputs]
        result = fn(*args, **kw)
        cache[inputs] = result
        return result
    return wrap

# compose an arbitrary number of functions (n)
#compose_n = partial(reduce, compose)

def negate(fn):
    """ negate(fn) -> not bool(fn) """
    def wrap(*args, **kwargs):
        return not fn(*args, **kwargs)
    return wrap

def splitwith(f, xs):
    """
    splitwith(f, xs) -> (ys, zs)
    splits xs into elements for which the predicate `f' returns
    true (ys) and false (zs).
    """
    # TODO: rewrite this so it only performs one traversal
    return (filter(f, xs), filter(lambda x: not f(x), xs))

def safe_unzip(zs, group=0):
    """
    safely unzip a list of pairs and return one of the resulting lists
    """
    try:
        # zip is acting as a matrix transposition here...
        return (zip(*zs) or ([],))[group]
    except IndexError:
        return []

def compare(key, f, x, y):
    """
    compare(key, f, x, y) -> f(key(x), key(y))
    Compare key(x) with key(y) using f.
    """
    return f(key(x), key(y))
    # return f(*key(x,y))
    
def detect(f, x, xs, key=None):
    """
    detect(f, x, xs, key=None) -> y or None
    where f(x, y)   -> cmp(x, y)
          x = the search item to detect
          xs = the search base
          key(x) = key function for x

    A simple root finder that bisects xs until a match for x is found and returned or
    no match exists; returns `None' if x is not in xs. Uses `f' as a comparison
    function and key (if present) as a key function for both x and each element in xs
    """
    compfn = key and partial(compare, key, f) or f
    lo = 0
    hi = len(xs)
    # CCARE - added quick fix to break out if xs is empty
    if (hi == 0):
        return None
    mid = (lo + hi) // 2
    candidate = xs[mid]
    detected = compfn(candidate, x)
    if  hi > 1 and detected < 0:
        return detect(compfn, x, xs[mid:], key=None)
    elif hi > 1 and detected > 0:
        return detect(compfn, x, xs[:mid], key=None)
    elif detected == 0:
        return candidate
    else:
        return None
