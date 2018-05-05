"""
A drop in replacement for the list that saves it's data persistently in an sqlite file.

A wrapper for the excellent SqliteDict:
https://github.com/RaRe-Technologies/sqlitedict


Example usage:

with SqliteList('sqlitelist_test.sqlite', autocommit=True) as l:
    l.clear()  # clear all items (in the file as well)
    l.append('apple')  # append an item
    l.extend(['orange', 'raspberry'])
    l.append('potato')
    l.insert(1, 'horse')
    print('list:', l)


Reasoning:

-existing SqliteList on pypy seemed to not work right!
-https://github.com/hospadar/sqlite_object seems a little immature?
-i have experimented with raw sqlite including index free methods that are faster and slower in certain ways
-i just need a working version, so i built a wrapper for existing and professional code (this)
-I personally put this to work webscraping, i have a requirement to fill up a list of links i want to follow, that are best represented as a list. You can end up with a lot of links and it would be worrying just putting them in a text/json file.


supported:
clear
get
set
append
extend
pop
delete

not-supported:
reverse
sort
maybe more? 


ISSUES:
autocommit must be enabled, buggy if off
the WHOLE db is copied to memory at the moment, which is easier to code. I built SqliteList for the convenience of easy persistent data and in this form it's already useful to me... however, later i will only copy out records as they are requested allowing dealing with massive data.




"""
from __future__ import absolute_import, division, print_function
import os
from sqlitedict import SqliteDict  # pip install sqlitedict


class SqliteList(list):
    """
    inherit from list, use a sqlite database as a list, do it with a SqliteDict
    """

    autocommit = True  # automatically update database (default is True as we have issues with this off atm)

    def _autocommit(self):
        if self.autocommit:
            self.commit()

    def clear(self):
        """
        clear all list data on db
        warning, a bit slow it deletes each cell individually, as SQlite
        """
        # for i in range(len(self._index)):
        # self.__delitem__(0)

        # for i in range(len(self._index)):
        #     list.__delitem__(self, 0)
        del(self[:])  # delete all on local list (but not DB)

        self._sqlitedict.clear()  # clear whole db
        self._index = []
        self._sqlitedict['index'] = self._index

    def _load_from_db(self):
        if 'index' not in self._sqlitedict:  # if no index add one
            self._sqlitedict['index'] = []
        self._index = self._sqlitedict['index']
        for key in self._index:  # copy all db data to memory! (slow?)
            list.append(self, self._sqlitedict[key])  # append with superclass method

    def __init__(self, filename, autocommit=True, *args):
        self.autocommit = autocommit  # my autocommit called after database operations
        list.__init__(self, *args)
        # self.append('FirstMen')
        # self.name = 'Westeros'
        self._sqlitedict = SqliteDict(filename, autocommit=False)  # init the db, note autocommit is off as this means some of our functions can be faster
        self._load_from_db()  # load data from db

    def _get_random_key(self):
        """
        get a random 128bit key suitable for the database key
        """
        # return os.urandom(16).encode('hex')
        return os.urandom(16)

    def __getitem__(self, key):
        """
        return item (from self not db)
        """
        return list.__getitem__(self, key)  # link to the supertypes method

    def __setitem__(self, key, value):
        """
        set item on both self and db
        no index modification required as order does not change
        """
        list.__setitem__(self, key, value)  # set normal list
        dict_key = self._index[key]  # get db key
        self._sqlitedict[dict_key] = value  # set the db data
        self._autocommit()  # update database

    def insert(self, key, value):
        """
        inserts both to self and db
        """
        list.insert(self, key, value)  # insert to self
        ran_key = self._get_random_key()  # gen a db key
        self._sqlitedict[ran_key] = value  # save value to db
        self._index.insert(key, ran_key)  # insert ref to index cache
        # self.__set_index(self._index)  # save modified index
        self._autocommit()  # update database

    def append(self, value):
        """
        appends both to self and db
        """
        list.append(self, value)  # set normal list
        dict_key = self._get_random_key()  # gen a db key
        self._sqlitedict[dict_key] = value  # save value to db
        self._index.append(dict_key)  # append index
        # self.__set_index(self._index)  # copy index back
        self._autocommit()  # update database

    def extend(self, value):
        """
        has an advantage that it appends all the data as one db write
        """
        list.extend(self, value)  # extend local list
        key_extend = []  # collect the keys so we can extend with one update
        for v in value:
            # self.append(v)  # OLD WAY (KEEP)
            dict_key = self._get_random_key()
            key_extend.append(dict_key)
            self._sqlitedict[dict_key] = v
        self._index.extend(key_extend)  # extend the local index
        # self.__set_index(self._index)  # update the db index
        self._autocommit()  # update database

    def __delitem__(self, key):
        """
        delete from both self and db
        """
        list.__delitem__(self, key)  # delete on local list
        dict_key = self._index[key]  # get the dict ref
        self._index.__delitem__(key)  # delete the index ref
        # self.__set_index(self._index)  # update db index
        self._sqlitedict.__delitem__(dict_key)  # delete the db data
        self._autocommit()  # update database

    def pop(self):
        """
        pop from self and db
        """
        v = self[-1]
        del(self[-1])
        self._autocommit()  # update database
        return v

    def __del__(self):
        """
        ensure database is closed if using delete
        """
        self.close()

    def __enter__(self):
        """
        called after init when using "with"
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # print('SqliteList close')
        self._sqlitedict.close()

    def commit(self):
        """
        update the database, called automaticly if autocommit is True
        """
        self._sqlitedict['index'] = self._index
        self._sqlitedict.commit()


if __name__ == "__main__":
    print('sqlitelist, run some example tests...')
    with SqliteList('sqlitelist_test.sqlite', autocommit=True) as l:
        l.clear()  # clear all items (in the file as well)
        l.append('apple')  # apend an item
        l.extend(['orange', 'raspberry'])
        l.append('potato')
        l.insert(1, 'horse')
        print('list:', l)
