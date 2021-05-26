# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:55:46 2021

@author: Eric Einspaenner
"""
import sqlite3
from PIL import Image, ImageDraw, ImageFont

connection = sqlite3.connect('data/umwelt.db')
print(connection)
cursor = connection.cursor()

messstellenNr = []
AQI_wert = []
RGB_colors = []
x_coords = []
y_coords = []


def karten_visual():
    card = Image.open("data/Karte.png")
    draw = ImageDraw.Draw(card)
    font = ImageFont.truetype("arial.ttf", 20) 
    
    cursor.execute('SELECT * FROM messung;')
    res = cursor.fetchall()[:20]

    i = 0
    for Nr in res:
        messstellenNr.append(res[i][1])
        if res[i][2] < 25:
            AQI_wert.append(1)
        if 24 < res[i][2] < 50:
            AQI_wert.append(2)
        if 49 < res[i][2] < 75:
            AQI_wert.append(3)
        if 74 < res[i][2] < 100:
            AQI_wert.append(4)
        if 99 < res[i][2] <= 500:
            AQI_wert.append(5)
        i += 1
    
    for Nr in messstellenNr:
        cursor.execute('SELECT coordX,coordY FROM messstelle WHERE messstelleNr=? ; ', (Nr,))
        coords = cursor.fetchall()
        x_coords.append(coords[0][0])
        y_coords.append(coords[0][1])

    for AQI in AQI_wert:
        cursor.execute('SELECT rgbColor FROM rating WHERE ratingNr=? ; ', (AQI,))
        RGB_colors.append(str(cursor.fetchall()[0][0]))

    for x,y,RGB in zip(x_coords,y_coords,RGB_colors):
        sqr_center = [x,y]
        sqr_length = 12
        
        sqr =(
        (sqr_center[0] + sqr_length / 2, sqr_center[1] + sqr_length / 2),
        (sqr_center[0] + sqr_length / 2, sqr_center[1] - sqr_length / 2),
        (sqr_center[0] - sqr_length / 2, sqr_center[1] - sqr_length / 2),
        (sqr_center[0] - sqr_length / 2, sqr_center[1] + sqr_length / 2)
        )
        draw.polygon(sqr,fill=RGB,outline=RGB)

    DATUM = str(res[0][3])
    UHRZEIT = str(res[0][4][:2])
    draw.text((10,10), DATUM + '   ' + UHRZEIT + ' Uhr', (0,0,0), font=font)
    
    # Legend
    draw.rectangle((10, 770, 140, 790),fill=(255,255,255),outline=(255,255,255))
    draw.rectangle((150, 770, 300, 790),fill=(255,255,255),outline=(255,255,255))
    draw.rectangle((310, 770, 460, 790),fill=(255,255,255),outline=(255,255,255))
    draw.rectangle((470, 770, 620, 790),fill=(255,255,255),outline=(255,255,255))
    draw.rectangle((630, 770, 790, 790),fill=(255,255,255),outline=(255,255,255))
    
    draw.text((10,775), 'Sehr niedrig', (0,0,0))
    draw.text((150,775),'Niedrig', (0,0,0))
    draw.text((310,775), 'Mittel', (0,0,0))
    draw.text((470,775), 'Hoch', (0,0,0))
    draw.text((630,775), 'Sehr hoch', (0,0,0))
    
    draw.rectangle((110, 775, 120, 785),fill='#7aeb34',outline='#7aeb34')
    draw.rectangle((250, 775, 260, 785),fill='#b4eb34',outline='#b4eb34')
    draw.rectangle((410, 775, 420, 785),fill='#e2eb34',outline='#e2eb34')
    draw.rectangle((570, 775, 580, 785),fill='#eba834',outline='#eba834')
    draw.rectangle((730, 775, 740, 785),fill='#eb3434',outline='#eb3434')

    card.save('Output/Map_with_infos.png')
    
#%% main
if __name__=="__main__":
    karten_visual()

    
    