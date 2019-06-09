# Ffair Gwyddoniaeth 2019
# Arbrawf Rafik Harrington
# Mesur CO2 mewn sgarff
# Mwy ar https://github.com/skuzzymiglet/ffair-gwyddoniaeth-2019
# Rhannu data o'r Arduino mewn i ddyddiau a chreu strwythyr ffowlderau ar eu cyfer

import json
import csv
import time
import os

datafile = open("DATA.CSV", "r") # Data o'r synhwyrydd

reader = csv.reader(datafile, delimiter=',') # I ddarllen y data

days = {} # Dyddiau a'u data {dydd: [[lefel co2, amser], [lefel co2, amser], yyb]}

def split_days():

    # RHANNU'R DATA I MEWN I DDYDDIAU

    for row in reader: # I bob cofnod o ddata
        tobj = time.localtime(int(row[1])) # Troi'r rhif mawr yn amser
        doy = time.strftime("%d-%m-%y", tobj) # Dydd y flwyddyn (dydd-mis-blwyddyn)
        if not doy in days.keys(): # Os nad ydym wedi prosesu data o'r dydd yma eto...
            days[doy] = [[int(row[0]), int(row[1])]] # Ychwanegir y dydd newydd a'r cofnod i'r dyddiau
        else: # Fel arall
            days[doy].append([int(row[0]), int(row[1])]) # Ychwanegu'r cofnod

    # CREU FFOWLDERI A FFEILIAU I'R DATA

    for day in days: # I bob dydd
        try:
            os.makedirs("days/"+day) # Trio creu ffowlder o enw'r dyddiad
        except OSError: # Os yw'r ffowlder yn bodoli...
            pass # Does dim rhaid gwneud unrhywbeth
        dump = open("days/"+day+"/"+"day.json", "w") # Y ffeil y roi data y dydd ynddo
        json.dump(days[day], dump) # Rhoi'r data mewn
        dump.close() # Arbed a chau'r ffeil 




