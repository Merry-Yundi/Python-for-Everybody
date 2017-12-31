#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 21:02:27 2017

@author: marui
"""

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('Desktop/py/py15/tracks/trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    artist_id INTEGER,
    album_id  INTEGER,
    genre_id  INTEGER,
    length INTEGER,
    rating INTEGER,
    count INTEGER
);
''')


fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Desktop/py/py15/tracks/library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')

for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue
    
    id = lookup(entry, 'Track ID')
    name = lookup(entry, 'Name')
    genre = lookup(entry,'Genre')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or genre is None or artist is None or album is None :
        continue


    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name)
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track (id, title, artist_id, album_id, genre_id,length, rating, count)
        VALUES ( ?, ?, ?, ?, ?, ?, ? ,? )''', ( id, name, artist_id, album_id, genre_id, length, rating, count ) )

    conn.commit()


query = '''SELECT Track.title, Artist.name, Album.title, Genre.name
           FROM Track JOIN Artist JOIN Album JOIN Genre
           ON Track.album_id = Album.id and Track.genre_id = Genre.id and Track.artist_id = Artist.id
           ORDER BY Artist.name LIMIT 3 ;'''
cur.execute(query)

cur.close()
