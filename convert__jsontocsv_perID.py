import json
import csv
import os
import config
import sys
import codecs

#to write into the csv header format. This will remain same across.
csv_header = ['Screen Name','Name','Description','URL','Location', 'Time Zone', 'Number of Tweets','Followers Count', 'Following ', 'Listed']
csv_filename = "DATA_223." + "csv" #Please provide appropriate name here
list_of_userdata = []

def write_into_list(data):
    #initialize an array
    row = []

    # add every 'cell' to the row list, identifying the item just like an index in a list
    row.append("@"+data['user']['screen_name'])
    row.append(str(data['user']['name'].encode("utf-8")))
    #row.append(data['user']['name'])
    row.append(str(data['user']['description'].encode("utf-8")))
    #row.append(data['user']['description'])
    row.append(data['user']['url'])
    #row.append(data['user']['location'])
    row.append(str(data['user']['location']).encode("utf-8"))
    row.append(data['user']['time_zone'])
    row.append(data['user']['statuses_count'])
    row.append(data['user']['followers_count'])
    row.append(data['user']['friends_count'])
    row.append(data['user']['listed_count'])

    list_of_userdata.append(row)


def getUsersList():
    print("Program begins")

    # Create a file and include the header
    writer = csv.writer(open(config.user_list_folder + csv_filename, 'w', newline=''))
    writer.writerow(csv_header)

    for filename in os.listdir(config.json_read_folder):
        print("Getting data from file  :" + filename)

        try:
            #Open the file where json data is stored and then load the json file
            with open(config.json_read_folder+filename) as file:
                for each_line in file:
                    parsed_json = json.loads(each_line.rstrip())
                    write_into_list(parsed_json)
                    break
        except:
            with open(config.user_list_folder + "error_list_csv.txt", 'a') as f:
                f.write("Error occurred while getting data from file %s" %filename + "\n")
                print("Error is : " + str(sys.exc_info()[0]))
    index =0
    writer = csv.writer(open(config.user_list_folder + csv_filename, 'a', newline=''))
    for row in list_of_userdata:
        index = index + 1
        writer.writerow(row)
    print(index)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("finished writing into the File %s" % csv_filename)
    print("________________________________________________")








