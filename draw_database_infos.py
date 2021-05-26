# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 11:54:32 2021

@author: Eric Einspaenner
"""
import sqlite3
from PIL import Image,ImageDraw


connection= sqlite3.connect('umwelt.db')
print(connection)

cursor = connection.cursor()
cursor2 = connection.cursor()

#%% Functions

# created list consisting of tuples
def AQI_Value():
    rowlist = []
    cursor.execute('SELECT ratingNr,aqiMax FROM rating ;')
    rowlist = cursor.fetchall()
    print(rowlist)   

# outputs the max AQI value based on an input     
def AQI_User(schadstoffNr):
    cursor.execute('SELECT aqiMax FROM rating WHERE ratingNr={};'.format(schadstoffNr))
    cursor2.execute('SELECT coordX,coordY FROM messstelle WHERE schadstoffNr={};'.format(schadstoffNr))
    AQI_max_value = cursor.fetchall()
    coords = cursor2.fetchall()

    return AQI_max_value, coords  

#%% main
if __name__=="__main__":
    # call function
    AQI_Value()

    # User-Input
    schadstoffNr= int(input("Schadstoffnummer eingeben (1-5):"))

    # call function
    AQI_max, coords = AQI_User(schadstoffNr)
    print(AQI_max, coords)

    karte=Image.open("data/Karte.png")
    draw = ImageDraw.Draw(karte)

    for coord in coords:
        x = coord[0]
        y = coord[1]
        sqr_center = [x,y]
        sqr_length = 12
        
        sqr =(
        (sqr_center[0] + sqr_length / 2, sqr_center[1] + sqr_length / 2),
        (sqr_center[0] + sqr_length / 2, sqr_center[1] - sqr_length / 2),
        (sqr_center[0] - sqr_length / 2, sqr_center[1] - sqr_length / 2),
        (sqr_center[0] - sqr_length / 2, sqr_center[1] + sqr_length / 2)
        )
        draw.polygon(sqr, outline="black")
        draw.text((x-30, y+10), 'AQI-Wert:' + str(AQI_max[0][0]), (0,0,0))

    karte.save("Output/KartemitText.png")
