'''

sqlite list by Richard Ellicott


Sources:
# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html



'''
from __future__ import absolute_import, division, print_function
import sqlite3
import pickle


class SqliteList(object):
    '''
    Version 1, experimental
    '''

    tablename = 'unnamed'

    def create_table(self):
        '''
        create table if it does not exist
        '''
        self.c.execute('CREATE TABLE IF NOT EXISTS "%s" (id INTEGER PRIMARY KEY AUTOINCREMENT, value BLOB)' % self.tablename)

    def drop_table(self):
        '''
        drop table
        '''
        self.c.execute('DROP TABLE "%s"' % self.tablename)

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
        self.c.execute('INSERT INTO "%s"(value) VALUES (?)' % self.tablename, value)
        if self.autocommit:
            self.conn.commit()

    def debug_info(self):
        s = ''
        s += '#' * 16 + '\n'
        s += 'SQLITE DATABASE\n'
        s += 'filename: \'{}\'\n'.format(self.filename)
        s += 'length: {}\n'.format(len(self))
        s += '-' * 32 + '\n'
        s += '{}\t|{}\t|{}\t|{}\n'.format('id', 'key', 'type', 'value')
        list_key = 0
        for row in self.c.execute('SELECT * FROM unnamed'):
            key = row[0]
            val = row[1]
            if self.pickle_data:
                val = pickle.loads(val)
            s += '{}\t|{}\t\t|{}\t|{}\n'.format(key, list_key, type(val).__name__ + ' ', val)
            list_key += 1
        s += '#' * 16
        return s



    def get_ids(self):
        new_list = []
        for row in self.c.execute('SELECT id FROM unnamed'):
            val = row[0]
            # if self.pickle_data:
            #     val = pickle.loads(val)
            new_list.append(val)
        return new_list

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
        GET_VALUES = 'SELECT value FROM "%s"' % self.tablename
        for value in self.c.execute(GET_VALUES):  # this varied from sqlitedict
            yield self.decode(value[0])

    def __add__(self, other):
        return list(self) + list(other)

    def __len__(self):
        self.c.execute('SELECT Count(*) FROM unnamed')
        return self.c.fetchone()[0]

    def commit(self):
        self.con.commit()

    def delete_by_id(self, row_id):
        '''
        delete row by id
        '''
        self.c.execute('DELETE FROM unnamed WHERE id = (?)', (row_id,))
        if self.autocommit:
            self.conn.commit()

    def get_last(self):
        self.c.execute('SELECT * FROM unnamed WHERE id = (SELECT MAX(ID) FROM unnamed)')
        # self.c.execute('SELECT * FROM unnamed ORDER BY id DESC LIMIT 1')  # different syntax
        row = self.c.fetchone()
        val = row[1]
        if self.pickle_data:
            val = pickle.loads(val)
        return val

    def delete_last(self):
        '''
        delete row with highest id
        '''
        self.c.execute('DELETE FROM unnamed WHERE id = (SELECT MAX(id) FROM unnamed)')
        if self.autocommit:
            self.conn.commit()

    def get_first(self):
        # https://stackoverflow.com/questions/5408201/how-to-get-first-top-row-of-the-table-in-sqlite-via-sql-query
        # self.c.execute('SELECT * FROM unnamed ORDER BY ROWID ASC LIMIT 1')
        self.c.execute('SELECT * FROM unnamed WHERE id = (SELECT MIN(id) FROM unnamed)')
        row = self.c.fetchone()
        val = row[1]
        if self.pickle_data:
            val = pickle.loads(val)
        return val

    def delete_first(self):
        self.c.execute('DELETE FROM unnamed WHERE id = (SELECT MIN(id) FROM unnamed)')
        if self.autocommit:
            self.conn.commit()

    def clear(self):
        self.c.execute('DELETE FROM unnamed')
        # self.drop_table()
        # self.create_table()
        if self.autocommit:
            self.conn.commit()

    def overwrite_all(self, new_list):
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
        this_list = self.__list__()
        new_list = this_list[:position] + [val] + this_list[position:]
        self.overwrite_all(new_list)

    



    def __getitem__(self, key):
        if key == 0:  # optimized
            return self.get_first()
        elif(key == len(self) - 1):  # optimized
            return self.get_last()
        else:  # unoptimal, gets all
            return list(self)[key]

    def __setitem__(self, key, value):
        '''
        unoptimal, recreates list 
        '''
        new_list = self.__list__()
        new_list[key] = value
        self.overwrite_all(new_list)

    def __delitem__(self, key):
        '''
        only fast for last and first record
        '''
        if key == 0:  # deleting first value, optimized
            print('SQLITELIST optimized route!!')
            self.delete_first()
        elif(key == len(self) - 1):  # deleting last value., optimized
            print('SQLITELIST optimized route!!')
            self.delete_last()
        else:  # unoptimal, recreates list
            print('SQLITELIST WARNING, recreating entire DB')
            new_list = list(self)
            del(new_list[key])
            self.overwrite_all(new_list)

    def __repr__(self):
        return 'SqliteList(\'{}\')'.format(self.filename)

    def random_id(self):
        return random.choice(self.__id_list__())

    def get_by_row(self, row_number):
        '''
        get record by the row number, this is unusual practise for a database
        https://stackoverflow.com/questions/14782559/how-to-get-a-row-in-sqlite-by-index-not-by-id
        '''
        self.c.execute('SELECT * FROM unnamed LIMIT 1 OFFSET {}'.format(row_number))
        row = self.c.fetchone()
        val = row[1]
        if self.pickle_data:
            val = pickle.loads(val)
        return val

    # def __unicode__(self):
    #     return unicode(self.__list__())

    def __str__(self):
        return self.__repr__()
