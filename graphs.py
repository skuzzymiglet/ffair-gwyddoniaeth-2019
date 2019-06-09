# Ffair Gwyddoniaeth 2019
# Arbrawf Rafik Harrington
# Mesur CO2 mewn sgarff
# Mwy ar https://github.com/skuzzymiglet/ffair-gwyddoniaeth-2019
# Creu graffiau amrywiol

from bokeh.plotting import *
from bokeh.io import export_png
import os 
import json

# filtered: defnyddio data 07:55 i 08:25 (True) neu bopeth (False)
# d: dyddiad ar ffurff e.e. 07-06-19

def days(d="", filtered=True, png=False, html=True): # Yr holl ddata o un ddydd neu bob dydd ar raff llinell 
    if filtered:
        to_read = "filtered.json" # Data sydd wedi ei ffiltro gan filter.py
    else:
        to_read = "day.json" # Holl ddata y dydd

    if d == "": # Os yw d yn ddim byd...
        files = ["days/"+day+"/"+to_read for day in os.listdir("days/")] # Plotio pob dyddiad sydd ar gael
        title = "CO2: Pob diwrnod" # Y teitl
        output_name = "days"

    else: # Fel arall...
        files = ["days/"+d+"/"+to_read] # Dim ond y dyddiad d
        title = "CO2 ar "+d  # e.e CO2 ar 07-06-19
        output_name = "day-"+d
    if html:
        output_file(output_name+".html", title=title)

    
    # Echelinau

    x = [] # Amser
    y = [] # CO2

    for f in files: # I bob dyddiad...
        data = open(f, "r") # Agor ei ffeil
        records = json.load(data) # Llwytho'r data
        data.close() # Cau'r ffeil
        for record in records: # I bob cofnod, ychwanegu at yr echelinau
            x.append(record[1])
            y.append(record[0])

    p = figure(title=title, x_axis_label="Amser", y_axis_label="CO2 ppm", y_range=[0, int(max(y))]) # Creu'r graff
    p.line(x, y, line_width=0.5, color="red") # Plotio'r llinell
    if html:
        show(p)
    if png:
        export_png(p, output_name+".png")

def troughs(d="", filtered=True, png=True, html=False): # Pwyntiau yn dangos lefel CO2 isaf cyn iddo godi eto 
    if filtered:
        to_read = "filtered.json"
    else:
        to_read = "day.json"

    if d == "":
        files = ["days/"+day+"/"+to_read for day in os.listdir("days/")]
        title = "Pwyntiau isaf CO2: Pob diwrnod"
        output_name = "troughs"
    else:
        files = ["days/"+d+"/"+to_read]
        title = "Pwyntiau isaf ar "+d 
        output_name = "troughs-"+d

    if html:
        output_file(output_name+".html", title=title)

    p = figure(title=title, x_axis_label="Amser", y_axis_label="CO2 ppm")

    for f in files:
        data = open(f, "r")
        records = json.load(data)
        data.close()

        # DEWIS PWYNTIAU ISAF

        current = [float("inf"), 0] # Cadw trac o'r pwynt diwethaf 
        first_up = False # Rhaid plotio cylch y tro cyntaf rydym yn gweld CO2 yn codi eto
        for record in records: # I bob cofnod
            if record[0] < current[0]: # Os yw'r lefel CO2 yn is na'r isaf o'r blaen
                first_up = True # Byddai y codiad nesaf yn un cyntaf ers gostwng
            elif first_up: # Os oes codiad a dyma'r codiad cyntaf ers gostwng
                p.circle(current[1], current[0]) # Plotio cylch y lefel isaf
                first_up = False # Nid dyma'r tro cyntaf iddo ostwng
            else:
                pass
            current = record # Cadw trac

    if html:
        show(p)
    if png:
        export_png(p, output_name+".png")

   
def peaks(d="", filtered=True, png=True, html=False): # Pwyntiau yn dangos lefel CO2 uchaf cyn iddo ddisgyn eto. Bron yr un peth a troughs
    if filtered:
        to_read = "filtered.json"
    else:
        to_read = "day.json"

    if d == "":
        files = ["days/"+day+"/"+to_read for day in os.listdir("days/")]
        title = "Pwyntiau uchaf: Pob diwrnod"
        output_name = "peaks"
    else:
        files = ["days/"+d+"/"+to_read]
        title = "Pwyntiau uchaf ar "+d 
        output_name = "peaks-"+d 

    if html:
        output_file(output_name+".html", title=title)


    p = figure(title=title, x_axis_label="Amser", y_axis_label="CO2 ppm")

    for f in files:
        data = open(f, "r")
        records = json.load(data)
        data.close()
        current = [float("inf"), 0] 
        first_up = False 
        for record in records:
            if record[0] > current[0]: 
                first_up = True 
            elif first_up: 
                p.circle(current[1], current[0]) 
                first_up = False 
            else:
                pass
            current = record 
    if html:
        show(p)
    if png:
        export_png(p, output_name+".png")

def all_graphs(): # Plotio pob graff ar gyfer pob dydd
    graphs = [day for day in os.listdir("days/")] # Dyddiadau
    for day in graphs: # I bob dyddiad...
        # Plotio pob graff iddo
        days(day)
        troughs(day)
        peaks(day)



