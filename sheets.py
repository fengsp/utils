# -*- coding: utf-8 -*-
"""
    sheets
    ~~~~~~

    A CSV Framework

    :copyright: (c) 2013 by fsp.
    :license: BSD.
"""

import os
import csv
import datetime
from collections import OrderedDict


class Sheet(object):
    """
    The main class.
    """
    def __init__(self, row_cls, filepath, csvkwargs=None):
        """
        :param csvkwargs: the keyword arguments passed to csv builtin func
        """
        self.row_cls = row_cls
        self.filepath = filepath
        self.csvkwargs = csvkwargs
        self.status = None
        self.fileobj = None

    def set_status(self, status):
        """Set the current working status"""
        self.status = status
        if status == 'read':
            self.fileobj = open(self.filepath, 'rb')
            self.ioer = Reader(self.row_cls, self.fileobj, self.csvkwargs)
        elif status == 'write':
            self.fileobj = open(self.filepath, 'wb')
            self.ioer = Writer(self.row_cls, self.fileobj, self.csvkwargs)
        elif status == 'append':
            self.fileobj = open(self.filepath, 'ab')
            self.ioer = Writer(self.row_cls, self.fileobj, self.csvkwargs)

    def read(self):
        self.set_status('read')
        return self.ioer

    def write(self, rows):
        self.set_status('write')
        if self.csvkwargs:
            writer = csv.writer(self.fileobj, **csvkwargs)
        else:
            writer = csv.writer(self.fileobj)
        titles = [column.title for column in self.row_cls._columns]
        writer.writerow(titles)
        self.ioer.writerows(rows)
        self.close()

    def append(self, rows):
        self.set_status('append')
        self.ioer.writerows(rows)
        self.close()

    def close(self):
        if self.fileobj: self.fileobj.close()


class Reader(object):
    """
    Itertor for CSV Reading
    """
    def __init__(self, row_cls, fileobj, csvkwargs):
        self.row_cls = row_cls
        if csvkwargs:
            self.reader = csv.reader(fileobj, **csvkwargs)
        else:
            self.reader = csv.reader(fileobj)
        self.reader.next()

    def __iter__(self):
        return self

    def next(self):
        return self.row_cls(*self.reader.next())


class Writer(object):
    """
    CSV Write Logic
    """
    def __init__(self, row_cls, fileobj, csvkwargs):
        self.row_cls = row_cls
        if csvkwargs:
            self.writer = csv.writer(fileobj, **csvkwargs)
        else:
            self.writer = csv.writer(fileobj)
    
    def writerow(self, row):
        values = [getattr(row, column.name) for column in \
            self.row_cls._columns]
        self.writer.writerow(values)

    def writerows(self, rows):
        try:
            iterator = iter(rows)
        except TypeError:
            self.writerow(rows)
        else:
            for row in rows:
                self.writerow(row)

class Column(object):
    """
    The base class for one individual column within a CSV file.
    """
    
    _column_counter = 0
    
    def __init__(self, title=None):
        self._column_counter = Column._column_counter
        Column._column_counter += 1
        self.title = title

    def attach(self, row_cls, name):
        self.row_cls = row_cls
        self.name = name
        if self.title is None:
            self.title = name

    def to_python(self, value):
        return value

    def to_string(self, value):
        return value

    def validate(self, value):
        pass
        
    
class RowMeta(type):
    """
    The row metaclass
    """
    def __init__(cls, name, bases, attrs):
        columns = [(key, attr) for key, attr in attrs.items() if isinstance(attr, Column)]
        columns = sorted(columns, key=lambda t: t[1]._column_counter)
        for key, attr in columns:
            attr.attach(cls, key)
        columns = [attr for key, attr in columns]
        cls._columns = columns

    # Just works in Python 3.x
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()


class Row(object):
    """
    The row class
    """

    __metaclass__ = RowMeta

    def __init__(self, *args, **kwargs):
        column_names = [column.name for column in self._columns]
        for i, name in enumerate(column_names[:len(args)]):
            kwargs[name] = args[i]
        for column in self._columns:
            value = column.to_python(kwargs[column.name])
            setattr(self, column.name, value)


class StringColumn(Column):
    pass


class IntegerColumn(Column):
    def to_python(self, value):
        return int(value)


class FloatColumn(Column):
    def to_python(self, value):
        return float(value)


class DateColumn(Column):
    
    def __init__(self, *args, **kwargs):
        format = kwargs.pop('format', '%Y-%m-%d')
        super(DateColumn, self).__init__(*args, **kwargs)
        self.format = format
    
    def to_python(self, value):
        if isinstance(value, datetime.date):
            return value.date()
        return datetime.datetime.strptime(value, self.format).date()

    def to_string(self, value):
        return value.strftime(self.format)


if __name__ == '__main__':
    class Person(Row):
        name = StringColumn()
        age = IntegerColumn(title='年龄')
        birthday = DateColumn()


    filepath = './sheets.csv'
    csvkwargs = {'delimiter':':'}


    person = Person('冯巩', 22, '1991-06-23')
    persons = []
    persons.append(Person('fsp2', 23, datetime.datetime.now()))
    persons.append(Person('fsp:3', 24, '1991-06-23'))
    persons.append(Person('fsp4', 25, '1991-06-23'))


    sheet = Sheet(Person, filepath, csvkwargs)
    sheet.write(person)
    sheet.write(persons)
    sheet.append(persons)
    sheet.append(person)


    for p in sheet.read():
        print (p, p.name, p.age, p.birthday)
    sheet.close()

