# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:50:22 2021

@author: Eric Einspaenner
"""
import sqlite3

connection = sqlite3.connect('data/umwelt.db')
print(connection)
cursor = connection.cursor()

#%% Function

# get specific informations from database
def information_messstation(DATUM, UHRZEIT):
    cursor.execute('SELECT * FROM messung WHERE datum=? AND uhrzeit=? ; ', (DATUM,UHRZEIT,))
    res = cursor.fetchall()    
    messstellenNr = res[0][1]
    AQI_wert = res[0][2]
    
    cursor.execute('SELECT coordX,coordY FROM messstelle WHERE messstelleNr=? ; ', (messstellenNr,))
    coords = cursor.fetchall()    
    x_coord = coords[0][0]
    y_coord = coords[0][1]
    
    cursor.execute('SELECT rgbColor FROM rating WHERE ratingNr=? ; ', (AQI_wert,))
    color = cursor.fetchall()[0][0]
    print('Nr.: {}, AQI: {}, X: {}, Y: {}, Color: {}'.format(messstellenNr,AQI_wert,x_coord,y_coord,color))

#%% main
if __name__=="__main__":
    # Output depending on date and time
    information_messstation('2021-01-20','23:57:52')
    
    
