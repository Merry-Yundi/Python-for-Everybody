#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 11:28:30 2017
@author: marui
"""

import sqlite3
from sqlite3 import Error
import re

# Connecting to the file in which we want to store our db
conn = sqlite3.connect('Desktop/py/py15/count_org.sqlite')
cur = conn.cursor()

# Deleting any possible table that may affect this assignment
cur.execute('drop table if exists counts')

# Creating the 'counts' table we're going to use
cur.execute('create table if not exists counts(org TEXT,count INTEGER)')

# Indicating the file from where we'll read the data
fname = input('Enter file name: ')
if (len(fname) < 1):
    fname = 'Desktop/py/py15/mbox-short.txt'
fh = open(fname)

# Reading each line with an emil address in the file
for line in fh:
    if not line.startswith('From: ') : continue

    # Splitting it into a list of words and assign the second word to 'email'
    pieces = line.split()
    email = pieces[1]

    # Splitting 'email' into 2 parts at the point of '@' and assign the last word to 'org'
    parts = email.split('@')
    org = parts[-1]

    # Updating the table with the correspondent information
    cur.execute('select count from counts where org = ?',(org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('insert into counts (org, count) values (?, 1)',(org,))
    else:
        cur.execute('update counts set count = count + 1 where org = ?',(org,))

# We commit the changes after they've finished because this speeds up the execution and
# since our operations are not critical, a loss wouldn't suppose any problem
conn.commit()

# Getting the top 10 results and showing them
for row in cur.execute('select org,count from counts order by count desc limit 10'):
    print(str(row[0]), row[1])

#Closing the DB
cur.close()
