'''

New test of the Object Orientated Cache Creature




TODO:
cell data to btsync
start to use browser class object
save functions must have the disk space check



get amazon/ebay products from search


*** WORKING ON PERSISTANT LINKS LIST, done pickle, ref implementation




'''
from __future__ import absolute_import, division, print_function

from SqliteList import SqliteList



sqlitelist = SqliteList('SqliteListTest.sqlite')


# sqlitelist.append('hello2222')
# sqlitelist.append([1,5,6,7])


def fill_random_data_test():
    import random
    import string
    # sqlitelist.clear()
    for n in range(5):
        sqlitelist.append('str' + ''.join([random.choice(string.digits) for n in xrange(2)]))
# fill_random_data_test()



# del(sqlitelist[0])

# sqlitelist.insert(3,'bbbb')

print(sqlitelist.debug_info())


print(list(sqlitelist))

# print(sqlitelist[-1])


# print(sqlitelist.get_random_index())


# sqlitelist.insert(0,'6')

