from pandas import read_excel, read_csv
from datetime import datetime
from codecs import open

typering = read_csv("typeerpostcode.csv", delimiter=';')
coord = read_csv("coordinaten.csv", delimiter=';')

df = read_excel("gegevens.xlsx", sheetname='theaterdans1014')

df = df[df["Datum tot"].between(datetime(2014, 1, 1), datetime(2014, 12, 31))]

with open("landen.txt", "r", "utf-8") as f:
    landnamen = f.readlines()
    landnamen = [n.strip() for n in landnamen]


data = {}
for i in df.index:
    tekst = df["tekst"][i]
    gemeente = df["Gemeente"][i]
    for landnaam in landnamen:
        if landnaam in tekst:
            typeringlijn = typering[typering["Gemeente Origineel"] == gemeente]
            fusiegemeente = typeringlijn["Fusiegemeente"].values[0]
            provincie = typeringlijn["Province (English)"].values[0]
            lat = coord[coord["Fusiegemeente"] == fusiegemeente]["latitude"].values[0]
            lon = coord[coord["Fusiegemeente"] == fusiegemeente]["longitude"].values[0]

            if fusiegemeente not in data:
                data[fusiegemeente] = {"latitude": lat,
                                       "longitude": lon,
                                       "provincie": provincie,
                                       "landen": {}
                                       }

            if landnaam not in data[fusiegemeente]["landen"]:
                data[fusiegemeente]["landen"][landnaam] = 0
            data[fusiegemeente]["landen"][landnaam] += 1

lines = []
for fusiegemeente in data:
    for land in data[fusiegemeente]["landen"]:
        lines.append(";".join([fusiegemeente,
                               data[fusiegemeente]["latitude"],
                               data[fusiegemeente]["longitude"],
                               land,
                               str(data[fusiegemeente]["landen"][land])]))

with open("corpusanalyse uitdatabank.csv", "w", "utf-8") as f:
    f.write("\n".join(lines))