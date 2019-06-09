#! /usr/bin/env python3

# Ffair Gwyddoniaeth 2019
# Arbrawf Rafik Harrington
# Mesur CO2 mewn sgarff
# Mwy ar https://github.com/skuzzymiglet/ffair-gwyddoniaeth-2019
# Rhaglen fach i gael cipolwg ar eich data

from bokeh.plotting import figure, output_file, show
import csv

data = open("DATA.CSV", "r") # Data o'r synhwyrydd
reader = csv.reader(data, delimiter=',') # I ddarllen y data

# Cyfeirnodau pwyntiau ar y llinell

x = [] # Amser
y = [] # CO2

# Ychwanegu'r holl data i'r echelinau

for row in reader:
    y.append(row[0]) 
    x.append(row[1])

data.close() # Cau'r ffeil

output_file("overview.html") # Y ffeil i blotio iddo

p = figure(title="CO2 ppm", x_axis_label="Time", y_axis_label="CO2 ppm", y_range=[0, int(max(y))]) # Creu y graff
p.line(x, y, line_width=1, color="blue") # Plotio'r llinell

show(p) # Dangos y graff
    

