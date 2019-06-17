# Ffair Gwyddoniaeth 2019
# Arbrawf Rafik Harrington
# Mesur CO2 mewn sgarff
# Mwy ar https://github.com/skuzzymiglet/ffair-gwyddoniaeth-2019
# I bob dydd o ddata, creu ffeil gyda dim ond data'r arbrawf

import json
import os 
import time

def filter_data():

    for date in os.listdir("days/"): # I bob ffowlder dydd 

        # DEWIS Y COFNODAU

        day = open("days/"+date+"/day.json", "r") # Agor y ffeil gyda data'r dydd ynddo
        data = json.load(day) # Darllen y data
        day.close() # Cau y ffeil

        filtered = [] # Y data newydd 

        for record in data: # I bob cofnod
            tobj = time.localtime(int(record[1])) # Troi'r rhif mawr yn amser
            t = time.strftime("%H%M", tobj) # Amser 24-awr e.e 0850, 2217
            if (int(t) >= 855 and int(t) <= 925) or (date == "16-06-19" and int(t) >= 1900): # Os yw'r amser rhwng 07:55 a 08:25, tua fy amser seiclo (awr o flaen)
                filtered.append(record) # Ychwanegu'r cofnod i'r data newydd
            else: # Fel arall
                continue # Mynd at y cofnod nesaf
        
        # EU RHOI MEWN FFEIL (filtered.json)

        filtered_file = open("days/"+date+"/filtered.json", "w") # Y ffeil
        json.dump(filtered, filtered_file) # Ysgrifennu'r data newydd
        filtered_file.close() # Arbed a chau
