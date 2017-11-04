sqlite list is a list style object, based on the epic sqlitedict:
https://github.com/RaRe-Technologies/sqlitedict

    from SqliteList import SqliteList
    sqlitelist = SqliteList('database.sqlite')
    sqlitelist.append('some string')
    sqlitelist.append(1234)
    sqlitelist.append(['any', 'picklable', 'object'])
    for val in sqlitelist:
        print(val)
    sqlitelist.clear()

warning, this is unfinished, usable only in one of my projects at the moment

it even breaks standard practise in SQLITE using an offset and not a primary key (it's not within sqlite spec, i had this discussion on stack overflow), i am gonna finish it later!

the file format for example is WRONG at the moment, the final file format will have a primary key again:

it will have id as autoincrement, because according to sqlite spec this is now an alias of the _uid_

i had decided to remove this and WRONGLY use _uid_ or even more WRONGLY use 'offset'

after this point, even with bugs, at least it will be compatible with itself in future
