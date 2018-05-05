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
