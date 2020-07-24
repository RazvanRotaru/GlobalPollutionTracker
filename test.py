import matplotlib.pyplot as plt
from tkinter import *
import pymongo
from pymongo import MongoClient
from bson.code import Code
from bson.son import SON


window = Tk()
window.title("PollutionDB")
window.geometry('1100x300')

client = MongoClient('localhost', 27017)

db = client.get_database("config")
collection = db.get_collection("continents")

continents = []
for post in collection.find({"nume":{"$exists": False}}):
    continents.append({"name": post["name"], "size": post["size (million km2)"],
                       "population": post["population (million)"], "rank": post["rank"]})


category = Label(window, text= "Top polluted contries indexes by continent", font='Helvetica 8 bold')
category.grid(column=1, row=0)

lbl = Label(window, text="Insert continent here:")
lbl.grid(column=0, row=1)

continentEntry = Entry(window, width = 30)
continentEntry.grid(column=1, row=1)


def getPollutionIndexes():
    global client, db, continentEntry
    continent = continentEntry.get()

    countries = []
    plastic_levels = []
    AQI_levels = []
    CO2_levels = []

    _collection = db.get_collection("top_pollutant_countries")

    for post in _collection.find({"continent": continent}, {"_id": 0, "name": 1, "Plastic waste (Mt)": 2}):
        countries.append(post["name"])
        plastic_levels.append(post["Plastic waste (Mt)"])

    for post in _collection.find({"continent": continent}, {"_id": 0, "name": 1, "Capital city AQI": 2}):
        AQI_levels.append(post["Capital city AQI"])

    for post in _collection.find({"continent":continent}, {"_id":0, "name":1, "CO2 emission (Gt)":2}):
        CO2_levels.append(post["CO2 emission (Gt)"])

    plt.figure(figsize=(15, 9))

    ax = plt.subplot(131)
    ax.set_title("Plastic waste (Mt)")
    ax.bar(countries, plastic_levels, width = 0.2, color = "r", align='center')
    ax = plt.subplot(132)
    ax.set_title("Capital city AQI")
    ax.bar(countries, AQI_levels, width=0.2, color="b", align='center')
    ax = plt.subplot(133)
    ax.set_title("CO2 emissions (Gt)")
    ax.bar(countries, CO2_levels, width=0.2, color="g", align='center')

    plt.suptitle(continent + ' top pollutant countries')
    plt.show()

getPollutionLevel = Button(window, text="Show", command = getPollutionIndexes)
getPollutionLevel.grid(column=2, row=1)

category = Label(window, text= "----------------------------------------------------------------------------", font='Helvetica 8 bold')
category.grid(column=1, row=2)

category = Label(window, text= "Total deaths register due to pollution by continent", font='Helvetica 8 bold')
category.grid(column=1, row=3)

lbl = Label(window, text="Insert continent here:")
lbl.grid(column=0, row=4)

deathsEntry = Entry(window, width = 30)
deathsEntry.grid(column=1, row=4)

def getPollutionDeaths():
    global client, db, continentEntry
    continent = deathsEntry.get()
    res = 0;

    Deaths_collection = db.get_collection("deaths")
    for post in Deaths_collection.find({"continent": continent}, {"_id":0, "deaths (k)":1}):
        res = post["deaths (k)"]

    ans = "Total thousands deaths registered: " + str(int(res))
    label = Label(window, text=ans)
    label.grid(column=3, row=4)

getDeaths = Button(window, text="Show", command = getPollutionDeaths)
getDeaths.grid(column=2, row=4)


category = Label(window, text= "----------------------------------------------------------------------------", font='Helvetica 8 bold')
category.grid(column=1, row=5)

category = Label(window, text= "Total endangered species by continent (leave field blank for global statistics)", font='Helvetica 8 bold')
category.grid(column=1, row=6)

lbl = Label(window, text="Insert continent here:")
lbl.grid(column=0, row=7)

endangeredEntry = Entry(window, width = 30)
endangeredEntry.grid(column=1, row=7)

def getEndangeredSpecies():
    global client, db, continentEntry
    continent = endangeredEntry.get()
    res = 0;
    list = []

    Species_collection = db.get_collection("endangered_species")
    for post in Species_collection.find({"continent":continent}, {"_id":0, "animals_endangered":1, "examples":2}):
        res = post["animals_endangered"]
        list = post["examples"]

    if continent=="":
        map = Code("function () {"
                   " emit('endangered', this.animals_endangered); "
                   "}")
        reduce = Code("function(key, values) {"
                      " return Array.sum(values);"
                      "}")
        res = Species_collection.map_reduce(map=map, reduce=reduce, out=SON([('inline', 1)]))
        res = res["results"][0]["value"]

        ans = "Total endangered species: " + str(int(res))
        label = Label(window, text=ans)
        label.grid(column=3, row=7)
        return

    examples = ", ".join(list)
    examples = "counting: " + examples
    ans = "Total endangered species: " + str(int(res))
    label = Label(window, text=ans)

    label.grid(column=3, row=7)

    examplelabel = Label(window, text=examples)
    # examplelabel.grid_forget()
    examplelabel.grid(column=3, row=8)

getEndangered = Button(window, text="Show", command = getEndangeredSpecies)
getEndangered.grid(column=2, row=7)


category = Label(window, text= "----------------------------------------------------------------------------", font='Helvetica 8 bold')
category.grid(column=1, row=8)

category = Label(window, text= "Main pollution sources by continent", font='Helvetica 8 bold')
category.grid(column=1, row=9)

lbl = Label(window, text="Insert continent here:")
lbl.grid(column=0, row=10)

solutionEntry = Entry(window, width = 30)
solutionEntry.grid(column=1, row=10)

def getPollutants():
    global client, db, continentEntry
    continent = solutionEntry.get()
    list = []

    Solution_collection = db.get_collection("main_pollutants")
    for post in Solution_collection.find({"continent":continent}, {"_id":0, "reasons":1}):
        list = post["reasons"]

    examples = ", ".join(list)
    ans = "Main pollution sources: " + str(examples)
    label = Label(window, text=examples)
    label.grid(column=3, row=10)

getSolutions = Button(window, text="Show", command = getPollutants)
getSolutions.grid(column=2, row=10)

# collection.loadServerScripts();
# print(db.system_js.list())
# print(db.system_js["test_func"])
#
# db.system_js["test_func"]('3')
# db.system_js.test_func('3')
# db.eval("""db.system_js["test_func"]""","3")
# db.command("test_func")
# print database_connection.system_js.my_func(['a', 'b'], ['c', 'd'])
# print(db.system_js.test_func('con'))


# res = collection.map_reduce(map=map, reduce=reduce,  out=SON([('inline',1)]))
# print(res["counts"]["output"])

window.mainloop()
client.close()