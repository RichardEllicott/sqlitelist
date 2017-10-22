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


# sqlitelist.delete_row(3)

# sqlitelist.delete_last_row()

# sqlitelist.delete_all_rows()


# print(list(sqlitelist))

# print(sqlitelist.get_last())

# print(sqlitelist.get_first_row())

# sqlitelist.delete_first_row()


list_test = [33, 67, 99]
# for val in dir(list_test):
#     print (val)
# print (list_test.count())

# print (sqlitelist + [1,4,7])

# sqlitelist.delete_all()


# sqlitelist.insert(100,'gg')

# sqlitelist.overwrite_all([5,7,99])





# sqlitelist.clear()

# fill_random_data_test()




# sqlitelist.insert(-1, 'hello1100000--xxx----')

# del(sqlitelist[0])

# sqlitelist[1] = 'xfxfxfx'

print(sqlitelist.debug_info())

# print(sqlitelist.get_by_row(2))


print(list(sqlitelist))



# from sqlitedict import SqliteDict
# sqlitedict_test = SqliteDict(get_desktop_path() + '/SqliteDictTest.sqlite', autocommit=True)
# print(sqlitedict_test)
# sqlitedict_test['xxx'] = 757
# sqlitedict_test['xxx22'] = 7676
# # sqlitedict_test = dict(sqlitedict_test)
# sqlitedict_test = list(sqlitedict_test)
# print(sqlitedict_test)



# sqlitelist.append('NEW DATA')

'''
from SqliteList import SqliteList
sqlitelist = SqliteList(database_test.sqlite')
'''


# import sys
# print(sys.version_info)
# print ('ssss') if 3 > 2 else print('xx')

print(sqlitelist)
print(sqlitelist + range(3))


# print(sqlitelist[1:3])

# print(sqlitelist[-1])

# del(sqlitelist[-1])

import random

print(random.choice(sqlitelist))



print(list(sqlitelist))
# print(sqlitelist[4])



print(sqlitelist[-5])
print(list(sqlitelist)[-5])










