from bokeh.plotting import figure
from bokeh.models import Dropdown
from bokeh.layouts import column
from bokeh.io import curdoc
import csv

T = list(range(1, 13))

Z1 = [0]*12
Z2 = [0]*12

# read CSV, get monthly avgs and zipcodes
def get_data():
    data_311 = {}
    zipcodes = []
    all_avgs = [0]*12
    
    with open("../data/monthly_averages.csv") as f1:
        reader = csv.reader(f1)
        next(reader)

        for row in reader:
            z, m, avg = row

            if z not in data_311:
                data_311[z] = [0]*12
                zipcodes.append(z)

            data_311[z][int(m)-1] = float(avg)

    with open("../data/all_avgs.csv") as f2:
        reader = csv.reader(f2)
        next(reader)

        for row in reader:
            m, avg = row
            all_avgs[int(m)-1] = float(avg)        

    print (data_311)
    return data_311, zipcodes, all_avgs

data_311, zipcodes, all_avgs = get_data()

Z1 = data_311[zipcodes[0]]
Z2 = data_311[zipcodes[1]]  

# figure with 3 lines 

max_y = max(max(v) for v in data_311.values())

p = figure(x_range = (1, 12), 
           y_range=(0, max_y), 
           title = "Average Monthly Response Time by Zipcode",
           x_axis_label = "Month",
           y_axis_label = "Average Response Time (hours)")

r1 = p.line(T, Z1, color="blue", legend_label="Zipcode 1")
r2 = p.line(T, Z2, color="pink", legend_label="Zipcode 2")
r3 = p.line(T, all_avgs, color="purple", legend_label="All Zipcodes Avg")

ds1 = r1.data_source
ds2 = r2.data_source

def update_zip1(event):
    zip1 = event.item
    ds1.data = {"x": T, "y" : data_311[zip1]}
    r1.legend_label = ("Zipcode " + str(zip1))

def update_zip2(event):
    zip2 = event.item
    ds2.data = {"x": T, "y" : data_311[zip2]}
    r2.legend_label = ("Zipcode " + str(zip2))

menu1 = [(z, z) for z in zipcodes]
menu2 = [(z, z) for z in zipcodes]

dropdown1 = Dropdown(label="Select Zipcode 1", menu = menu1)
dropdown2 = Dropdown(label="Select Zipcode 2", menu = menu2)

dropdown1.on_event("menu_item_click", update_zip1)
dropdown2.on_event("menu_item_click", update_zip2)

curdoc().add_root(column(p, dropdown1, dropdown2))