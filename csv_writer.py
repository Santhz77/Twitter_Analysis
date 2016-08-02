import csv
import json


data = []
with open("stream_adityaag.json") as file:
    for each_line in file:
        data.append(json.loads(each_line.rstrip()))

    for each_element in data:
        print(each_element)

    '''with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)'''




