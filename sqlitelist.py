'''

sqlite list by Richard Ellicott (mescalin@gmail.com)


Sources:
# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html


#override get slice for faster slicing
#https://stackoverflow.com/questions/31874952/how-to-raise-an-indexerror-when-slice-indices-are-out-of-range
def __getslice__(self, i, j):
        len_ = len(self)
        if i > len_ or j > len_:
            raise IndexError('list index out of range')
        return super(MyList, self).__getslice__(i, j)


'''
from __future__ import absolute_import, division, print_function
import sqlite3
import pickle

import random


class SqliteList(object):
    '''
    not working on slices like [0:3]
    '''

    table = 'unnamed'

    def create_table(self):
        '''
        create table if it does not exist
        '''
        self.c.execute('CREATE TABLE IF NOT EXISTS "%s" (value BLOB)' % self.table)

    def drop_table(self):
        self.c.execute('DROP TABLE "%s"' % self.table)

    def __init__(self, filename, pickle_data=True, autocommit=True):

        self.filename = filename
        self.pickle_data = pickle_data
        self.autocommit = autocommit

        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()
        self.create_table()

        # https://stackoverflow.com/questions/16108748/python-using-pickled-objects-with-sqlite

    def append(self, value):
        if self.pickle_data:
            value = pickle.dumps(value)
        value = (value,)
        self.c.execute('INSERT INTO "%s"(value) VALUES (?)' % self.table, value)
        if self.autocommit:
            self.conn.commit()

    def debug_info(self):
        s = ''
        s += '#' * 16 + '\n'
        s += 'SQLITE DATABASE\n'
        s += 'filename: \'{}\'\n'.format(self.filename)
        s += 'length: {}\n'.format(len(self))
        s += '-' * 32 + '\n'
        s += '{}\t|{}\t|{}\t|{}\t|{}\n'.format('key', 'rowid', 'id\t', 'type', 'value')
        index = 0
        for row in self.c.execute('SELECT _rowid_,* FROM %s' % self.table):
            rowid = row[0]
            # v1 with id
            # _id = row[1]
            # val = row[2]
            # v2 no id
            _id = None
            val = row[1]

            val = self.decode(val)
            s += '{}\t|{}\t\t|{}\t\t|{}\t|{}\n'.format(index, rowid, _id, type(val).__name__ + ' ', val)
            index += 1
        s += '#' * 16
        return s

    # def get_ids(self):
    #     new_list = []
    #     for row in self.c.execute('SELECT id FROM unnamed'):
    #         val = row[0]
    #         # if self.pickle_data:
    #         #     val = pickle.loads(val)
    #         new_list.append(val)
    #     return new_list

    # def get_rowids(self):
    #     new_list = []
    #     for row in self.c.execute('SELECT _rowid_ FROM unnamed'):
    #         val = row[0]
    #         # if self.pickle_data:
    #         #     val = pickle.loads(val)
    #         new_list.append(val)
    #     return new_list

    def encode(self, value):
        if self.pickle_data:
            value = pickle.dumps(value)
        return value

    def decode(self, value):
        if self.pickle_data:
            value = pickle.loads(value)
        return value

    def __iter__(self):
        '''
        allows conversion to list/tuples etc
        '''
        # GET_VALUES = 'SELECT value FROM "%s" ORDER BY id' % self.tablename
        GET_VALUES = 'SELECT value FROM "%s"' % self.table
        for value in self.c.execute(GET_VALUES):  # this varied from sqlitedict
            yield self.decode(value[0])

    def __add__(self, other):
        return list(self) + list(other)

    last_length = None

    def __len__(self):
        self.c.execute('SELECT Count(*) FROM unnamed')
        return self.c.fetchone()[0]

    def commit(self):
        self.conn.commit()

    def delete_by_id(self, row_id):
        '''
        delete row by id
        '''
        self.c.execute('DELETE FROM unnamed WHERE id = (?)', (row_id,))
        if self.autocommit:
            self.conn.commit()

    # def get_last(self):
    #     '''
    #     may be depreciated
    #     '''
    #     self.c.execute('SELECT * FROM unnamed WHERE id = (SELECT MAX(ID) FROM unnamed)')
    #     # self.c.execute('SELECT * FROM unnamed ORDER BY id DESC LIMIT 1')  # different syntax
    #     row = self.c.fetchone()
    #     val = row[1]
    #     if self.pickle_data:
    #         val = pickle.loads(val)
    #     return val

    # def delete_last(self):
    #     '''
    #     may be depreciated
    #     delete row with highest id
    #     '''
    #     self.c.execute('DELETE FROM unnamed WHERE id = (SELECT MAX(id) FROM unnamed)')
    #     if self.autocommit:
    #         self.conn.commit()

    # def get_first(self):
    #     '''
    #     may be depreciated
    #     '''
    #     # https://stackoverflow.com/questions/5408201/how-to-get-first-top-row-of-the-table-in-sqlite-via-sql-query
    #     # self.c.execute('SELECT * FROM unnamed ORDER BY ROWID ASC LIMIT 1')
    #     self.c.execute('SELECT * FROM unnamed WHERE id = (SELECT MIN(id) FROM unnamed)')
    #     row = self.c.fetchone()
    #     val = row[1]
    #     if self.pickle_data:
    #         val = pickle.loads(val)
    #     return val

    # def delete_first(self):
    #     '''
    #     may be depreciated
    #     '''
    #     self.c.execute('DELETE FROM unnamed WHERE id = (SELECT MIN(id) FROM unnamed)')
    #     if self.autocommit:
    #         self.conn.commit()

    def clear(self):
        self.c.execute('DELETE FROM unnamed')
        # self.drop_table()
        # self.create_table()
        if self.autocommit:
            self.conn.commit()

    def overwrite_all(self, new_list):
        '''
        clears the whole database and writes in new values from an iterator object (like a list)
        '''
        self.clear()
        for val in new_list:
            self.append(val)

    def insert(self, position, val):
        '''
        highly ineffecient as this involves rebuilding the database!
        '''
        if position > len(self):
            raise Exception('position {} is longer than length {}'.format(position, len(self)))
        elif position < 0:
            raise Exception('position {} is less than 0'.format(position))
        this_list = list(self)
        new_list = this_list[:position] + [val] + this_list[position:]
        self.overwrite_all(new_list)

    def __getitem__(self, index):

        # # version 1, creates an entire list which is slow but it works
        # if key == 0:  # optimized
        #     return self.get_first()
        # elif(key == len(self) - 1):  # optimized
        #     return self.get_last()
        # else:  # unoptimal, gets all
        #     return list(self)[key]

        # version 2, should be faster
        # note how this uses no id! it's strange but i think safe

        if index >= len(self):  # if the index is too high throw error
            raise IndexError('list index out of range')
        if index < 0:  # if the index is negative, work our new key
            index = len(self) + index
            if index < 0:
                raise IndexError('list index out of range')  # if our new key ends up negative again, throw index error

        self.c.execute('SELECT value FROM unnamed LIMIT 1 OFFSET %s' % index)
        row = self.c.fetchone()
        val = row[0]
        val = self.decode(val)
        return val

    def get_rowid_by_index(self, row_number):
        '''
        index as defined as the actual sequnece, first entry=0, second=1 etc
        get record by the row number, this is unusual practise for a database
        https://stackoverflow.com/questions/14782559/how-to-get-a-row-in-sqlite-by-index-not-by-id
        '''
        self.c.execute('SELECT _rowid_ FROM unnamed LIMIT 1 OFFSET %s' % row_number)
        row = self.c.fetchone()
        return row[0]

    def __setitem__(self, index, value):
        # version 1, just recreate the entire list, reference implementation
        # new_list = self.__list__()
        # new_list[key] = value
        # self.overwrite_all(new_list)

        # version 2
        # UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
        # https://www.tutorialspoint.com/sqlite/sqlite_update_query.htm
        rowid = self.get_rowid_by_index(index)
        value = self.encode(value)
        self.c.execute('UPDATE unnamed SET value=? WHERE _rowid_ = %s' % rowid, (value,))
        if self.autocommit:
            self.conn.commit()

    def __delitem__(self, index):
        rowid = self.get_rowid_by_index(index)
        self.c.execute('DELETE FROM unnamed WHERE _rowid_ = %s' % rowid)
        if self.autocommit:
            self.conn.commit()

    def __repr__(self):
        return 'SqliteList(\'{}\')'.format(self.filename)

    # def __unicode__(self):
    #     return unicode(self.__list__())

    def __str__(self):
        return self.__repr__()

    def get_random_index(self):
        length = len(self)
        return random.randint(0, length - 1)
