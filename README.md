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
