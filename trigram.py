# -*- coding: utf-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import collections
import re
import sqlite3

connection = sqlite3.connect('trigramDB.db')

file = open('corpus.txt').read()
commaSplit = file.split('،')
file = ' '.join(commaSplit)
periodSplit = file.split('.')
file = ' '.join(periodSplit)
englishCommaSplit = file.split(',')
file = ' '.join(englishCommaSplit)
words = file.split()
print words

counter = collections.Counter(words)
countDict = dict(counter)

wordPairs = []
for word in countDict:
    for otherWord in countDict:
        pair = (word, otherWord)
        wordPairs.append(pair)


cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS wordCount
             (word text, count INTEGER)''')

for word in countDict:
    t = (unicode(word, encoding='utf-8'), countDict[word])
    cursor.execute("INSERT INTO wordCount VALUES (?, ?)", t)

connection.commit()

#for row in cursor.execute('SELECT * FROM wordCount'):
        # print row

cursor.execute('''CREATE TABLE IF NOT EXISTS pair
             (pair text)''')

for pair in wordPairs:
    str = ' '.join(pair)
    str = unicode(str, encoding='utf-8')
    str = (str,)
    cursor.execute("INSERT INTO pair VALUES (?)", str)

connection.commit()

# for row in cursor.execute('SELECT * FROM pair'):
#         print row

cursor.execute('''CREATE TABLE IF NOT EXISTS frequency
             (sentence text, count INTEGER)''')




for pair in wordPairs:
    for word in countDict:
        pattern = ' '.join(pair)
        pattern = pattern + ' ' + word
        # print pattern
        starts = [match.start() for match in re.finditer(re.escape(pattern), file)]
        t = (unicode(pattern, encoding='utf-8'), len(starts))
        cursor.execute("INSERT INTO frequency VALUES (?, ?)", t)
        connection.commit()


for row in cursor.execute('SELECT * FROM frequency'):
        print row