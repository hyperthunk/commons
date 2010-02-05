#!/usr/bin/env python

from contextlib import contextmanager

# resource management

def resourcemanager(acquire, release):
    """
    Create a resource management function wrapped by contextlib.contextmanager.
    The supplied functions are used in the appropriate lifecycle phases. Example:
    
    class Disposable(object):
        def __init__(self, other)
            self.other = other
        # .... some more code
        
        def dispose(self):
            pass
    
    disposable = resourcemanager(lambda x: Disposable(x), lambda x: x.dispose())
    
    with disposable(blah) as obj:
        # .....
    # ....
    """
    @contextmanager
    def manager(*args):
        resource = acquire(*args)
        try:
            yield resource
        finally:
            release(resource)
    return manager
