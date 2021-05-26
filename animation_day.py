# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:55:46 2021

@author: Eric Einspaenner
"""
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os
import re

#%% Functions

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key, reverse=False)

def karten_visual(j, minimum, maximum):
    cursor= connection.cursor()
    messstellenNr=[]
    AQI_wert=[]
    RGB_colors = []
    x_coords=[]
    y_coords=[]
    
     
    
    cursor.execute('SELECT * FROM messung;')
    res = cursor.fetchall()[minimum:maximum]

    i=0
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
        #print(sqr)
        draw.polygon(sqr,fill=RGB,outline=RGB)

    
    draw.text((10,10), DATUM + '   ' + UHRZEIT + ' Uhr', (0,0,0), font=font)
    
    #Legende
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

    card.save('Output/GIF/bild_0' + str(j) + '.png')
    
    cursor.close()
    
#%% main
if __name__=="__main__":
    connection = sqlite3.connect('data/umwelt.db')
    
    tag1 = 20
    UHRZEIT = "12%"[:2]
    monat1 = 1
    j = 0

    minimum = 240
    maximum = 260

    for wdh in range(20):
        card = Image.open("data/Karte.png")
        draw = ImageDraw.Draw(card)
        font = ImageFont.truetype("arial.ttf", 20)
        tag1 += 1
        if tag1 > 31:
            tag1 = 1
            monat1 += 1
        if tag1 < 10:
            DATUM = f"2021-0{monat1}-0{tag1}"
        else:
            DATUM = f"2021-0{monat1}-{tag1}"

        karten_visual(j, minimum, maximum)
        minimum += 480
        maximum += 480
        j += 1

    frames = []
    py_path = os.getcwd()
    cards = sorted_alphanumeric(os.listdir(py_path + 'Output/GIF'))
    i = 0

    for card in cards:
        card = Image.open(py_path + 'Output/GIF/' + card)

        # convert RGB
        background = Image.new('RGB', card.size,(255,255,255))
        background.paste(card, mask = card.split()[3])
        background.save(f"Output/cardrgb_forgif/frame{i}.png", quality=100)
        frames.append(background)
        i += 1
    
    # GIF
    frames[0].save("Output/Messverlauf_Tage.gif", save_all=True, append_images=frames[1:], duration=1000, loop=0)
