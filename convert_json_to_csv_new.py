import json
import csv
import os
import config
import sys
import codecs

#to write into the csv header format. This will remain same across.
csv_header = ['text','created_at','text_id_str','lang','retweet_count','retweeted','favorite_count','favorited','co-ordinates','source','user_id_str','name', 'user_created_at', 'user_followers_count', 'user_friend_count','user_screenname','user_description', 'user_mentions_screenname','tweet_hashtags']



def write_into_file(data,csv_filename):


    user_mentions = ""
    user_text_hashtags = ""
    for sub_data in data['entities']['user_mentions']:
        user_mentions = user_mentions + sub_data['screen_name'] + "\t"
    for sub_data in data['entities']['hashtags']:
        user_text_hashtags = user_text_hashtags + sub_data['text'] + "\t"

    #initialize an array
    row = []

    # add every 'cell' to the row list, identifying the item just like an index in a list
    row.append(str(data['text'].encode("utf-8")))
    row.append(data['created_at'])
    row.append(data['id_str'])
    row.append(data['lang'])
    row.append(data['retweet_count'])
    row.append(data['retweeted'])
    row.append(data['favorite_count'])
    row.append(data['favorited'])
    row.append(data['coordinates'])
    row.append(data['source'])
    row.append(data['user']['id_str'])
    row.append(data['user']['name'])
    row.append(data['user']['created_at'])
    row.append(data['user']['followers_count'])
    row.append(data['user']['friends_count'])
    row.append(data['user']['screen_name'])
    row.append(data['user']['description'])
    row.append(user_mentions)
    row.append(user_text_hashtags)

    # once you have all the cells in there, write the row to your csv
    # Writing  each row of json file into the csv file
    print(row)
    writer = csv.writer(open(config.csv_write_folder + csv_filename, 'a'))
    writer.writerow(row)



def convert_json_to_csv():
    print("Program begins")
    for filename in os.listdir(config.json_read_folder):
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
                    write_into_file(parsed_json,csv_filename)
            print("finished writing into the File %s" % csv_filename)
            print("________________________________________________")
        except:
            with open(config.csv_write_folder + "error_list_csv.txt", 'a') as f:
                f.write("Error occurred while writing to file %s" %csv_filename + "\n")
                print("Error is : " + str(sys.exc_info()[0]))










