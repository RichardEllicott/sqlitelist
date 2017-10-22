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
    Version 1, experimental, not even a list yet
    '''

    def create_table(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS unnamed (id INTEGER PRIMARY KEY AUTOINCREMENT, value BLOB)')

    def drop_table(self):
        self.c.execute('DROP TABLE unnamed')

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
        self.c.execute('INSERT INTO unnamed(value) VALUES (?)', value)
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

        # print('{}\t{}\t{}'.format('id','type','value'))

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

    def __iter__(self):
        return self.__list__()

    def __list__(self):
        new_list = []
        # for row in self.c.execute('SELECT * FROM unnamed'):
        for row in self.c.execute('SELECT value FROM unnamed'):
            val = row[0]
            if self.pickle_data:
                val = pickle.loads(val)
            new_list.append(val)
        return new_list
        # data = self.c.execute('SELECT value FROM unnamed').fetchall()
        # print(data)

    def __id_list__(self):
        new_list = []
        for row in self.c.execute('SELECT id FROM unnamed'):
            val = row[0]
            # if self.pickle_data:
            #     val = pickle.loads(val)
            new_list.append(val)
        return new_list

    # def __iter__(self):
    #     # for i in range(self.n):
    #     #     yield i * i
    #     return self.get_list()

    #     # this may be more effecient
    #     # https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows
    #     pass

    def __add__(self, other):
        try:
            other = other.__list__()
        except AttributeError as e:
            # print(type(e),e)
            pass
        return self.__list__() + other

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
        if position > len(self):
            raise Exception('position {} is longer than length {}'.format(position, len(self)))
        elif position < 0:
            raise Exception('position {} is less than 0'.format(position))
        this_list = self.__list__()
        new_list = this_list[:position] + [val] + this_list[position:]
        self.overwrite_all(new_list)

    def add_with_id(self, id, val):
        '''
        not implemented
        '''
        pass

    def segment(self, start_pos=0, end_pos=3):
        '''
        todo can be dropped
        not implemented
        '''
        self.c.execute('SELECT * FROM unnamed ORDER BY ROWID ASC LIMIT {}'.format(end_pos))
        row = self.c.fetchall()
        print ('segment', row)
        pass

    def listkey_to_db_id(self, key):

        pass

    def __getitem__(self, key):
        if key == 0:  # optimized
            return self.get_first()
        elif(key == len(self) - 1):  # optimized
            return self.get_last()
        else:  # unoptimal, gets all
            return self.__list__()[key]

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
            self.delete_first()
        elif(key == len(self) - 1):  # deleting last value., optimized
            self.delete_last()
        else:  # unoptimal, recreates list
            new_list = self.__list__()
            del(new_list[key])
            self.overwrite_all(new_list)

    def __repr__(self):
        # return 'SqliteList(' + str(self.__list__()) + ')'
        return 'SqliteList(\'{}\')'.format(self.filename)

    def random_id(self):
        return random.choice(self.__id_list__())

    # def __unicode__(self):
    #     return unicode(self.__list__())

    def __str__(self):
        return self.__repr__()
