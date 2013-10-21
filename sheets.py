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
    def __init__(self, row_cls, filepath):
        self.row_cls = row_cls
        self.filepath = filepath

    def read(self):
        file = open(self.filepath, 'rb')
        return Reader(self.row_cls, file)

    def write(self, rows):
        need_header = False
        if os.path.exists(self.filepath):
            need_header = True
        with open(self.filepath, 'wb') as f:
            writer = csv.writer(f)
            if need_header:
                titles = [column.title for column in self.row_cls._columns]
                writer.writerow(titles)
            try:
                iterator = iter(rows)
            except TypeError:
                values = [getattr(rows, column.name) for column in \
                    self.row_cls._columns]
                writer.writerow(values)
            else:
                for row in rows:
                    values = [getattr(row, column.name) for column in \
                        self.row_cls._columns]
                    writer.writerow(values)

    def append(self):
        pass


class Reader(object):
    """
    Itertor for CSV Reading
    """
    def __init__(self, row_cls, file):
        self.row_cls = row_cls
        self.file = file
        self.reader = csv.reader(self.file)
        self.reader.next()

    def __iter__(self):
        return self

    def next(self):
        return self.row_cls(*self.reader.next())


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
        age = IntegerColumn(title='agetitle')
        birthday = DateColumn()


    filepath = './sheets.csv'


    sheet = Sheet(Person, filepath)
    person = Person('fsp', 22, '1991-06-23')
    persons = []
    persons.append(Person('fsp2', 23, datetime.datetime.now()))
    persons.append(Person('fsp3', 24, '1991-06-23'))
    persons.append(Person('fsp4', 25, '1991-06-23'))
    sheet.write(person)
    sheet.write(persons)


    for p in sheet.read():
        print (p, p.name, p.age, p.birthday)

