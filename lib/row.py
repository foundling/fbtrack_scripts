from collections import namedtuple

'''
    This is a row object used to represent CSV data to be written to a csv file.
'''

def row_factory(headers=None, default_header_value='.'):

    if headers is None or not hasattr(headers, '__iter__'):
        raise ValueError('Make row requires a single iterable argument.')

    # these are the ordered named fields in our row where we can assign data
    Row = namedtuple('Row', headers)
    Row.__new__.__defaults__ = (default_header_value,) * len(Row._fields)

    return Row
