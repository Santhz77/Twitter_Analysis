from convert_json_to_csv_new import convert_json_to_csv
from convert__jsontocsv_perID import getUsersList
import os
import config




BASEURL= "https://app.receptiviti.com"

index = 0
#To convert the json file to csv file
# Before calling this function edit config.py
# Change the following parameters
# json_read_folder : Folder for the files containing json files
# csv_write_folder : Folder to write the csv files
#convert_json_to_csv()
#getUsersList()

def twitter_import_user_api_url(baseurl):
    return "{}/import/twitter/user".format(api_base_url(baseurl))


def api_base_url(baseurl):
    return "{}/api".format(baseurl)


resp = twitter_import_user_api_url(BASEURL)

print(resp)