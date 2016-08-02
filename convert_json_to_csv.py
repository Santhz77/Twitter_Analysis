import json
import csv
import os
import config
import sys
import codecs

#to write into the csv header format. This will remain same across.
csv_header = "text,created_at,text_id_str,lang,retweet_count,retweeted,favorite_count,favorited,"
csv_header = csv_header + "co-ordinates, source,"
csv_header = csv_header + "user_id_str,name, user_created_at, user_followers_count,"
csv_header = csv_header + "user_friend_count,user_screenname,user_description, user_mentions_screenname,tweet_hashtags"
csv_header = csv_header + "\n"


def preprare_text(data,index):
    text_modified = str(data[index]['text'].encode("utf-8"))  #.replace('"','double_quotes')
    temp_str = "\"" + text_modified + "\"" + ","
    temp_str = temp_str + str(data[index]['created_at']) + ","
    temp_str = temp_str + "\"" + str(data[index]['id_str']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['lang']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['retweet_count']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['retweeted']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['favorite_count']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['favorited']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['coordinates']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['source']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['id_str']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['name']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['created_at']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['followers_count']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['friends_count']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['screen_name']) + "\"" + ","
    temp_str = temp_str + "\"" + str(data[index]['user']['description']) + "\"" + ","
    user_mentions = ""
    user_text_hashtags = ""
    for sub_data in data[index]['entities']['user_mentions']:
        user_mentions = user_mentions + str(sub_data['screen_name']) + "\t"
    for sub_data in data[index]['entities']['hashtags']:
        user_text_hashtags = user_text_hashtags + str(sub_data['text']) + "\t"
    temp_str = temp_str + "\"" + user_mentions + "\"" + ","
    temp_str = temp_str + "\"" + user_text_hashtags + "\"" + "\n"
    return temp_str


def write_into_file(data, index,csv_filename):
    #Writing  each row of json file into the csv file
    with open(config.csv_write_folder + csv_filename, 'a') as f:
        single_tweet_data = preprare_text(data,index)
        print(single_tweet_data)
        f.write(single_tweet_data)


def convert_json_to_csv():
    print("Program begins")
    for filename in os.listdir(config.json_read_folder):
        print("filename :" + filename)
        data = []
        index = 0
        csv_filename = filename[:-4] + "csv"
        try:
            # Create a file and include the header
            with open(config.csv_write_folder + csv_filename, 'w', encoding="utf-8") as f:
                f.write(csv_header)

            #Open the file where json data is stored and then load the json file
            with open(config.json_read_folder+filename, encoding="utf-8") as file:
                for each_line in file:
                    data.append(json.loads(each_line.rstrip()))
                    write_into_file(data,index,csv_filename)
                    index += 1
            print("finished writing into the File %s" % csv_filename)
            print("________________________________________________")
        except:
            with open(config.csv_write_folder + "error_list_csv.txt", 'a') as f:
                f.write("Error occurred while writing to file %s" %csv_filename + "\n")
                print("Error is : " + str(sys.exc_info()[0]))










