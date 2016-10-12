import json
import csv
import os
import config
import sys
import codecs

#to write into the csv header format. This will remain same across.
csv_header = ['Text','Created Date','Language','Retweet Count','Retweeted','Favorite Count','Favorited','co-ordinates', 'Tweeted By', 'Screen Name']



def write_into_list(data):

    #initialize an array
    row = []

    # add every 'cell' to the row list, identifying the item just like an index in a list
    row.append(data['text'])
    row.append(data['created_at'])
    row.append(data['lang'])
    row.append(data['retweet_count'])
    row.append(data['retweeted'])
    row.append(data['favorite_count'])
    row.append(data['favorited'])
    row.append(data['coordinates'])
    row.append(data['user']['name'])
    row.append(data['user']['screen_name'])

    return row

    #* retweeted - indicates that the current user has retweeted this particular status before
    #* favorited - indicates the current user has retweeted this particular status before

def convert_json_to_csv():
    print("Program begins")
    index = 0
    for filename in os.listdir(config.json_read_folder):
        tweet_data = []
        print("Converting file  :" + filename)
        csv_filename = filename[:-4] + "csv"
        try:
            # Create a file and include the header
            writer = csv.writer(open(config.csv_write_folder + csv_filename, 'w'))
            writer.writerow(csv_header)

            #Open the file where json data is stored and then load the json file
            with open(config.json_read_folder+filename) as file:
                for each_line in file:
                    parsed_json = json.loads(each_line.rstrip())
                    row =  write_into_list(parsed_json)
                    tweet_data.append(row)

            writer = csv.writer(open(config.csv_write_folder + csv_filename, 'a'))
            for eachrow in tweet_data:
                writer.writerow(eachrow)

            print("finished writing into the File %s" % csv_filename)
            index = index + 1
            print("________________________________________________")
        except:
            with open(config.csv_write_folder + "error_list_csv.txt", 'a') as f:
                f.write("Error occurred while writing to file %s" %csv_filename + "\n")
                print("Error is : " + str(sys.exc_info()[0]))
    print("number of files : " + str(index))










