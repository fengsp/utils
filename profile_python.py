# -*- coding: utf-8 -*-
"""
    Profile
    ~~~~~~~

    Profiling Python Like a Boss

    https://zapier.com/engineering/profiling-python-boss/
"""
import time
import cProfile


# Main decorator
def timefunc(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print f.__name__, 'took', end - start, 'seconds'
        return result
    return wrapper


#----------- Decorator Demo -----------#
def get_number():
    for x in xrange(5000000):
        yield x


def expensive_func():
    for x in get_number():
        i = x ^ x ^ x
    return 'result'


timefunc(expensive_func)()
#----------- Decorator Demo -----------#


# Main context manager
class timewith(object):
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        print '{timer} {checkpoint} took {elapsed} seconds'.format(
            timer=self.name,
            checkpoint=name,
            elapsed=self.elapsed,
        ).strip()
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass


with timewith('expensive func') as timer:
    expensive_func()
    timer.checkpoint('run one time')
    expensive_func()
    expensive_func()
    timer.checkpoint('run three times')


def do_cprofile(func):
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return wrapper


do_cprofile(expensive_func)()


try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return wrapper
        return decorator

except ImportError:
    def do_profile(follow=[]):
        "Helpful if you accidentally leave in production!"
        def decorator(func):
            return func
        return decorator


do_profile(follow=[get_number])(expensive_func)()
