# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:07:25 2021

@author: Eric Einspaenner
"""
import sqlite3

connection = sqlite3.connect('data/umwelt.db')
print(connection)

cursor = connection.cursor()

#%% create a new table
with open('data/Messstellen.txt') as data:
    id_NO2 = []
    y_coords_NO2 = []
    x_coords_NO2 = []
    lines = data.readlines()

    for line in lines[1:]:
        id_NO2.append(int(line[0]))
        y_coords_NO2.append(int(line[2:4]))
        x_coords_NO2.append(int(line[6:]))

    cursor.execute('''CREATE TABLE messstelle_NO2 (id_NO2 INTEGER, y_coords_NO2 INTEGER, x_coords_NO2 INTEGER) ''')

    for i in range(len(id_NO2)):
        cursor.execute('''INSERT INTO messstelle_NO2 
                       (id_NO2,y_coords_NO2,x_coords_NO2) 
                       VALUES 
                       ({},{},{})'''.format(id_NO2[i], y_coords_NO2[i], x_coords_NO2[i]))
    connection.commit()

cursor.close 
connection.close()
